"""
Til tarjimalari (o'zbek / rus / ingliz).

Foydalanish: from i18n import t
t("welcome_title", lang)
t("service_chosen", lang, service=SERVICE_NAMES[lang][service_type])
"""

SERVICE_NAMES = {
    "uz": {"electric": "⚡ Elektrik", "plumber": "🔧 Santexnik", "cleaning": "🧹 Uy tozalash"},
    "ru": {"electric": "⚡ Электрик", "plumber": "🔧 Сантехник", "cleaning": "🧹 Уборка дома"},
    "en": {"electric": "⚡ Electrician", "plumber": "🔧 Plumber", "cleaning": "🧹 House cleaning"},
}

SERVICE_EXAMPLES = {
    "uz": {
        "electric": "✍️ Muammoni qisqacha tasvirlab bering.\nMasalan: \"Oshxonada rozetka ishlamayapti\":",
        "plumber": "✍️ Muammoni qisqacha tasvirlab bering.\nMasalan: \"Vannada quvur oqib yotibdi\":",
        "cleaning": "✍️ Qanday tozalash kerakligini qisqacha yozing.\nMasalan: \"3 xonali kvartirani umumiy tozalash kerak\":",
    },
    "ru": {
        "electric": "✍️ Кратко опишите проблему.\nНапример: «Не работает розетка на кухне»:",
        "plumber": "✍️ Кратко опишите проблему.\nНапример: «Течёт труба в ванной»:",
        "cleaning": "✍️ Кратко опишите, что нужно почистить.\nНапример: «Нужна генеральная уборка 3-комнатной квартиры»:",
    },
    "en": {
        "electric": "✍️ Briefly describe the problem.\nExample: \"Kitchen outlet isn't working\":",
        "plumber": "✍️ Briefly describe the problem.\nExample: \"Pipe is leaking in the bathroom\":",
        "cleaning": "✍️ Briefly describe what needs cleaning.\nExample: \"Need a full cleaning of a 3-room apartment\":",
    },
}

