from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

import database as db
import keyboards as kb
from states import CustomerOrder
from utils import sort_masters_by_distance_and_rating, notify_admins, format_order_line
from config import SERVICE_TYPES, COMMISSION_RATE

router = Router()

_ORDER_STATES = (
    CustomerOrder.choosing_service,
    CustomerOrder.entering_description,
    CustomerOrder.sending_location,
    CustomerOrder.sending_phone,
    CustomerOrder.choosing_master,
)


@router.message(F.text == kb.BTN_CUSTOMER)
async def customer_start(message: Message, state: FSMContext):
    await db.create_customer(message.from_user.id)
    await message.answer(
        "Xush kelibsiz! 🙋 Kerakli bo'limni tanlang:",
        reply_markup=kb.customer_menu_kb(),
    )


@router.message(F.text == kb.BTN_NEW_ORDER)
async def customer_new_order(message: Message, state: FSMContext):
    await db.create_customer(message.from_user.id)
    await state.set_state(CustomerOrder.choosing_service)
    await message.answer(
        "🆕 Yangi buyurtma\n\nQanday xizmat kerak?",
        reply_markup=kb.service_type_kb("cust_service"),
    )


@router.message(StateFilter(*_ORDER_STATES), F.text == kb.BTN_CANCEL)
async def customer_order_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Buyurtma bekor qilindi.", reply_markup=kb.customer_menu_kb())


@router.callback_query(CustomerOrder.choosing_service, F.data.startswith("cust_service:"))
async def customer_service_chosen(callback: CallbackQuery, state: FSMContext):
    service_type = callback.data.split(":")[1]
    await state.update_data(service_type=service_type)
    await state.set_state(CustomerOrder.entering_description)
    await callback.message.answer(
        f"{SERVICE_TYPES[service_type]} tanlandi. ✅\n\n"
        "✍️ Muammoni qisqacha tasvirlab bering "
        "(masalan: \"Oshxonada rozetka ishlamayapti\"):",
        reply_markup=kb.cancel_kb(),
    )
    await callback.answer()


