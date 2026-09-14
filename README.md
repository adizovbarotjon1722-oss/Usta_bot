# Usta Chaqirish — Telegram Bot (MVP)

Elektrik, santexnik va uy tozalash xizmatlarini Telegram orqali buyurtma qilish tizimi.
3 tilda ishlaydi: o'zbek, rus, ingliz.

## Ishlash tamoyili

- **Yangi foydalanuvchi**: `/start` bosganda avval til tanlaydi (🇺🇿/🇷🇺/🇬🇧), so'ng
  "Mijozman" yoki "Ustaman" ni tanlaydi. Tanlangan til bazaga saqlanadi va botning
  keyingi barcha muloqoti (asosiy oqimlarda) o'sha tilda davom etadi.
- **Mijoz**: xizmat turini tanlaydi → muammoni yozadi (har bir xizmat turi uchun mos
  misol bilan) → lokatsiya va telefon yuboradi → eng yaqin va yuqori reytingli
  ustalar ro'yxatidan birini tanlaydi.
- **Usta**: ism, yosh, ish tajribasi, pasport, telefon, qo'shimcha telefon, xizmat
  turi, ish hududi va (ixtiyoriy) rasm bilan ro'yxatdan o'tadi → admin tasdig'ini
  kutadi → tasdiqlangach buyurtmalarni qabul qiladi, narx taklif qiladi (tavsiya
  etilgan narx oralig'i ko'rsatiladi, sezilarli past narxda ogohlantiriladi).
- **Jonli kuzatuv**: usta yo'lga chiqqach Telegram'ning "Share Live Location"
  funksiyasi orqali joylashuvini ulashsa, mijoz uni real vaqtda xaritada kuzatadi.
- **Admin**: tugmali panel orqali (`/admin` yoki admin sifatida `/start`) barcha
  ustalarni, mijozlarni, faol va tarixiy buyurtmalarni nazorat qiladi; yangi
  ustalarni tasdiqlaydi/rad etadi; balans to'ldirish so'rovlarini ko'rib chiqadi;
  qo'llab-quvvatlash xabarlariga javob beradi.
- **To'lov**: mijoz ustaga to'g'ridan-to'g'ri naqd/karta orqali to'laydi (platforma
  aralashmaydi). Buyurtma narxi tasdiqlangan zahoti, 10% komissiya ustaning ichki
  balansidan avtomatik yechiladi. Har bir yangi ustaning birinchi 2 ta buyurtmasi
  komissiyasiz. Balans yetarli bo'lmasa (va bepul buyurtmalar tugagan bo'lsa),
  usta yangi buyurtma qabul qila olmaydi — "💳 Balansni to'ldirish" tugmasi orqali
  so'rov yuboradi, admin karta raqamini beradi, usta skrinshot yuboradi, admin
  tasdiqlab balansni ko'taradi.

## O'rnatish

```bash
cd usta-xizmati
pip install -r requirements.txt
```

`config.py` faylida albatta o'zgartiring:
1. `BOT_TOKEN` — @BotFather dan olingan token
2. `ADMIN_IDS` — o'z Telegram ID raqamingiz (@userinfobot orqali bilib oling)
3. `ADMIN_CARD_NUMBER`, `ADMIN_CARD_HOLDER` — balans to'ldirish uchun ko'rsatiladigan karta

Ishga tushirish:

```bash
python main.py
```

