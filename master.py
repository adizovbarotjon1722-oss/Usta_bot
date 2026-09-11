from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter

import database as db
import keyboards as kb
from states import MasterRegister, MasterPricing
from config import SERVICE_TYPES, ADMIN_IDS, FREE_ORDERS_COUNT

router = Router()

_REGISTER_STATES = (
    MasterRegister.entering_name,
    MasterRegister.entering_passport,
    MasterRegister.entering_phone,
    MasterRegister.choosing_service,
    MasterRegister.sending_location,
    MasterRegister.sending_photo,
)


@router.message(F.text == kb.BTN_MASTER)
async def master_start(message: Message, state: FSMContext):
    existing = await db.get_master(message.from_user.id)

    if existing and existing["status"] == "verified":
        await message.answer(
            "Xush kelibsiz! 🛠", reply_markup=kb.master_menu_kb()
        )
        return
    if existing and existing["status"] == "pending":
        await message.answer(
            "⏳ Arizangiz hali ko'rib chiqilmoqda. Admin tasdig'ini kuting.",
            reply_markup=kb.remove_kb(),
        )
        return
    if existing and existing["status"] == "rejected":
        await message.answer(
            "Afsuski, avvalgi arizangiz rad etilgan edi. Savol bo'lsa, "
            f"{kb.BTN_SUPPORT} orqali admin bilan bog'laning."
        )
        return

    await db.create_master(message.from_user.id)
    await state.set_state(MasterRegister.entering_name)
    await message.answer(
        "🛠 Usta sifatida ro'yxatdan o'tish\n\n"
        "To'liq ism-familiyangizni kiriting:",
        reply_markup=kb.cancel_kb(),
    )


@router.message(StateFilter(*_REGISTER_STATES), F.text == kb.BTN_CANCEL)
async def master_register_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Ro'yxatdan o'tish bekor qilindi.", reply_markup=kb.role_choice_kb())


@router.message(MasterRegister.entering_name)
async def master_name_entered(message: Message, state: FSMContext):
    await state.update_data(full_name=message.text)
    await state.set_state(MasterRegister.entering_passport)
    await message.answer(
        "Pasport seriya va raqamingizni kiriting (masalan: AB1234567).\n\n"
        "⚠️ Bu ma'lumot faqat verifikatsiya uchun ishlatiladi va uchinchi shaxslarga berilmaydi."
    )


@router.message(MasterRegister.entering_passport)
async def master_passport_entered(message: Message, state: FSMContext):
    await state.update_data(passport_number=message.text)
    await state.set_state(MasterRegister.entering_phone)
    await message.answer(
        "Telefon raqamingizni yuboring:",
        reply_markup=kb.contact_request_kb(),
    )


@router.message(MasterRegister.entering_phone, F.contact)
async def master_phone_entered(message: Message, state: FSMContext):
    await state.update_data(phone=message.contact.phone_number)
    await state.set_state(MasterRegister.choosing_service)
    await message.answer(
        "Qaysi xizmat turida ishlaysiz?",
        reply_markup=kb.remove_kb(),
    )
    await message.answer("Tanlang:", reply_markup=kb.service_type_kb("mast_service"))


@router.callback_query(MasterRegister.choosing_service, F.data.startswith("mast_service:"))
async def master_service_chosen(callback: CallbackQuery, state: FSMContext):
    service_type = callback.data.split(":")[1]
    await state.update_data(service_type=service_type)
    await state.set_state(MasterRegister.sending_location)
    await callback.message.answer(
        "Doimiy ish hududingiz (uy/ofis) joylashuvini yuboring:",
        reply_markup=kb.location_request_kb(),
    )
    await callback.answer()


@router.message(MasterRegister.sending_location, F.location)
async def master_location_sent(message: Message, state: FSMContext):
    await state.update_data(
        latitude=message.location.latitude,
        longitude=message.location.longitude,
    )
    await state.set_state(MasterRegister.sending_photo)
    await message.answer(
        "📷 Profilingiz uchun o'z rasmingizni yuboring (mijozlar sizni tanishi uchun).\n"
        "Xohlamasangiz, o'tkazib yuborishingiz mumkin:",
        reply_markup=kb.photo_request_kb(),
    )


