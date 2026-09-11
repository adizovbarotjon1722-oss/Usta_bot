from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

import database as db
from config import ADMIN_IDS, SERVICE_TYPES, FREE_ORDERS_COUNT
from utils import format_order_line

router = Router()


def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS


@router.message(Command("pending"))
async def list_pending(message: Message):
    if not is_admin(message.from_user.id):
        return
    masters = await db.get_pending_masters()
    if not masters:
        await message.answer("Kutilayotgan arizalar yo'q.")
        return
    for m in masters:
        text = (
            f"#{m['id']} — {m['full_name']}\n"
            f"Pasport: {m['passport_number']}\n"
            f"Telefon: {m['phone']}\n"
            f"Xizmat: {SERVICE_TYPES.get(m['service_type'], m['service_type'])}"
        )
        if m["photo_file_id"]:
            await message.answer_photo(m["photo_file_id"], caption=text)
        else:
            await message.answer(text)


@router.callback_query(F.data.startswith("admin_approve:"))
async def admin_approve(callback: CallbackQuery, bot: Bot):
    if not is_admin(callback.from_user.id):
        await callback.answer("Ruxsat yo'q.", show_alert=True)
        return
    master_id = int(callback.data.split(":")[1])
    master = await db.get_master_by_id(master_id)
    if not master:
        await callback.answer("Usta topilmadi.", show_alert=True)
        return
    await db.update_master(master["telegram_id"], status="verified")

    try:
        await callback.message.edit_caption(caption=(callback.message.caption or "") + "\n\n✅ TASDIQLANDI")
    except Exception:
        try:
            await callback.message.edit_text(callback.message.text + "\n\n✅ TASDIQLANDI")
        except Exception:
            pass

    await bot.send_message(
        master["telegram_id"],
        "🎉 Tabriklaymiz! Arizangiz tasdiqlandi. Endi buyurtmalarni qabul qila olasiz.\n\n"
        f"🎁 Birinchi <b>{FREE_ORDERS_COUNT} ta buyurtma</b> uchun komissiya olinmaydi — "
        "bemalol ishlashni boshlang!\n\n"
        "Undan keyingi buyurtmalardan har birida 10% komissiya balansingizdan yechiladi. "
        "Balansni to'ldirish uchun admin bilan bog'laning (🆘 Qo'llab-quvvatlash tugmasi orqali).",
    )
    await callback.answer("Tasdiqlandi")


@router.callback_query(F.data.startswith("admin_reject:"))
async def admin_reject(callback: CallbackQuery, bot: Bot):
    if not is_admin(callback.from_user.id):
        await callback.answer("Ruxsat yo'q.", show_alert=True)
        return
    master_id = int(callback.data.split(":")[1])
    master = await db.get_master_by_id(master_id)
    if not master:
        await callback.answer("Usta topilmadi.", show_alert=True)
        return
    await db.update_master(master["telegram_id"], status="rejected")

    try:
        await callback.message.edit_caption(caption=(callback.message.caption or "") + "\n\n❌ RAD ETILDI")
    except Exception:
        try:
            await callback.message.edit_text(callback.message.text + "\n\n❌ RAD ETILDI")
        except Exception:
            pass

    await bot.send_message(master["telegram_id"], "Afsuski, arizangiz rad etildi.")
    await callback.answer("Rad etildi")


@router.message(Command("addbalance"))
async def add_balance(message: Message):
    """Foydalanish: /addbalance <master_id> <summa>"""
    if not is_admin(message.from_user.id):
        return
    parts = message.text.split()
    if len(parts) != 3:
        await message.answer("Foydalanish: /addbalance <master_id> <summa>")
        return
    try:
        master_id, amount = int(parts[1]), float(parts[2])
    except ValueError:
        await message.answer("master_id va summa raqam bo'lishi kerak.")
        return

    master = await db.get_master_by_id(master_id)
    if not master:
        await message.answer("Bunday usta topilmadi.")
        return

    await db.adjust_master_balance(master_id, amount)
    await message.answer(f"✅ {master['full_name']} balansiga {amount:.0f} so'm qo'shildi.")


@router.message(Command("orders"))
async def list_orders(message: Message):
    """Foydalanish: /orders [soni] — so'nggi buyurtmalar tarixi"""
    if not is_admin(message.from_user.id):
        return
    parts = message.text.split()
    limit = 20
    if len(parts) == 2 and parts[1].isdigit():
        limit = int(parts[1])

    orders = await db.get_recent_orders(limit)
    if not orders:
        await message.answer("Hozircha buyurtmalar yo'q.")
        return

    lines = [format_order_line(o) for o in orders]
    text = "📋 <b>So'nggi buyurtmalar</b>\n\n" + "\n".join(lines)
    # Telegram xabar uzunligi cheklovi (4096) — bo'lib yuborish
    for i in range(0, len(text), 3500):
        await message.answer(text[i:i + 3500])


@router.message(Command("reply"))
async def admin_reply(message: Message, bot: Bot):
    """Foydalanish: /reply <telegram_id> <matn> — foydalanuvchiga qo'llab-quvvatlash orqali javob berish"""
    if not is_admin(message.from_user.id):
        return
    parts = message.text.split(maxsplit=2)
    if len(parts) < 3:
        await message.answer("Foydalanish: /reply <telegram_id> <xabar matni>")
        return
    try:
        target_id = int(parts[1])
    except ValueError:
        await message.answer("telegram_id raqam bo'lishi kerak.")
        return
    reply_text = parts[2]

    try:
        await bot.send_message(target_id, f"💬 <b>Admin javobi:</b>\n{reply_text}")
        await message.answer("✅ Yuborildi.")
    except Exception as e:
        await message.answer(f"❌ Yuborib bo'lmadi: {e}")