TEXTS = {
    "choose_language": (
        "🌐 Tilni tanlang / Выберите язык / Choose language:"
    ),
    "welcome": {
        "uz": (
            "Assalomu alaykum! 👋\n\n"
            "Bu — <b>elektrik, santexnik va uy tozalash</b> ustalarini Telegram orqali "
            "chaqirish xizmati.\n\n"
            "🔹 Tez va ishonchli\n"
            "🔹 Yaqin va yuqori reytingli ustalar\n"
            "🔹 Shaffof narxlar\n\n"
            "Kimsiz?"
        ),
        "ru": (
            "Здравствуйте! 👋\n\n"
            "Это — сервис вызова <b>электриков, сантехников и клинеров</b> через Telegram.\n\n"
            "🔹 Быстро и надёжно\n"
            "🔹 Ближайшие и высокорейтинговые мастера\n"
            "🔹 Прозрачные цены\n\n"
            "Кто вы?"
        ),
        "en": (
            "Hello! 👋\n\n"
            "This is a service for calling <b>electricians, plumbers and cleaners</b> via Telegram.\n\n"
            "🔹 Fast and reliable\n"
            "🔹 Nearby, highly-rated professionals\n"
            "🔹 Transparent pricing\n\n"
            "Who are you?"
        ),
    },
    "btn_customer": {"uz": "🙋 Mijozman", "ru": "🙋 Я клиент", "en": "🙋 I'm a customer"},
    "btn_master": {"uz": "🛠 Ustaman", "ru": "🛠 Я мастер", "en": "🛠 I'm a professional"},
    "btn_support": {"uz": "🆘 Qo'llab-quvvatlash", "ru": "🆘 Поддержка", "en": "🆘 Support"},
    "btn_balance": {"uz": "💰 Balansim", "ru": "💰 Мой баланс", "en": "💰 My balance"},
    "btn_profile": {"uz": "👤 Profilim", "ru": "👤 Мой профиль", "en": "👤 My profile"},
    "btn_toggle_busy": {"uz": "🔄 Holatni almashtirish", "ru": "🔄 Сменить статус", "en": "🔄 Toggle status"},
    "btn_topup": {"uz": "💳 Balansni to'ldirish", "ru": "💳 Пополнить баланс", "en": "💳 Top up balance"},
    "btn_stats": {"uz": "📊 Statistikam", "ru": "📊 Моя статистика", "en": "📊 My stats"},
    "btn_new_order": {"uz": "🆕 Yangi buyurtma", "ru": "🆕 Новый заказ", "en": "🆕 New order"},
    "btn_cancel": {"uz": "❌ Bekor qilish", "ru": "❌ Отмена", "en": "❌ Cancel"},
    "btn_prices": {"uz": "💰 Narxlar", "ru": "💰 Цены", "en": "💰 Prices"},
    "btn_my_orders": {"uz": "📋 Mening buyurtmalarim", "ru": "📋 Мои заказы", "en": "📋 My orders"},
    "btn_promo": {"uz": "🎁 Aksiya va Keshbek", "ru": "🎁 Акции и Кешбэк", "en": "🎁 Promo & Cashback"},
    "btn_settings": {"uz": "⚙️ Sozlamalar", "ru": "⚙️ Настройки", "en": "⚙️ Settings"},
    "btn_send_phone": {"uz": "📱 Raqamni yuborish", "ru": "📱 Отправить номер", "en": "📱 Send phone number"},
    "btn_send_location": {"uz": "📍 Joylashuvni yuborish", "ru": "📍 Отправить геолокацию", "en": "📍 Send location"},
    "btn_type_address": {"uz": "✍️ Manzilni yozib kiritish", "ru": "✍️ Ввести адрес текстом", "en": "✍️ Type address manually"},
    "btn_use_saved_address": {"uz": "📍 Oldingi manzilimdan foydalanish", "ru": "📍 Использовать прошлый адрес", "en": "📍 Use my previous address"},
    "btn_skip_photo": {"uz": "⏭ O'tkazib yuborish", "ru": "⏭ Пропустить", "en": "⏭ Skip"},

    "customer_menu_welcome": {
        "uz": "Xush kelibsiz! 🙋 Kerakli bo'limni tanlang:",
        "ru": "Добро пожаловать! 🙋 Выберите нужный раздел:",
        "en": "Welcome! 🙋 Choose a section:",
    },
    "master_menu_welcome": {
        "uz": "Xush kelibsiz! 🛠",
        "ru": "Добро пожаловать! 🛠",
        "en": "Welcome! 🛠",
    },
    "master_pending_wait": {
        "uz": "⏳ Arizangiz hali ko'rib chiqilmoqda. Admin tasdig'ini kuting.",
        "ru": "⏳ Ваша заявка ещё рассматривается. Ожидайте подтверждения администратора.",
        "en": "⏳ Your application is still under review. Please wait for admin approval.",
    },
    "master_rejected": {
        "uz": "Afsuski, avvalgi arizangiz rad etilgan edi.",
        "ru": "К сожалению, ваша предыдущая заявка была отклонена.",
        "en": "Unfortunately, your previous application was rejected.",
    },

    "choose_service": {
        "uz": "🆕 Yangi buyurtma\n\nQanday xizmat kerak?",
        "ru": "🆕 Новый заказ\n\nКакая услуга нужна?",
        "en": "🆕 New order\n\nWhich service do you need?",
    },
    "service_chosen_prefix": {
        "uz": "{service} tanlandi. ✅\n\n",
        "ru": "Выбрано: {service}. ✅\n\n",
        "en": "{service} selected. ✅\n\n",
    },
    "ask_location": {
        "uz": "📍 Manzilingiz joylashuvini yuboring:",
        "ru": "📍 Отправьте геолокацию вашего адреса:",
        "en": "📍 Please share your location:",
    },
    "ask_address_text": {
        "uz": "✍️ Manzilingizni to'liq yozing (mahalla, ko'cha, uy raqami):",
        "ru": "✍️ Напишите ваш полный адрес (район, улица, номер дома):",
        "en": "✍️ Type your full address (neighborhood, street, house number):",
    },
    "ask_phone": {
        "uz": "📱 Telefon raqamingizni yuboring:",
        "ru": "📱 Отправьте ваш номер телефона:",
        "en": "📱 Please send your phone number:",
    },
    "no_masters_found": {
        "uz": "😔 Afsuski, hozircha bu xizmat turi bo'yicha bo'sh usta topilmadi. Birozdan so'ng qayta urinib ko'ring.",
        "ru": "😔 К сожалению, свободных мастеров по этой услуге сейчас нет. Попробуйте позже.",
        "en": "😔 Unfortunately, no available professionals for this service right now. Please try again later.",
    },
    "nearby_masters": {
        "uz": "👷 Eng yaqin ustalar (masofa va reyting bo'yicha):",
        "ru": "👷 Ближайшие мастера (по расстоянию и рейтингу):",
        "en": "👷 Nearest professionals (by distance and rating):",
    },
    "choose_master": {
        "uz": "Ustani tanlang:",
        "ru": "Выберите мастера:",
        "en": "Choose a professional:",
    },
    "order_sent_to_master": {
        "uz": "✅ So'rovingiz ustaga yuborildi. Javobni kuting...",
        "ru": "✅ Ваш запрос отправлен мастеру. Ожидайте ответа...",
        "en": "✅ Your request has been sent to the professional. Awaiting response...",
    },
    "order_tracking_hint": {
        "uz": "Buyurtma holatini kuzatib boring. Usta javob berishi bilan sizga xabar beramiz. 🔔",
        "ru": "Следите за статусом заказа. Как только мастер ответит, мы вам сообщим. 🔔",
        "en": "Keep an eye on your order status. We'll notify you as soon as the professional responds. 🔔",
    },
    "cancel_done": {
        "uz": "Bekor qilindi.",
        "ru": "Отменено.",
        "en": "Cancelled.",
    },
    "order_cancelled": {
        "uz": "Buyurtma bekor qilindi.",
        "ru": "Заказ отменён.",
        "en": "Order cancelled.",
    },

    "support_prompt": {
        "uz": "🆘 Qo'llab-quvvatlash xizmati\n\nMuammoingizni yoki savolingizni yozing (matn yoki rasm yuborishingiz mumkin). Xabaringiz to'g'ridan-to'g'ri administratorga yetkaziladi.",
        "ru": "🆘 Служба поддержки\n\nОпишите вашу проблему или вопрос (можно отправить текст или фото). Ваше сообщение будет напрямую передано администратору.",
        "en": "🆘 Support\n\nDescribe your issue or question (you can send text or a photo). Your message will be forwarded directly to the admin.",
    },
    "support_sent": {
        "uz": "✅ Xabaringiz qabul qilindi. Tez orada admin siz bilan bog'lanadi.",
        "ru": "✅ Ваше сообщение принято. Администратор скоро свяжется с вами.",
        "en": "✅ Your message has been received. The admin will contact you soon.",
    },

    # --- Usta ro'yxatdan o'tish ---
    "register_intro": {
        "uz": "🛠 Usta sifatida ro'yxatdan o'tish\n\nTo'liq ism-familiyangizni kiriting:",
        "ru": "🛠 Регистрация в качестве мастера\n\nВведите ваше полное имя и фамилию:",
        "en": "🛠 Registering as a professional\n\nEnter your full name:",
    },
    "register_cancelled": {
        "uz": "Ro'yxatdan o'tish bekor qilindi.",
        "ru": "Регистрация отменена.",
        "en": "Registration cancelled.",
    },
    "ask_age": {
        "uz": "Yoshingizni kiriting (masalan: 27):",
        "ru": "Введите ваш возраст (например: 27):",
        "en": "Enter your age (e.g. 27):",
    },
    "ask_experience": {
        "uz": "Ish tajribangiz necha yil? (masalan: 3 yil, yoki \"yangi boshlovchi\"):",
        "ru": "Сколько лет опыта работы? (например: 3 года, или «начинающий»):",
        "en": "How many years of experience do you have? (e.g. 3 years, or \"beginner\"):",
    },
    "ask_passport": {
        "uz": "Pasport seriya va raqamingizni kiriting (masalan: AB1234567).\n\n⚠️ Bu ma'lumot faqat verifikatsiya uchun ishlatiladi va uchinchi shaxslarga berilmaydi.",
        "ru": "Введите серию и номер паспорта (например: AB1234567).\n\n⚠️ Эти данные используются только для верификации и не передаются третьим лицам.",
        "en": "Enter your passport series and number (e.g. AB1234567).\n\n⚠️ This is used only for verification and will not be shared with third parties.",
    },
    "ask_phone_master": {
        "uz": "Telefon raqamingizni yuboring:",
        "ru": "Отправьте ваш номер телефона:",
        "en": "Send your phone number:",
    },
    "ask_extra_phone": {
        "uz": "Qo'shimcha (zaxira) telefon raqamingiz bormi? Kiriting, yoki \"yo'q\" deb yozing:",
        "ru": "Есть ли у вас дополнительный (запасной) номер телефона? Введите его, или напишите «нет»:",
        "en": "Do you have an additional (backup) phone number? Enter it, or type \"no\":",
    },
    "ask_service_type": {
        "uz": "Qaysi xizmat turida ishlaysiz?",
        "ru": "В какой сфере услуг вы работаете?",
        "en": "Which service do you provide?",
    },
    "ask_work_location": {
        "uz": "Doimiy ish hududingiz (uy/ofis) joylashuvini yuboring:",
        "ru": "Отправьте геолокацию вашего постоянного района работы (дом/офис):",
        "en": "Send the location of your regular working area (home/office):",
    },
    "ask_photo": {
        "uz": "📷 Profilingiz uchun o'z rasmingizni yuboring (mijozlar sizni tanishi uchun).\nXohlamasangiz, o'tkazib yuborishingiz mumkin:",
        "ru": "📷 Отправьте своё фото для профиля (чтобы клиенты вас узнавали).\nЕсли не хотите — можете пропустить:",
        "en": "📷 Send a photo for your profile (so customers can recognize you).\nYou can skip this if you prefer:",
    },
    "register_done": {
        "uz": "✅ Arizangiz qabul qilindi. Admin tasdig'idan so'ng ishni boshlashingiz mumkin.",
        "ru": "✅ Ваша заявка принята. После подтверждения администратора вы сможете начать работу.",
        "en": "✅ Your application has been received. You can start working once approved by the admin.",
    },
    "not_verified_yet": {
        "uz": "Siz hali usta sifatida tasdiqlanmagansiz.",
        "ru": "Вы ещё не подтверждены как мастер.",
        "en": "You have not been verified as a professional yet.",
    },
}