@router.message(MasterRegister.sending_photo, F.photo)
async def master_photo_sent(message: Message, state: FSMContext, bot: Bot):
    photo_file_id = message.photo[-1].file_id
    await _finish_master_registration(message, state, bot, photo_file_id)


@router.message(MasterRegister.sending_photo, F.text == "⏭ O'tkazib yuborish")
async def master_photo_skipped(message: Message, state: FSMContext, bot: Bot):
    await _finish_master_registration(message, state, bot, None)


async def _finish_master_registration(message: Message, state: FSMContext, bot: Bot, photo_file_id):
    data = await state.get_data()
    await db.update_master(
        message.from_user.id,
        full_name=data["full_name"],
        passport_number=data["passport_number"],
        phone=data["phone"],
        service_type=data["service_type"],
        latitude=data["latitude"],
        longitude=data["longitude"],
        photo_file_id=photo_file_id,
        status="pending",
    )
    await message.answer(
        "✅ Arizangiz qabul qilindi. Admin tasdig'idan so'ng ishni boshlashingiz mumkin.",
        reply_markup=kb.remove_kb(),
    )

    master = await db.get_master(message.from_user.id)
    caption = (
        f"🆕 Yangi usta arizasi\n\n"
        f"Ism: {master['full_name']}\n"
        f"Pasport: {master['passport_number']}\n"
        f"Telefon: {master['phone']}\n"
        f"Xizmat: {SERVICE_TYPES[master['service_type']]}\n"
        f"Telegram ID: {master['telegram_id']}"
    )
    for admin_id in ADMIN_IDS:
        try:
            if photo_file_id:
                await bot.send_photo(
                    admin_id, photo_file_id, caption=caption,
                    reply_markup=kb.admin_master_review_kb(master["id"]),
                )
            else:
                await bot.send_message(
                    admin_id, caption, reply_markup=kb.admin_master_review_kb(master["id"]),
                )
        except Exception:
            pass
    await state.clear()


@router.callback_query(F.data.startswith("accept_order:"))
async def master_accept_order(callback: CallbackQuery, state: FSMContext):
    order_id = int(callback.data.split(":")[1])
    order = await db.get_order(order_id)
    if not order or order["status"] != "offered":
        await callback.answer("Bu buyurtma allaqachon boshqa holatda.", show_alert=True)
        return

    master = await db.get_master(callback.from_user.id)
    if not master or master["status"] != "verified":
        await callback.answer("Sizning hisobingiz tasdiqlanmagan.", show_alert=True)
        return

    if master["free_orders_left"] <= 0 and master["balance"] <= 0:
        await callback.answer(
            "❌ Balansingiz yetarli emas. Buyurtma qabul qilish uchun hisobingizni to'ldiring "
            "(🆘 Qo'llab-quvvatlash orqali admin bilan bog'laning).",
            show_alert=True,
        )
        return

    await db.update_order(order_id, status="pricing")
    await state.update_data(pricing_order_id=order_id)
    await state.set_state(MasterPricing.entering_price)
    try:
        await callback.message.edit_text(callback.message.text + "\n\n✅ Siz qabul qildingiz.")
    except Exception:
        pass
    await callback.message.answer(
        "💵 Ish narxini kiriting (faqat son, so'mda, masalan: 150000):"
    )
    await callback.answer()


@router.callback_query(F.data.startswith("decline_order:"))
async def master_decline_order(callback: CallbackQuery):
    order_id = int(callback.data.split(":")[1])
    await db.update_order(order_id, status="cancelled", master_id=None)
    try:
        await callback.message.edit_text(callback.message.text + "\n\n❌ Siz rad etdingiz.")
    except Exception:
        pass
    await callback.answer()


