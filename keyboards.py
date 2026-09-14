from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove,
    InlineKeyboardMarkup, InlineKeyboardButton,
)
from config import SERVICE_TYPES
from i18n import TEXTS, t, service_name

# ---------- Har bir tugma uchun barcha tillardagi variantlar (filter uchun) ----------
def _all_langs(key):
    return list(TEXTS[key].values())

BTN_CUSTOMER_ALL = _all_langs("btn_customer")
BTN_MASTER_ALL = _all_langs("btn_master")
BTN_SUPPORT_ALL = _all_langs("btn_support")
BTN_BALANCE_ALL = _all_langs("btn_balance")
BTN_PROFILE_ALL = _all_langs("btn_profile")
BTN_TOGGLE_BUSY_ALL = _all_langs("btn_toggle_busy")
BTN_TOPUP_ALL = _all_langs("btn_topup")
BTN_STATS_ALL = _all_langs("btn_stats")
BTN_NEW_ORDER_ALL = _all_langs("btn_new_order")
BTN_CANCEL_ALL = _all_langs("btn_cancel")
BTN_SKIP_PHOTO_ALL = _all_langs("btn_skip_photo")
BTN_PRICES_ALL = _all_langs("btn_prices")
BTN_MY_ORDERS_ALL = _all_langs("btn_my_orders")
BTN_PROMO_ALL = _all_langs("btn_promo")
BTN_SETTINGS_ALL = _all_langs("btn_settings")
BTN_TYPE_ADDRESS_ALL = _all_langs("btn_type_address")
BTN_USE_SAVED_ADDRESS_ALL = _all_langs("btn_use_saved_address")

# ---------- Standart (uz) qiymatlar — eski kod bilan moslik uchun ----------
BTN_CUSTOMER = TEXTS["btn_customer"]["uz"]
BTN_MASTER = TEXTS["btn_master"]["uz"]
BTN_SUPPORT = TEXTS["btn_support"]["uz"]
BTN_BALANCE = TEXTS["btn_balance"]["uz"]
BTN_PROFILE = TEXTS["btn_profile"]["uz"]
BTN_TOGGLE_BUSY = TEXTS["btn_toggle_busy"]["uz"]
BTN_TOPUP = TEXTS["btn_topup"]["uz"]
BTN_NEW_ORDER = TEXTS["btn_new_order"]["uz"]
BTN_CANCEL = TEXTS["btn_cancel"]["uz"]


def language_choice_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🇺🇿 O'zbek", callback_data="lang:uz"),
            InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang:ru"),
            InlineKeyboardButton(text="🇬🇧 English", callback_data="lang:en"),
        ]
    ])


def role_choice_kb(lang="uz"):
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=t("btn_customer", lang)),
                KeyboardButton(text=t("btn_master", lang)),
            ],
        ],
        resize_keyboard=True,
    )


def customer_menu_kb(lang="uz"):
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=t("btn_new_order", lang))],
            [KeyboardButton(text=t("btn_my_orders", lang)), KeyboardButton(text=t("btn_prices", lang))],
            [KeyboardButton(text=t("btn_promo", lang)), KeyboardButton(text=t("btn_settings", lang))],
            [KeyboardButton(text=t("btn_support", lang))],
        ],
        resize_keyboard=True,
    )


def master_menu_kb(lang="uz"):
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=t("btn_profile", lang)), KeyboardButton(text=t("btn_balance", lang))],
            [KeyboardButton(text=t("btn_toggle_busy", lang)), KeyboardButton(text=t("btn_topup", lang))],
            [KeyboardButton(text=t("btn_stats", lang))],
            [KeyboardButton(text=t("btn_support", lang))],
        ],
        resize_keyboard=True,
    )


def cancel_kb(lang="uz"):
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=t("btn_cancel", lang))]],
        resize_keyboard=True,
    )


def service_type_kb(prefix: str, lang="uz"):
    """prefix: 'cust_service' yoki 'mast_service' — callback_data ni farqlash uchun"""
    buttons = [
        [InlineKeyboardButton(text=service_name(key, lang), callback_data=f"{prefix}:{key}")]
        for key in SERVICE_TYPES
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def service_multiselect_kb(selected: list, lang="uz"):
    """Usta bir nechta xizmat turini tanlashi uchun — belgilangan tugmalarda ✅ ko'rinadi."""
    buttons = []
    for key in SERVICE_TYPES:
        mark = "✅ " if key in selected else ""
        buttons.append([InlineKeyboardButton(
            text=f"{mark}{service_name(key, lang)}", callback_data=f"mast_toggle:{key}"
        )])
    done_labels = {"uz": "✅ Tasdiqlash", "ru": "✅ Подтвердить", "en": "✅ Confirm"}
    buttons.append([InlineKeyboardButton(text=done_labels.get(lang, done_labels["uz"]), callback_data="mast_service_done")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def contact_request_kb(lang="uz"):
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=t("btn_send_phone", lang), request_contact=True)],
            [KeyboardButton(text=t("btn_cancel", lang))],
        ],
        resize_keyboard=True,
    )