def t(key: str, lang: str = "uz", **kwargs) -> str:
    lang = lang if lang in ("uz", "ru", "en") else "uz"
    entry = TEXTS.get(key)
    if entry is None:
        return key
    if isinstance(entry, dict):
        text = entry.get(lang, entry.get("uz", key))
    else:
        text = entry
    if kwargs:
        try:
            text = text.format(**kwargs)
        except Exception:
            pass
    return text


def service_name(service_type: str, lang: str = "uz") -> str:
    lang = lang if lang in ("uz", "ru", "en") else "uz"
    return SERVICE_NAMES.get(lang, SERVICE_NAMES["uz"]).get(service_type, service_type)


def service_example(service_type: str, lang: str = "uz") -> str:
    lang = lang if lang in ("uz", "ru", "en") else "uz"
    return SERVICE_EXAMPLES.get(lang, SERVICE_EXAMPLES["uz"]).get(
        service_type, SERVICE_EXAMPLES["uz"]["electric"]
    )


def service_names_display(service_type_field: str, lang: str = "uz") -> str:
    """Ustaning bir nechta xizmat turini ('electric,plumber' kabi vergul bilan
    ajratilgan) o'qish uchun qulay ko'rinishda birlashtiradi."""
    if not service_type_field:
        return "—"
    keys = [k.strip() for k in service_type_field.split(",") if k.strip()]
    return " / ".join(service_name(k, lang) for k in keys)
