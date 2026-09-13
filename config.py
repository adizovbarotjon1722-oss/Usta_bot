"""
Konfiguratsiya fayli.
BOT_TOKEN va ADMIN_IDS ni o'zingiznikiga almashtiring.
"""

# @BotFather dan olingan bot tokeni
BOT_TOKEN = "8388516466:AAGl306VZBbdetjJDl3JJMqZ0s7aziQv0Bo"

# Admin(lar)ning Telegram user ID raqami (bir nechta bo'lishi mumkin)
# ID ni bilish uchun @userinfobot ga yozing
ADMIN_IDS = [1047268578]

# Platforma komissiyasi (10%)
COMMISSION_RATE = 0.10

# Usta ro'yxatdan o'tgandan so'ng komissiyasiz bajara oladigan buyurtmalar soni
FREE_ORDERS_COUNT = 2

# Balansni to'ldirish uchun admin/kompaniya kartasi ma'lumotlari
# (usta pul o'tkazishi uchun ustaga ko'rsatiladi)
ADMIN_CARD_NUMBER = "8600 0000 0000 0000"
ADMIN_CARD_HOLDER = "F.I.SH."

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
SEARCH_RADIUS_KM = 15

# Yetib borish vaqtini taxminiy hisoblash uchun o'rtacha shahar ichi tezlik (km/soat)
AVERAGE_SPEED_KMH = 25

# Bajarilgan ish uchun kafolat muddati (kun)
WARRANTY_DAYS = 5

# Sifat nazorati: reyting shu chegaradan past bo'lsa (kamida shuncha baho bilan),
# admin avtomatik ogohlantiriladi
LOW_RATING_THRESHOLD = 3.0
LOW_RATING_MIN_COUNT = 3

# True bo'lsa, yuqoridagi chegaradan past ustalar AVTOMATIK bloklanadi (yangi
# buyurtma qabul qila olmaydi, admin /unblock bilan qaytarishi mumkin).
# ESLATMA: bir nechta og'ir mijozning noxolis bahosi ham ustani bloklashi
# mumkin — shuning uchun False qilib, faqat ogohlantirish bilan cheklanish
# ham oqilona variant.
AUTO_BLOCK_ON_LOW_RATING = True

# Rag'batlantirish: mijoz shuncha buyurtmani yakunlagach tabriklanadi
LOYALTY_MILESTONES = [3, 5, 10, 20]

# Sug'urta jamg'armasi: platforma komissiyasining shuncha ulushi (masalan 0.10 = 10%)
# ustaning balansidan EMAS, balki platformaning o'z komissiyasidan jamg'armaga
# ajratiladi — usta uchun qo'shimcha xarajat emas.
INSURANCE_FUND_RATE = 0.10

# Referral: do'stini taklif qilgan mijoz, taklif qilingan kishi birinchi
# buyurtmasini yakunlagach ushbu matnli bonusni oladi (hozircha avtomatik pul
# emas — admin qo'lda his-sanoat sifatida amalga oshiradi, masalan chegirma).
REFERRAL_BONUS_NOTE = "Keyingi buyurtmangizda 10% chegirma"

# Ma'lumotlar bazasi fayli
DB_PATH = "usta_xizmati.db"