def location_request_kb(lang="uz", offer_saved=False):
    keyboard = []
    if offer_saved:
        keyboard.append([KeyboardButton(text=t("btn_use_saved_address", lang))])
    keyboard.append([KeyboardButton(text=t("btn_send_location", lang), request_location=True)])
    keyboard.append([KeyboardButton(text=t("btn_type_address", lang))])
    keyboard.append([KeyboardButton(text=t("btn_cancel", lang))])
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def photo_request_kb(lang="uz"):
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=t("btn_skip_photo", lang))],
            [KeyboardButton(text=t("btn_cancel", lang))],
        ],
        resize_keyboard=True,
    )


def remove_kb():
    return ReplyKeyboardRemove()


def masters_list_kb(enriched_masters):
    """enriched_masters: [(master_row, distance_km), ...]"""
    from utils import estimate_eta_minutes
    buttons = []
    for m, dist in enriched_masters:
        if dist == float("inf"):
            dist_text = "📍 masofa noma'lum"
        else:
            eta = estimate_eta_minutes(dist)
            eta_text = f" | ⏱~{eta} daq" if eta else ""
            dist_text = f"📍{dist:.1f} km{eta_text}"
        text = f"👤 {m['full_name']} | {dist_text} | ⭐{m['rating']:.1f}"
        buttons.append([InlineKeyboardButton(text=text, callback_data=f"pick_master:{m['id']}")])
        buttons.append([InlineKeyboardButton(text="📝 Sharhlarni ko'rish", callback_data=f"view_reviews:{m['id']}")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def order_accept_kb(order_id: int):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Qabul qilish", callback_data=f"accept_order:{order_id}"),
            InlineKeyboardButton(text="❌ Rad etish", callback_data=f"decline_order:{order_id}"),
        ]
    ])


def price_confirm_kb(order_id: int):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Tasdiqlash", callback_data=f"confirm_price:{order_id}"),
            InlineKeyboardButton(text="❌ Bekor qilish", callback_data=f"cancel_order:{order_id}"),
        ]
    ])


def low_price_confirm_kb(order_id: int):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Ha, shu narxda davom etaman", callback_data=f"low_price_ok:{order_id}")],
        [InlineKeyboardButton(text="✏️ Narxni o'zgartiraman", callback_data=f"low_price_edit:{order_id}")],
    ])


def order_finish_kb(order_id: int):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Bajarildi deb belgilash", callback_data=f"finish_order:{order_id}")]
    ])


def stage_kb(order_id: int, stage: str):
    """Ustaning joriy ish bosqichiga qarab keyingi tugmani ko'rsatadi."""
    buttons = {
        "confirmed": [[InlineKeyboardButton(text="🚗 Yo'lga chiqdim", callback_data=f"stage_on_the_way:{order_id}")]],
        "on_the_way": [[InlineKeyboardButton(text="📍 Yetib keldim", callback_data=f"stage_arrived:{order_id}")]],
        "arrived": [[InlineKeyboardButton(text="🔧 Ishni boshladim", callback_data=f"stage_working:{order_id}")]],
        "working": [
            [InlineKeyboardButton(text="⏳ Deyarli tugadi", callback_data=f"stage_almost_done:{order_id}")],
            [InlineKeyboardButton(text="✅ Ishni tugatdim", callback_data=f"finish_order:{order_id}")],
        ],
        "almost_done": [[InlineKeyboardButton(text="✅ Ishni tugatdim", callback_data=f"finish_order:{order_id}")]],
    }
    return InlineKeyboardMarkup(inline_keyboard=buttons.get(stage, buttons["working"]))


def skip_comment_kb():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="⏭ O'tkazib yuborish")]],
        resize_keyboard=True,
    )


