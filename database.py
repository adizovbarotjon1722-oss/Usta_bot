"""
Ma'lumotlar bazasi qatlami (SQLite, aiosqlite orqali).

Jadvallar:
- masters   : ustalar (verifikatsiya, balans, reyting, lokatsiya, rasm)
- customers : mijozlar
- orders    : buyurtmalar
- reviews   : ikki tomonlama baholashlar
"""

import aiosqlite
from datetime import datetime

from config import DB_PATH, FREE_ORDERS_COUNT


async def _add_column_if_missing(db, table: str, column_def: str):
    """SQLite'da ALTER TABLE ADD COLUMN ni xavfsiz bajaradi (ustun mavjud bo'lsa xato bermaydi)."""
    column_name = column_def.split()[0]
    try:
        await db.execute(f"ALTER TABLE {table} ADD COLUMN {column_def}")
    except aiosqlite.OperationalError as e:
        if "duplicate column name" not in str(e):
            raise


async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS masters (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_id INTEGER UNIQUE NOT NULL,
                full_name TEXT,
                phone TEXT,
                passport_number TEXT,
                service_type TEXT,
                latitude REAL,
                longitude REAL,
                balance REAL DEFAULT 0,
                rating REAL DEFAULT 5.0,
                rating_count INTEGER DEFAULT 0,
                status TEXT DEFAULT 'pending',   -- pending / verified / rejected / blocked
                is_busy INTEGER DEFAULT 0,
                photo_file_id TEXT,
                free_orders_left INTEGER DEFAULT 0,
                created_at TEXT
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_id INTEGER UNIQUE NOT NULL,
                full_name TEXT,
                phone TEXT,
                rating REAL DEFAULT 5.0,
                rating_count INTEGER DEFAULT 0,
                created_at TEXT
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER,
                master_id INTEGER,
                service_type TEXT,
                description TEXT,
                latitude REAL,
                longitude REAL,
                address_text TEXT,
                phone TEXT,
                price REAL,
                commission REAL,
                status TEXT DEFAULT 'searching',
                -- searching / offered / pricing / offered_price / in_progress / done / cancelled
                created_at TEXT,
                updated_at TEXT
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS reviews (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id INTEGER,
                from_role TEXT,   -- 'customer' or 'master'
                stars INTEGER,
                comment TEXT,
                created_at TEXT
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS topup_requests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                master_id INTEGER,
                amount REAL,
                status TEXT DEFAULT 'requested',
                -- requested / accepted / proof_submitted / confirmed / rejected
                screenshot_file_id TEXT,
                created_at TEXT,
                updated_at TEXT
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS insurance_fund_ledger (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id INTEGER,
                amount REAL,
                note TEXT,
                created_at TEXT
            )
        """)

        # Eski bazalarda yo'q bo'lishi mumkin bo'lgan ustunlarni xavfsiz qo'shish
        await _add_column_if_missing(db, "masters", "photo_file_id TEXT")
        await _add_column_if_missing(db, "masters", f"free_orders_left INTEGER DEFAULT {FREE_ORDERS_COUNT}")
        await _add_column_if_missing(db, "orders", "tracking_message_id INTEGER")
        await _add_column_if_missing(db, "orders", "tracking_chat_id INTEGER")
        await _add_column_if_missing(db, "masters", "age INTEGER")
        await _add_column_if_missing(db, "masters", "experience_years TEXT")
        await _add_column_if_missing(db, "masters", "extra_phone TEXT")
        await _add_column_if_missing(db, "masters", "language TEXT DEFAULT 'uz'")
        await _add_column_if_missing(db, "customers", "language TEXT DEFAULT 'uz'")
        await _add_column_if_missing(db, "orders", "warranty_until TEXT")
        await _add_column_if_missing(db, "customers", "completed_orders INTEGER DEFAULT 0")
        await _add_column_if_missing(db, "masters", "criminal_record_photo TEXT")
        await _add_column_if_missing(db, "masters", "qualification_photo TEXT")
        await _add_column_if_missing(db, "orders", "warranty_claims_count INTEGER DEFAULT 0")
        await _add_column_if_missing(db, "customers", "referred_by INTEGER")
        await _add_column_if_missing(db, "customers", "referral_bonus_given INTEGER DEFAULT 0")
        await _add_column_if_missing(db, "orders", "description_photo TEXT")

        await db.commit()


def now() -> str:
    return datetime.utcnow().isoformat()


async def get_lang(telegram_id: int) -> str:
    """Foydalanuvchining saqlangan tilini aniqlaydi (usta yoki mijoz sifatida), aks holda 'uz'."""
    master = await get_master(telegram_id)
    if master and master["language"]:
        return master["language"]
    customer = await get_customer(telegram_id)
    if customer and customer["language"]:
        return customer["language"]
    return "uz"


# ---------- MASTERS ----------

async def create_master(telegram_id: int, language: str = "uz"):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT OR IGNORE INTO masters (telegram_id, free_orders_left, language, created_at) "
            "VALUES (?, ?, ?, ?)",
            (telegram_id, FREE_ORDERS_COUNT, language, now()),
        )
        await db.commit()


async def update_master(telegram_id: int, **fields):
    if not fields:
        return
    keys = ", ".join(f"{k} = ?" for k in fields)
    values = list(fields.values()) + [telegram_id]
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(f"UPDATE masters SET {keys} WHERE telegram_id = ?", values)
        await db.commit()


async def get_master(telegram_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute("SELECT * FROM masters WHERE telegram_id = ?", (telegram_id,))
        return await cur.fetchone()


async def get_master_by_id(master_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute("SELECT * FROM masters WHERE id = ?", (master_id,))
        return await cur.fetchone()


async def get_pending_masters():
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute("SELECT * FROM masters WHERE status = 'pending'")
        return await cur.fetchall()


async def get_all_masters():
    """Admin panel uchun — barcha ro'yxatdan o'tgan ustalar (holatidan qat'iy nazar)."""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute("SELECT * FROM masters ORDER BY id DESC")
        return await cur.fetchall()


async def get_verified_masters_by_service(service_type: str):
    """Usta bir nechta xizmat turini ko'rsatishi mumkin (masters.service_type da
    vergul bilan ajratilgan, masalan 'electric,plumber'), shuning uchun
    aniq moslikni emas, ro'yxat ichida borligini tekshiramiz."""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute(
            "SELECT * FROM masters WHERE status = 'verified' AND is_busy = 0 "
            "AND (',' || service_type || ',') LIKE ('%,' || ? || ',%')",
            (service_type,),
        )
        return await cur.fetchall()


async def adjust_master_balance(master_id: int, delta: float):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE masters SET balance = balance + ? WHERE id = ?", (delta, master_id)
        )
        await db.commit()


async def decrement_free_orders(master_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE masters SET free_orders_left = MAX(free_orders_left - 1, 0) WHERE id = ?",
            (master_id,),
        )
        await db.commit()


async def add_master_rating(master_id: int, stars: int):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute("SELECT rating, rating_count FROM masters WHERE id = ?", (master_id,))
        row = await cur.fetchone()
        if not row:
            return None
        new_count = row["rating_count"] + 1
        new_rating = (row["rating"] * row["rating_count"] + stars) / new_count
        new_rating = round(new_rating, 2)
        await db.execute(
            "UPDATE masters SET rating = ?, rating_count = ? WHERE id = ?",
            (new_rating, new_count, master_id),
        )
        await db.commit()
        return {"rating": new_rating, "rating_count": new_count}


async def create_review(order_id: int, from_role: str, stars: int, comment: str = None):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO reviews (order_id, from_role, stars, comment, created_at) "
            "VALUES (?, ?, ?, ?, ?)",
            (order_id, from_role, stars, comment, now()),
        )
        await db.commit()


async def get_master_reviews(master_id: int, limit: int = 3):
    """Ustaning eng so'nggi sharhlari (buyurtmalar orqali bog'langan)."""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute(
            """SELECT reviews.stars, reviews.comment, reviews.created_at
               FROM reviews
               JOIN orders ON orders.id = reviews.order_id
               WHERE orders.master_id = ? AND reviews.from_role = 'master'
               ORDER BY reviews.id DESC LIMIT ?""",
            (master_id, limit),
        )
        return await cur.fetchall()


async def set_master_status(master_id: int, status: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("UPDATE masters SET status = ? WHERE id = ?", (status, master_id))
        await db.commit()


async def add_customer_rating(customer_id: int, stars: int):
    """Ikki tomonlama baholash: usta mijozni baholaganda ishlatiladi."""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute("SELECT rating, rating_count FROM customers WHERE id = ?", (customer_id,))
        row = await cur.fetchone()
        if not row:
            return None
        new_count = row["rating_count"] + 1
        new_rating = round((row["rating"] * row["rating_count"] + stars) / new_count, 2)
        await db.execute(
            "UPDATE customers SET rating = ?, rating_count = ? WHERE id = ?",
            (new_rating, new_count, customer_id),
        )
        await db.commit()
        return {"rating": new_rating, "rating_count": new_count}


# ---------- CUSTOMERS ----------

async def create_customer(telegram_id: int, language: str = "uz", referred_by: int = None):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT OR IGNORE INTO customers (telegram_id, language, referred_by, created_at) "
            "VALUES (?, ?, ?, ?)",
            (telegram_id, language, referred_by, now()),
        )
        await db.commit()


async def mark_referral_bonus_given(customer_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE customers SET referral_bonus_given = 1 WHERE id = ?", (customer_id,)
        )
        await db.commit()


async def update_customer(telegram_id: int, **fields):
    if not fields:
        return
    keys = ", ".join(f"{k} = ?" for k in fields)
    values = list(fields.values()) + [telegram_id]
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(f"UPDATE customers SET {keys} WHERE telegram_id = ?", values)
        await db.commit()


async def get_customer(telegram_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute("SELECT * FROM customers WHERE telegram_id = ?", (telegram_id,))
        return await cur.fetchone()


async def get_customer_by_id(customer_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute("SELECT * FROM customers WHERE id = ?", (customer_id,))
        return await cur.fetchone()


async def get_all_customers():
    """Admin panel uchun — barcha ro'yxatdan o'tgan mijozlar."""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute("SELECT * FROM customers ORDER BY id DESC")
        return await cur.fetchall()


async def get_customer_orders(customer_id: int, limit: int = 15):
    """Mijozning o'z buyurtmalari (faol + tarix) — 'Mening buyurtmalarim' bo'limi uchun."""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute(
            "SELECT * FROM orders WHERE customer_id = ? ORDER BY id DESC LIMIT ?",
            (customer_id, limit),
        )
        return await cur.fetchall()


async def increment_customer_completed_orders(customer_id: int):
    """Mijozning yakunlangan buyurtmalar sonini oshiradi va yangi qiymatni qaytaradi."""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE customers SET completed_orders = completed_orders + 1 WHERE id = ?",
            (customer_id,),
        )
        await db.commit()
        db.row_factory = aiosqlite.Row
        cur = await db.execute("SELECT completed_orders FROM customers WHERE id = ?", (customer_id,))
        row = await cur.fetchone()
        return row["completed_orders"] if row else None


# ---------- ORDERS ----------

async def create_order(customer_id, service_type, description, latitude, longitude, address_text, phone):
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute(
            """INSERT INTO orders
               (customer_id, service_type, description, latitude, longitude,
                address_text, phone, status, created_at, updated_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, 'searching', ?, ?)""",
            (customer_id, service_type, description, latitude, longitude,
             address_text, phone, now(), now()),
        )
        await db.commit()
        return cur.lastrowid


async def get_order(order_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute("SELECT * FROM orders WHERE id = ?", (order_id,))
        return await cur.fetchone()


async def update_order(order_id: int, **fields):
    if not fields:
        return
    fields["updated_at"] = now()
    keys = ", ".join(f"{k} = ?" for k in fields)
    values = list(fields.values()) + [order_id]
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(f"UPDATE orders SET {keys} WHERE id = ?", values)
        await db.commit()


async def get_master_orders(master_id: int, statuses=None):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        if statuses:
            placeholders = ",".join("?" for _ in statuses)
            cur = await db.execute(
                f"SELECT * FROM orders WHERE master_id = ? AND status IN ({placeholders})",
                (master_id, *statuses),
            )
        else:
            cur = await db.execute("SELECT * FROM orders WHERE master_id = ?", (master_id,))
        return await cur.fetchall()


async def get_active_in_progress_order(master_id: int):
    """Ustaning hozirgi faol (bajarilayotgan) buyurtmasi — jonli joylashuvni yuborish uchun."""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute(
            "SELECT * FROM orders WHERE master_id = ? AND status = 'in_progress' ORDER BY id DESC LIMIT 1",
            (master_id,),
        )
        return await cur.fetchone()


_RELAYABLE_STATUSES = ("offered", "pricing", "offered_price", "in_progress")


async def get_customer_active_order(customer_id: int):
    """Mijozning hozir muzokara/bajarilish jarayonidagi buyurtmasi — anonim chat uchun."""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        placeholders = ",".join("?" for _ in _RELAYABLE_STATUSES)
        cur = await db.execute(
            f"SELECT * FROM orders WHERE customer_id = ? AND status IN ({placeholders}) "
            "ORDER BY id DESC LIMIT 1",
            (customer_id, *_RELAYABLE_STATUSES),
        )
        return await cur.fetchone()


async def get_master_active_order(master_id: int):
    """Ustaning hozir muzokara/bajarilish jarayonidagi buyurtmasi — anonim chat uchun."""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        placeholders = ",".join("?" for _ in _RELAYABLE_STATUSES)
        cur = await db.execute(
            f"SELECT * FROM orders WHERE master_id = ? AND status IN ({placeholders}) "
            "ORDER BY id DESC LIMIT 1",
            (master_id, *_RELAYABLE_STATUSES),
        )
        return await cur.fetchone()


async def increment_warranty_claims(order_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE orders SET warranty_claims_count = warranty_claims_count + 1 WHERE id = ?",
            (order_id,),
        )
        await db.commit()
        db.row_factory = aiosqlite.Row
        cur = await db.execute("SELECT warranty_claims_count FROM orders WHERE id = ?", (order_id,))
        row = await cur.fetchone()
        return row["warranty_claims_count"] if row else None


async def get_recent_orders(limit: int = 20):
    """Admin uchun — eng so'nggi buyurtmalar, eng yangi birinchi."""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute(
            "SELECT * FROM orders ORDER BY id DESC LIMIT ?", (limit,)
        )
        return await cur.fetchall()


async def get_active_orders():
    """Admin uchun — hozir faol (hali yakunlanmagan) barcha buyurtmalar."""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute(
            "SELECT * FROM orders WHERE status IN "
            "('offered','pricing','offered_price','in_progress') ORDER BY id DESC"
        )
        return await cur.fetchall()


async def count_orders_by_status():
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute(
            "SELECT status, COUNT(*) as cnt FROM orders GROUP BY status"
        )
        return await cur.fetchall()


# ---------- TOP-UP REQUESTS (balansni to'ldirish so'rovlari) ----------

async def create_topup_request(master_id: int, amount: float):
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute(
            """INSERT INTO topup_requests (master_id, amount, status, created_at, updated_at)
               VALUES (?, ?, 'requested', ?, ?)""",
            (master_id, amount, now(), now()),
        )
        await db.commit()
        return cur.lastrowid


async def get_topup_request(request_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute("SELECT * FROM topup_requests WHERE id = ?", (request_id,))
        return await cur.fetchone()


async def update_topup_request(request_id: int, **fields):
    if not fields:
        return
    fields["updated_at"] = now()
    keys = ", ".join(f"{k} = ?" for k in fields)
    values = list(fields.values()) + [request_id]
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(f"UPDATE topup_requests SET {keys} WHERE id = ?", values)
        await db.commit()


async def get_master_accepted_topup(master_id: int):
    """Ustaning to'lov skrinshoti kutilayotgan (admin qabul qilgan) so'rovi, agar bo'lsa."""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute(
            "SELECT * FROM topup_requests WHERE master_id = ? AND status = 'accepted' "
            "ORDER BY id DESC LIMIT 1",
            (master_id,),
        )
        return await cur.fetchone()