@router.message(MasterPricing.entering_price)
async def master_price_entered(message: Message, state: FSMContext, bot: Bot):
    cleaned = message.text.replace(" ", "").replace(",", "")
    if not cleaned.isdigit():
        await message.answer("Iltimos, faqat raqam kiriting (masalan: 150000):")
        return

    price = float(cleaned)
    data = await state.get_data()
    order_id = data["pricing_order_id"]

    await db.update_order(order_id, price=price, status="offered_price")
    order = await db.get_order(order_id)
    customer = await db.get_customer_by_id(order["customer_id"])

    await message.answer(
        f"✅ Narx ({price:.0f} so'm) mijozga yuborildi. Tasdig'ini kuting.",
        reply_markup=kb.master_menu_kb(),
    )
    await state.clear()

    if customer:
        await bot.send_message(
            customer["telegram_id"],
            f"💰 Usta narx taklif qildi: <b>{price:.0f} so'm</b>\n"
            f"Buyurtma #{order_id}",
            reply_markup=kb.price_confirm_kb(order_id),
        )


@router.message(Command("balance"))
@router.message(F.text == kb.BTN_BALANCE)
async def master_balance(message: Message):
    master = await db.get_master(message.from_user.id)
    if not master or master["status"] != "verified":
        await message.answer("Siz hali usta sifatida tasdiqlanmagansiz.")
        return
    free_text = (
        f"🎁 Bepul buyurtmalar qoldi: {master['free_orders_left']}\n"
        if master["free_orders_left"] > 0 else ""
    )
    await message.answer(
        f"💰 Balansingiz: <b>{master['balance']:.0f} so'm</b>\n{free_text}",
    )


@router.message(Command("profile"))
@router.message(F.text == kb.BTN_PROFILE)
async def master_profile(message: Message):
    master = await db.get_master(message.from_user.id)
    if not master or master["status"] != "verified":
        await message.answer("Siz hali usta sifatida tasdiqlanmagansiz.")
        return

    busy_text = "🔴 Band" if master["is_busy"] else "🟢 Bo'sh"
    caption = (
        f"👤 <b>{master['full_name']}</b>\n"
        f"🛠 Xizmat: {SERVICE_TYPES.get(master['service_type'], master['service_type'])}\n"
        f"⭐ Reyting: {master['rating']:.1f} ({master['rating_count']} baho)\n"
        f"💰 Balans: {master['balance']:.0f} so'm\n"
        f"🎁 Bepul buyurtmalar: {master['free_orders_left']}\n"
        f"📶 Holat: {busy_text}"
    )
    if master["photo_file_id"]:
        await message.answer_photo(master["photo_file_id"], caption=caption)
    else:
        await message.answer(caption)


@router.message(Command("mybusy"))
@router.message(F.text == kb.BTN_TOGGLE_BUSY)
async def master_toggle_busy(message: Message):
    master = await db.get_master(message.from_user.id)
    if not master or master["status"] != "verified":
        return
    new_busy = 0 if master["is_busy"] else 1
    await db.update_master(message.from_user.id, is_busy=new_busy)
    status = "band 🔴" if new_busy else "bo'sh 🟢"
    await message.answer(f"Holatingiz endi: {status}")


@router.callback_query(F.data.startswith("finish_order:"))
async def master_finish_order(callback: CallbackQuery, bot: Bot):
    order_id = int(callback.data.split(":")[1])
    order = await db.get_order(order_id)
    if not order:
        await callback.answer("Buyurtma topilmadi.", show_alert=True)
        return
    await db.update_order(order_id, status="done")
    try:
        await callback.message.edit_text(callback.message.text + "\n\n✅ Bajarildi deb belgilandi.")
    except Exception:
        pass

    customer = await db.get_customer_by_id(order["customer_id"])
    if customer:
        await bot.send_message(
            customer["telegram_id"],
            f"✅ Buyurtma #{order_id} bajarildi. Ustani baholang:",
            reply_markup=kb.rating_kb(order_id, "master"),
        )

    from utils import notify_admins, format_order_line
    fresh_order = await db.get_order(order_id)
    await notify_admins(bot, "✅ Buyurtma yakunlandi:\n" + format_order_line(fresh_order))
    await callback.answer()