def rating_kb(order_id: int, role: str):
    buttons = [
        [InlineKeyboardButton(text="⭐" * i, callback_data=f"rate:{role}:{order_id}:{i}") for i in range(1, 4)],
        [InlineKeyboardButton(text="⭐" * i, callback_data=f"rate:{role}:{order_id}:{i}") for i in range(4, 6)],
    ]
    if role == "master":
        buttons.append(
            [InlineKeyboardButton(text="⚠️ Ish sifatidan norozi bo'lsam", callback_data=f"warranty_claim:{order_id}")]
        )
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def admin_master_review_kb(master_id: int):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Tasdiqlash", callback_data=f"admin_approve:{master_id}"),
            InlineKeyboardButton(text="❌ Rad etish", callback_data=f"admin_reject:{master_id}"),
        ]
    ])


def topup_admin_review_kb(request_id: int):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Qabul qilish", callback_data=f"topup_accept:{request_id}"),
            InlineKeyboardButton(text="❌ Rad etish", callback_data=f"topup_reject_req:{request_id}"),
        ]
    ])


def topup_confirm_kb(request_id: int):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ To'lovni tasdiqlash", callback_data=f"topup_confirm:{request_id}"),
            InlineKeyboardButton(text="❌ Rad etish", callback_data=f"topup_reject_proof:{request_id}"),
        ]
    ])


# ---------- Admin panel menyusi ----------
BTN_ADMIN_PENDING = "⏳ Kutilayotgan ustalar"
BTN_ADMIN_MASTERS = "🛠 Barcha ustalar"
BTN_ADMIN_CUSTOMERS = "🙋 Barcha mijozlar"
BTN_ADMIN_ACTIVE = "🔴 Faol buyurtmalar"
BTN_ADMIN_ORDERS = "📋 Buyurtmalar tarixi"
BTN_ADMIN_FUND = "🛡 Sug'urta jamg'armasi"
BTN_ADMIN_ADD_BALANCE = "💰 Balans qo'shish"
BTN_ADMIN_BLOCK = "🚫 Ustani bloklash"
BTN_ADMIN_UNBLOCK = "🔓 Blokdan chiqarish"
BTN_ADMIN_BLOCK_CUSTOMER = "🚫 Mijozni bloklash"
BTN_ADMIN_UNBLOCK_CUSTOMER = "🔓 Mijozni blokdan chiqarish"
BTN_ADMIN_REPLY = "💬 Foydalanuvchiga javob"
BTN_ADMIN_FUND_PAYOUT = "➖ Jamg'aradan to'lov"
BTN_ADMIN_STATS = "📊 Statistika"
BTN_ADMIN_BROADCAST = "📢 Ommaviy xabar"
BTN_ADMIN_AUDIT = "🧾 Admin harakatlari"
BTN_ADMIN_MASTERS_MAP = "🗺 Ustalar joylashuvi"
BTN_ADMIN_CHART = "📈 O'sish grafigi"
BTN_ADMIN_HELP = "ℹ️ Buyruqlar ro'yxati"
BTN_ADMIN_CANCEL = "❌ Bekor qilish"


def admin_menu_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=BTN_ADMIN_STATS), KeyboardButton(text=BTN_ADMIN_CHART)],
            [KeyboardButton(text=BTN_ADMIN_PENDING)],
            [KeyboardButton(text=BTN_ADMIN_MASTERS), KeyboardButton(text=BTN_ADMIN_CUSTOMERS)],
            [KeyboardButton(text=BTN_ADMIN_ACTIVE), KeyboardButton(text=BTN_ADMIN_ORDERS)],
            [KeyboardButton(text=BTN_ADMIN_MASTERS_MAP)],
            [KeyboardButton(text=BTN_ADMIN_ADD_BALANCE), KeyboardButton(text=BTN_ADMIN_REPLY)],
            [KeyboardButton(text=BTN_ADMIN_BLOCK), KeyboardButton(text=BTN_ADMIN_UNBLOCK)],
            [KeyboardButton(text=BTN_ADMIN_BLOCK_CUSTOMER), KeyboardButton(text=BTN_ADMIN_UNBLOCK_CUSTOMER)],
            [KeyboardButton(text=BTN_ADMIN_FUND), KeyboardButton(text=BTN_ADMIN_FUND_PAYOUT)],
            [KeyboardButton(text=BTN_ADMIN_BROADCAST), KeyboardButton(text=BTN_ADMIN_AUDIT)],
            [KeyboardButton(text=BTN_ADMIN_HELP)],
        ],
        resize_keyboard=True,
    )


def admin_cancel_kb():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=BTN_ADMIN_CANCEL)]],
        resize_keyboard=True,
    )


def broadcast_target_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🛠 Barcha ustalarga")],
            [KeyboardButton(text="🙋 Barcha mijozlarga")],
            [KeyboardButton(text=BTN_ADMIN_CANCEL)],
        ],
        resize_keyboard=True,
    )