Ma'lumotlar bazasi (`usta_xizmati.db`) birinchi ishga tushganda avtomatik yaratiladi;
kod yangilanganda eski bazadagi jadvallar avtomatik migratsiya qilinadi (qayta
o'rnatish shart emas).

## Admin panel

`/admin` buyrug'i (yoki admin sifatida oddiy `/start`) tugmali panelni ochadi:

- ⏳ Kutilayotgan ustalar — arizalar, hujjatlar (pasport, sudlanmaganlik
  ma'lumotnomasi, malaka hujjati) bilan birga, tasdiqlash/rad etish
- 🛠 Barcha ustalar — holati, reytingi, balansi, yoshi, tajribasi bilan
- 🙋 Barcha mijozlar
- 🔴 Faol buyurtmalar — hozir kim qaysi ish bilan band
- 📋 Buyurtmalar tarixi
- 🛡 Sug'urta jamg'armasi — balans va harakatlar tarixi
- ℹ️ Buyruqlar ro'yxati

Matn buyruqlari ham ishlaydi: `/pending`, `/masters`, `/customers`, `/active`,
`/orders [soni]`, `/addbalance <master_id> <summa>`, `/block <master_id>`,
`/unblock <master_id>`, `/fund`, `/fund_payout <summa> <sabab>`,
`/reply <telegram_id> <matn>`.

## Fayl tuzilishi

```
usta-xizmati/
├── main.py              # bot ishga tushirish, til tanlash, referal, global xato handler
├── config.py             # sozlamalar (token, admin, komissiya, narx, kafolat, jamg'arma)
├── i18n.py                # 3 tilli matnlar (uz/ru/en)
├── database.py             # SQLite bilan ishlash (CRUD, avtomatik migratsiya)
├── utils.py                # masofa/ETA hisoblash, admin xabar, formatlash
├── keyboards.py             # Telegram klaviaturalar (tilga mos)
├── states.py                 # FSM holatlari (suhbat bosqichlari)
└── handlers/
    ├── customer.py           # mijoz oqimi, sharhlar, kafolat, narxlar, promo
    ├── master.py              # usta oqimi, jonli joylashuv, hujjatlar, narx tizimi
    ├── admin.py                # admin panel, sifat nazorati, sug'urta jamg'armasi
    ├── support.py               # qo'llab-quvvatlash oqimi
    ├── topup.py                  # balansni to'ldirish oqimi
    └── relay.py                   # mijoz-usta o'rtasida anonim yozishma
webapp/                  # (ixtiyoriy) brauzerdagi admin nazorat paneli — batafsil: webapp/README.md
├── app.py
├── requirements.txt
└── templates/
```

## Ushbu yangilanishda qo'shilganlar

🖥 **Yangi: brauzerdagi admin veb-paneli** (`webapp/` papkasi) — statistika,
grafik, ustalar/mijozlar/buyurtmalar ro'yxatini brauzerda ko'rish uchun.
Batafsil o'rnatish yo'riqnomasi: `webapp/README.md`.

🔴 **KRITIK TUZATISH**: mijoz buyurtma berish jarayonida lokatsiya yuborganda,
kodda import qilinmagan funksiya sabab bot xato berib "qotib qolar" edi
(`NameError`). Bu — eng ustuvor tuzatish bo'ldi. Shu bilan birga butun kod
bazasi avtomatik tekshirildi — boshqa shunday yashirin xato topilmadi.

**Xizmat hududi va narxlar:**
- Xizmat hozircha faqat Toshkent shahri doirasida (GPS orqali ham, qo'lda
  yozilgan manzilda ham tekshiriladi — shahar nomi tilga olinishi shart)
- Qidiruv radiusi 5 km qilib **haqiqiy qo'llaniladi** (avval faqat eng yaqin
  8 tasi ko'rsatilib, masofa chegarasi tekshirilmagan edi)
- Komissiya 5%ga tushirildi

**Qulaylik:**
- Mijozning oldingi manzili eslab qolinadi — keyingi buyurtmada "📍 Oldingi
  manzilimdan foydalanish" tugmasi orqali qayta kiritmasdan foydalanish mumkin
- Usta ro'yxatdan o'tishda endi tavsiyanoma kontakti (uni tanigan odam) ham
  so'raladi — admin zarurat tug'ilsa tekshirish uchun bog'lanishi mumkin

**Allaqachon mavjud bo'lib, bu tekshiruvda tasdiqlangan keng qamrovli tizim:**
- SQLite WAL rejimi — ko'p foydalanuvchi bir vaqtda ishlaganda barqarorlik
- Usta ish bosqichlari: yo'lga chiqdi → yetib keldi → ishni boshladi →
  deyarli tugadi → tugatdi — har birida mijozga avtomatik xabar
- Admin ustaning **jonli joylashuvini** buyurtma davomida real vaqtda kuzatadi
- 📊 Kunlik/oylik statistika, 📈 o'sish grafiklari (matplotlib), 🗺 barcha
  ustalarning bazaviy joylashuv ro'yxati
- Admin uchun "tushunmadim" umumiy javob — hech qanday tugma botni "qotib
  qolgandek" tuyultirmaydi



🔴 **KRITIK TUZATISH**: mijoz buyurtma berish jarayonida lokatsiya yuborganda
bot xato berib "qotib qolishi" mumkin bo'lgan jiddiy dastur xatosi (import
qilinmagan funksiya) topildi va tuzatildi. Butun kod bazasi bo'ylab shunga
o'xshash boshqa xatolar avtomatik tekshiruv orqali yo'qligi tasdiqlandi.

**Qulaylik:**
- Toshkentdan tashqaridagi manzil (GPS yoki qo'lda yozilgan) endi to'g'ri
  rad etiladi — avval bu tekshiruv qo'lda yozilgan manzilda ishlamas edi
- 5 km radius endi haqiqatda qo'llaniladi (avval faqat "eng yaqin 8 ta"
  tanlanardi, radiusdan tashqarisi ham chiqishi mumkin edi)
- Mijozning oldingi manzili eslab qolinadi — keyingi buyurtmada
  "📍 Oldingi manzilimdan foydalanish" tugmasi bilan tezroq buyurtma berish



**Lokatsiya va qulaylik:**
- Mijoz endi manzilni GPS orqali YOKI qo'lda yozib kiritishi mumkin (agar
  joylashuvni ulashishni xohlamasa/ololmasa) — bu "qotib qolish" muammosini
  butunlay bartaraf etadi
