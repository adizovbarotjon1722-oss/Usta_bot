"""
Konfiguratsiya fayli.
BOT_TOKEN va ADMIN_IDS ni o'zingiznikiga almashtiring.
"""

# @BotFather dan olingan bot tokeni
BOT_TOKEN = "8388516466:AAFGAfU1ynptbibATNZN5Qa5zmRno2lcbm0"

# Admin(lar)ning Telegram user ID raqami (bir nechta bo'lishi mumkin)
# ID ni bilish uchun @userinfobot ga yozing
ADMIN_IDS = [1047268578]

# Platforma komissiyasi (10%)
COMMISSION_RATE = 0.10

# Usta ro'yxatdan o'tgandan so'ng komissiyasiz bajara oladigan buyurtmalar soni
FREE_ORDERS_COUNT = 1

# Balansni to'ldirish uchun admin/kompaniya kartasi ma'lumotlari
# (usta pul o'tkazishi uchun ustaga ko'rsatiladi)
ADMIN_CARD_NUMBER = "9860 3501 4575 6861"
ADMIN_CARD_HOLDER = "Adizov Barotjon"

# Xizmat turlari
SERVICE_TYPES = {
    "electric": "⚡ Elektrik",
    "plumber": "🔧 Santexnik",
    "cleaning": "🧹 Uy tozalash",
}

# Har bir xizmat turi uchun tavsiya etilgan narx oralig'i (so'mda).
# Bu — ustaga yo'l-yo'riq sifatida ko'rsatiladi va ish haqini arzonga
# baholamasligi uchun mo'ljal beradi. Zarur bo'lsa raqamlarni o'zgartiring.
PRICE_RANGES = {
    "electric": (50_000, 300_000),
    "plumber": (50_000, 350_000),
    "cleaning": (100_000, 500_000),
}

# Agar usta shu chegaradan (min narxning shu nisbatidan) past narx kiritsa,
# tizim uni bir bor ogohlantiradi va tasdiqlashni so'raydi.
LOW_PRICE_WARNING_RATIO = 0.5

# Ustalarni mijozga ko'rsatishda qidiriladigan maksimal radius (km)
SEARCH_RADIUS_KM = 5

# Ma'lumotlar bazasi fayli
DB_PATH = "usta_xizmati.db"
