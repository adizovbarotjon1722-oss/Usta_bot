import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, CallbackQuery, BotCommand, ErrorEvent

from config import BOT_TOKEN, ADMIN_IDS
import database as db
from database import init_db
import keyboards as kb
from i18n import t
from states import Onboarding
from handlers import customer, master, admin, support, topup
from utils import notify_admins

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def cmd_start(message: Message, state: FSMContext):
    if message.from_user.id in ADMIN_IDS:
        await state.clear()
        await message.answer(
            "👑 <b>Admin panel</b>\n\nKerakli bo'limni tanlang:",
            reply_markup=kb.admin_menu_kb(),
        )
        return

    master_row = await db.get_master(message.from_user.id)
    if master_row and master_row["status"] == "verified":
        await state.clear()
        lang = master_row["language"] or "uz"
        await message.answer(t("master_menu_welcome", lang), reply_markup=kb.master_menu_kb(lang))
        return
    if master_row and master_row["status"] == "pending":
        await state.clear()
        lang = master_row["language"] or "uz"
        await message.answer(t("master_pending_wait", lang), reply_markup=kb.remove_kb())
        return
    if master_row and master_row["status"] == "rejected":
        await state.clear()
        lang = master_row["language"] or "uz"
        await message.answer(t("master_rejected", lang))
        return

    customer_row = await db.get_customer(message.from_user.id)
    if customer_row:
        await state.clear()
        lang = customer_row["language"] or "uz"
        await message.answer(t("customer_menu_welcome", lang), reply_markup=kb.customer_menu_kb(lang))
        return

    # Yangi foydalanuvchi — avval tilni tanlatamiz
    await state.set_state(Onboarding.choosing_language)
    await message.answer(t("choose_language"), reply_markup=kb.language_choice_kb())


async def language_selected(callback: CallbackQuery, state: FSMContext):
    lang = callback.data.split(":")[1]
    if lang not in ("uz", "ru", "en"):
        lang = "uz"
    await state.update_data(lang=lang)
    await state.set_state(None)

    try:
        await callback.message.edit_reply_markup(reply_markup=None)
    except Exception:
        pass

    await callback.message.answer(t("welcome", lang), reply_markup=kb.role_choice_kb(lang))
    await callback.answer()


async def cmd_help(message: Message):
    lang = await db.get_lang(message.from_user.id)
    text = (
        "ℹ️ <b>Yordam</b>\n\n"
        "/start — botni qayta ishga tushirish\n"
        f"{t('btn_support', lang)} — admin bilan bog'lanish\n\n"
        "Agar biror muammo yuzaga kelsa, pastdagi qo'llab-quvvatlash tugmasi orqali "
        "bevosita administratorga yozishingiz mumkin."
    )
    if message.from_user.id in ADMIN_IDS:
        text += (
            "\n\n<b>Admin buyruqlari:</b>\n"
            "/pending — tasdiq kutayotgan ustalar\n"
            "/masters — barcha ustalar ro'yxati\n"
            "/customers — barcha mijozlar ro'yxati\n"
            "/active — hozir faol buyurtmalar (ustalar qanday ish bilan band)\n"
            "/orders [soni] — buyurtmalar tarixi\n"
            "/addbalance &lt;master_id&gt; &lt;summa&gt; — balans to'ldirish\n"
            "/block &lt;master_id&gt; — ustani bloklash\n"
            "/unblock &lt;master_id&gt; — blokdan chiqarish\n"
            "/reply &lt;telegram_id&gt; &lt;matn&gt; — qo'llab-quvvatlashga javob\n"
            "/admin — admin panelni ochish"
        )
    await message.answer(text)


async def setup_bot_commands(bot: Bot):
    await bot.set_my_commands([
        BotCommand(command="start", description="Botni ishga tushirish / Start / Запуск"),
        BotCommand(command="help", description="Yordam / Help / Помощь"),
    ])


async def main():
    await init_db()

    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(storage=MemoryStorage())

    dp.message.register(cmd_start, Command("start"))
    dp.message.register(cmd_start, Command("admin"))
    dp.message.register(cmd_help, Command("help"))
    dp.callback_query.register(language_selected, F.data.startswith("lang:"))

    dp.include_router(admin.router)
    dp.include_router(support.router)
    dp.include_router(master.router)
    dp.include_router(topup.router)
    dp.include_router(customer.router)

    @dp.error()
    async def global_error_handler(event: ErrorEvent):
        logger.exception("Xatolik yuz berdi: %s", event.exception)
        try:
            await notify_admins(
                bot,
                f"⚠️ Botda xatolik yuz berdi:\n<code>{event.exception}</code>",
            )
        except Exception:
            pass

        update = event.update
        chat_id = None
        if update.message:
            chat_id = update.message.chat.id
        elif update.callback_query and update.callback_query.message:
            chat_id = update.callback_query.message.chat.id

        if chat_id:
            try:
                await bot.send_message(
                    chat_id,
                    "⚠️ Kutilmagan xatolik yuz berdi. Iltimos, /start bosib qayta urinib ko'ring.",
                )
            except Exception:
                pass
        return True

    await setup_bot_commands(bot)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