- Masofa noma'lum bo'lganda "masofa noma'lum" deb chiroyli ko'rsatiladi

**Admin panel — endi to'liq tugma asosida:**
- 💰 Balans qo'shish, 🚫/🔓 Ustani va mijozni bloklash/blokdan chiqarish,
  💬 Foydalanuvchiga javob, ➖ Jamg'aradan to'lov — barchasi bosqichma-bosqich
  so'rov orqali (ID, summa, matn), buyruq yozish shart emas
- 📊 **Statistika** — jami/bugungi buyurtmalar, aylanma, komissiya daromadi,
  o'rtacha reyting, jamg'arma balansi — bitta ekranda
- 📢 **Ommaviy xabar** — barcha ustalarga yoki barcha mijozlarga bir vaqtda
  e'lon yuborish
- 🧾 **Admin harakatlari jurnali** — kim, qachon, nima qildi (balans qo'shish,
  bloklash, ommaviy xabar) — javobgarlik va nazorat uchun

## Muhim — "admin uchun alohida oyna" haqida

Bu so'rovni ikki xil tushunish mumkin:
1. **Telegram ichida alohida rejim** — bu allaqachon mavjud: admin `/admin`
   yoki oddiy `/start` bosganda butunlay boshqa menyu (yuqoridagi barcha
   tugmalar) ochiladi, mijoz/usta menyusidan farq qiladi.
2. **Haqiqiy alohida dastur (veb-sayt/desktop panel)** — bu Telegram bot
   doirasidan tashqarida, butunlay boshqa texnologiya (veb-server, hosting,
   domen) talab qiladigan **alohida loyiha**. Buni ham xohlasangiz, alohida
   muhokama qilib, boshidan rejalashtirish kerak bo'ladi.



**Xavfsizlik va ishonch:**
1. Mijozning aniq manzili endi faqat narx tasdiqlangandan SO'NG ustaga yuboriladi
2. **Telefon raqamlari butunlay yashiriladi** — mijoz va usta bir-birining
   raqamini ko'rmaydi; o'zaro yozishish uchun botga oddiy xabar (matn/rasm/ovoz/video)
   yozish kifoya — bot buni avtomatik boshqa tomonga, shaxsiy ma'lumotsiz, yetkazadi
3. **Qat'iy verifikatsiya**: ro'yxatdan o'tishda endi pasport raqamidan tashqari,
   sudlanmaganlik haqida ma'lumotnoma rasmi (majburiy) va malaka hujjati
   (ixtiyoriy) so'raladi — bular admin panelida ko'rinadi, admin qo'lda tekshiradi
4. **Ikki tomonlama reyting**: endi usta ham mijozni baholaydi, nafaqat aksincha
5. **Sifat nazorati**: past reytingli usta `config.py`dagi sozlamaga qarab
   avtomatik bloklanadi (yoki faqat ogohlantirish bilan cheklanadi);
   `/block`, `/unblock` orqali qo'lda ham boshqarish mumkin
