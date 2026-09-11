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

- ⏳ Kutilayotgan ustalar — yangi arizalarni ko'rish va tasdiqlash/rad etish
- 🛠 Barcha ustalar — holati, reytingi, balansi, yoshi, tajribasi bilan
- 🙋 Barcha mijozlar
- 🔴 Faol buyurtmalar — hozir kim qaysi ish bilan band
- 📋 Buyurtmalar tarixi
- ℹ️ Buyruqlar ro'yxati

Matn buyruqlari ham ishlaydi: `/pending`, `/masters`, `/customers`, `/active`,
`/orders [soni]`, `/addbalance <master_id> <summa>`, `/reply <telegram_id> <matn>`.

## Fayl tuzilishi

```
usta-xizmati/
├── main.py              # bot ishga tushirish, til tanlash, global xato handler
├── config.py             # sozlamalar (token, admin, komissiya, narx oralig'i, karta)
├── i18n.py                # 3 tilli matnlar (uz/ru/en)
├── database.py             # SQLite bilan ishlash (CRUD, avtomatik migratsiya)
├── utils.py                # masofa hisoblash, admin xabar yuborish, formatlash
├── keyboards.py             # Telegram klaviaturalar (tilga mos)
├── states.py                 # FSM holatlari (suhbat bosqichlari)
└── handlers/
    ├── customer.py           # mijoz oqimi
    ├── master.py              # usta oqimi, jonli joylashuv, narx tizimi
    ├── admin.py                # admin panel
    ├── support.py               # qo'llab-quvvatlash oqimi
    └── topup.py                  # balansni to'ldirish oqimi
```

## Muhim — hozirgi cheklovlar (halol ro'yxat)

1. **3 tillilik qisman**: foydalanuvchi tomonidagi asosiy oqimlar (til tanlash,
   ro'yxatdan o'tish, buyurtma berish, menyular, tugmalar) to'liq tarjima qilingan.
   Ammo usta-mijoz o'rtasidagi ba'zi orqa fon xabarlari (narx taklifi matni,
   komissiya eslatmalari, "buyurtma bajarildi" kabi tizim xabarlari) va butun
   admin paneli hozircha faqat o'zbek tilida. Buni to'liq tarjima qilish katta
   qo'shimcha ish talab qiladi.
2. **Xavfsizlik**: pasport ma'lumotlari bazada shifrlanmagan holda saqlanadi
3. **Mijozni baholash**: hozir faqat usta baholanadi, mijozni ham baholash yo'q
4. **Bekor qilish siyosati**: usta yo'lga chiqqandan keyin bekor qilinsa nima
   bo'lishi (jarima va h.k.) belgilanmagan
5. **SQLite → PostgreSQL**: foydalanuvchilar ko'paysa, PostgreSQL'ga o'tish tavsiya
   etiladi
6. **Testlar**: avtomatik testlar yozilmagan
7. **Click/Payme integratsiyasi**: balans hozircha admin tomonidan qo'lda
   tasdiqlanadi (skrinshot orqali)