@router.message(CustomerOrder.entering_description)
async def customer_description_entered(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await state.set_state(CustomerOrder.sending_location)
    await message.answer(
        "📍 Manzilingiz joylashuvini yuboring:",
        reply_markup=kb.location_request_kb(),
    )


@router.message(CustomerOrder.sending_location, F.location)
async def customer_location_sent(message: Message, state: FSMContext):
    await state.update_data(
        latitude=message.location.latitude,
        longitude=message.location.longitude,
    )
    await state.set_state(CustomerOrder.sending_phone)
    await message.answer(
        "📱 Telefon raqamingizni yuboring:",
        reply_markup=kb.contact_request_kb(),
    )


@router.message(CustomerOrder.sending_phone, F.contact)
async def customer_phone_sent(message: Message, state: FSMContext):
    phone = message.contact.phone_number
    await db.update_customer(message.from_user.id, phone=phone)
    data = await state.get_data()

    masters = await db.get_verified_masters_by_service(data["service_type"])
    if not masters:
        await message.answer(
            "😔 Afsuski, hozircha bu xizmat turi bo'yicha bo'sh usta topilmadi. "
            "Birozdan so'ng qayta urinib ko'ring.",
            reply_markup=kb.customer_menu_kb(),
        )
        await state.clear()
        return

    enriched = sort_masters_by_distance_and_rating(masters, data["latitude"], data["longitude"])
    enriched = enriched[:8]  # eng yaqin 8 ta

    await state.update_data(phone=phone)
    await state.set_state(CustomerOrder.choosing_master)
    await message.answer(
        "👷 Eng yaqin ustalar (masofa va reyting bo'yicha):",
        reply_markup=kb.remove_kb(),
    )
    await message.answer("Ustani tanlang:", reply_markup=kb.masters_list_kb(enriched))


@router.callback_query(CustomerOrder.choosing_master, F.data.startswith("pick_master:"))
async def customer_master_picked(callback: CallbackQuery, state: FSMContext, bot: Bot):
    master_id = int(callback.data.split(":")[1])
    data = await state.get_data()

    customer = await db.get_customer(callback.from_user.id)
    order_id = await db.create_order(
        customer_id=customer["id"],
        service_type=data["service_type"],
        description=data["description"],
        latitude=data["latitude"],
        longitude=data["longitude"],
        address_text=None,
        phone=data["phone"],
    )
    await db.update_order(order_id, master_id=master_id, status="offered")

    master = await db.get_master_by_id(master_id)
    await callback.message.edit_text("✅ So'rovingiz ustaga yuborildi. Javobni kuting...")
    await callback.message.answer(
        "Buyurtma holatini kuzatib boring. Usta javob berishi bilan sizga xabar beramiz. 🔔",
        reply_markup=kb.customer_menu_kb(),
    )

    await bot.send_message(
        master["telegram_id"],
        f"🆕 <b>Yangi buyurtma #{order_id}</b>\n\n"
        f"Xizmat: {SERVICE_TYPES[data['service_type']]}\n"
        f"Tavsif: {data['description']}\n",
        reply_markup=kb.order_accept_kb(order_id),
    )

    order = await db.get_order(order_id)
    await notify_admins(bot, "🆕 Yangi buyurtma yaratildi:\n" + format_order_line(order))

    await state.clear()
    await callback.answer()


@router.callback_query(F.data.startswith("confirm_price:"))
async def customer_confirm_price(callback: CallbackQuery, bot: Bot):
    order_id = int(callback.data.split(":")[1])
    order = await db.get_order(order_id)
    if not order or order["status"] != "offered_price":
        await callback.answer("Bu buyurtma allaqachon boshqa holatda.", show_alert=True)
        return

    master = await db.get_master_by_id(order["master_id"])

    if master["free_orders_left"] > 0:
        commission = 0
        await db.decrement_free_orders(master["id"])
        commission_note = (
            f"🎁 Bu sizning bepul buyurtmalaringizdan biri edi — komissiya olinmadi. "
            f"Qolgan bepul buyurtmalar: {master['free_orders_left'] - 1}"
        )
    else:
        commission = round(order["price"] * COMMISSION_RATE)
        await db.adjust_master_balance(master["id"], -commission)
        commission_note = f"Komissiya ({commission:.0f} so'm) balansingizdan yechildi."

    await db.update_order(order_id, commission=commission, status="in_progress")

    try:
        await callback.message.edit_text(callback.message.text + "\n\n✅ Narx tasdiqlandi. Usta yo'lda.")
    except Exception:
        pass

    customer = await db.get_customer_by_id(order["customer_id"])

    # Ustaga xabar
    await bot.send_message(
        master["telegram_id"],
        f"✅ Mijoz narxni tasdiqladi (buyurtma #{order_id}).\n"
        f"📱 Mijoz telefoni: {customer['phone'] if customer else '-'}\n"
        f"{commission_note}",
        reply_markup=kb.order_finish_kb(order_id),
    )

    # Mijozga ustaning tanishtiruvi (ishonch uchun)
    intro = (
        f"👷 Sizga xizmat ko'rsatadigan usta:\n"
        f"<b>{master['full_name']}</b>\n"
        f"⭐ Reyting: {master['rating']:.1f}\n"
        f"📱 Telefon: {master['phone']}"
    )
    if master["photo_file_id"]:
        await bot.send_photo(callback.from_user.id, master["photo_file_id"], caption=intro)
    else:
        await bot.send_message(callback.from_user.id, intro)

    await callback.answer()


@router.callback_query(F.data.startswith("cancel_order:"))
async def customer_cancel_order(callback: CallbackQuery, bot: Bot):
    order_id = int(callback.data.split(":")[1])
    order = await db.get_order(order_id)
    await db.update_order(order_id, status="cancelled")
    try:
        await callback.message.edit_text(callback.message.text + "\n\n❌ Buyurtma bekor qilindi.")
    except Exception:
        pass

    if order and order["master_id"]:
        master = await db.get_master_by_id(order["master_id"])
        if master:
            await bot.send_message(master["telegram_id"], f"❌ Mijoz buyurtma #{order_id} ni bekor qildi.")
    await callback.answer()


@router.callback_query(F.data.startswith("rate:"))
async def handle_rating(callback: CallbackQuery, bot: Bot):
    _, role, order_id, stars = callback.data.split(":")
    order_id, stars = int(order_id), int(stars)
    order = await db.get_order(order_id)
    if not order:
        await callback.answer()
        return

    if role == "master":
        # mijoz ustani baholayapti
        await db.add_master_rating(order["master_id"], stars)

    try:
        await callback.message.edit_text(callback.message.text + f"\n\nBaho: {'⭐' * stars}. Rahmat!")
    except Exception:
        pass
    await callback.answer("Rahmat!")