6. **Kafolat**: har ish uchun kunlik kafolat, muammo takrorlansa kuchliroq
   til bilan ustaga eslatiladi (bepul tuzatish talabi)
7. **Sug'urta jamg'armasi**: har bir komissiyadan avtomatik ulush jamg'armaga
   o'tadi, admin panelida shaffof ko'rinadi, zarar to'lovlari qayd etiladi

**Biznes o'sishi:**
8. **Referral tizimi**: har bir mijoz o'zining shaxsiy taklif havolasiga ega
   ("🎁 Aksiya va Keshbek" bo'limida); do'sti birinchi buyurtmasini yakunlasa,
   taklif qilgan mijozga bonus xabari yuboriladi
9. **Ko'p xizmatli ustalar**: usta ro'yxatdan o'tishda bir nechta xizmat turini
   (masalan, Elektrik + Santexnik) belgilashi mumkin
10. **Yangi mijoz menyusi**: 💰 Narxlar, 📋 Mening buyurtmalarim, 🎁 Aksiya va
    Keshbek, ⚙️ Sozlamalar (tilni o'zgartirish) bo'limlari qo'shildi
11. **Geolokatsiya/ETA**: usta tanlashda masofa + taxminiy yetib borish vaqti

## Muhim — hozirgi cheklovlar (halol ro'yxat)

1. **Verifikatsiya — bot avtomatik tekshira olmaydi**: sudlanmaganlik
   ma'lumotnomasi va malaka hujjatining haqiqiyligini bot O'ZI tasdiqlay olmaydi
   (bunday davlat bazasiga ochiq API mavjud emas). Bot faqat hujjat rasmini
   yig'ib, admin panelida ko'rsatadi — yakuniy tekshiruv har doim ADMIN
   tomonidan qo'lda amalga oshiriladi. **Ichkilikbozlik, chekish yoki shunga
   o'xshash shaxsiy odatlarni bot texnik jihatdan umuman aniqlay olmaydi** —
   bunday narsalarni faqat inson (admin, shaxsiy suhbat, tavsiyanoma orqali
   tekshirish) baholay oladi. Shu sababli ro'yxatdan o'tishga **tavsiyanoma
   kontakti** (usta uchun kafolat bera oladigan shaxsning raqami) qo'shildi —
   bu to'liq yechim emas, balki admin uchun qo'shimcha tekshirish imkoniyati.
2. **Anonim yozishma cheksiz emas**: bot telefon RAQAM MAYDONINI yashiradi,
   lekin agar usta yoki mijoz xabar matnida o'z raqamini yozib qo'ysa (masalan
   "menga +998... orqali qo'ng'iroq qiling"), buni bot avtomatik bloklamaydi.
   Bu — istalgan shu turdagi platformaga (Uber, Yandex) xos umumiy cheklov.
3. **Platformani "aylanib o'tish" xavfi**: to'liq bartaraf etilmagan, faqat
   yumshatilgan (yashirin raqamlar + sodiqlik dasturi + kafolat faqat bot
   orqali buyurtmalarga taalluqli).
4. **3 tillilik qisman**: asosiy foydalanuvchi oqimlari to'liq tarjima
   qilingan, lekin butun admin paneli va ba'zi tizim xabarlari o'zbek tilida.
5. **Xavfsizlik**: pasport ma'lumotlari bazada shifrlanmagan holda saqlanadi
6. **Bekor qilish siyosati**: usta yo'lga chiqqandan keyin bekor qilinsa nima
   bo'lishi (jarima va h.k.) hali belgilanmagan
7. **SQLite → PostgreSQL**: foydalanuvchilar ko'paysa, PostgreSQL'ga o'tish
   tavsiya etiladi
8. **Testlar**: avtomatik testlar yozilmagan
9. **Click/Payme integratsiyasi**: balans hozircha admin tomonidan qo'lda
   tasdiqlanadi (skrinshot orqali)
10. **Referral bonusi**: hozircha faqat bildirishnoma darajasida (matnli
    e'lon) — avtomatik pul/chegirma-kod tizimi emas; buni amalga oshirish
    uchun admin qo'lda chegirma berishi kerak
