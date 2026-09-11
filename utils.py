"""Yordamchi funksiyalar."""

from math import radians, sin, cos, sqrt, atan2


def haversine_km(lat1, lon1, lat2, lon2) -> float:
    """Ikki koordinata orasidagi masofani km da hisoblaydi."""
    if None in (lat1, lon1, lat2, lon2):
        return float("inf")
    R = 6371.0
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c


def sort_masters_by_distance_and_rating(masters, cust_lat, cust_lon):
    """
    Ustalarni masofa (asosiy) va reyting (teng masofada bo'lsa) bo'yicha saralaydi.
    Har bir usta uchun masofani hisoblab, ro'yxat qaytaradi:
    [(master_row, distance_km), ...]
    """
    enriched = []
    for m in masters:
        dist = haversine_km(cust_lat, cust_lon, m["latitude"], m["longitude"])
        enriched.append((m, dist))
    enriched.sort(key=lambda pair: (round(pair[1], 1), -pair[0]["rating"]))
    return enriched


async def notify_admins(bot, text: str, reply_markup=None):
    """Barcha adminlarga xabar yuborishga urinadi; admin botni bloklagan bo'lsa xatoni yutib yuboradi."""
    from config import ADMIN_IDS
    for admin_id in ADMIN_IDS:
        try:
            await bot.send_message(admin_id, text, reply_markup=reply_markup)
        except Exception:
            pass


def format_order_line(order) -> str:
    from config import SERVICE_TYPES
    status_labels = {
        "searching": "🔍 Qidirilmoqda",
        "offered": "📨 Ustaga yuborildi",
        "pricing": "💬 Narx kutilmoqda",
        "offered_price": "💰 Narx taklif qilindi",
        "in_progress": "🚗 Bajarilmoqda",
        "done": "✅ Bajarildi",
        "cancelled": "❌ Bekor qilindi",
    }
    price_text = f"{order['price']:.0f} so'm" if order["price"] else "—"
    return (
        f"#{order['id']} | {SERVICE_TYPES.get(order['service_type'], order['service_type'])} | "
        f"{status_labels.get(order['status'], order['status'])} | {price_text}"
    )


def format_master_line(m) -> str:
    from config import SERVICE_TYPES
    status_labels = {
        "pending": "⏳ Kutilmoqda",
        "verified": "✅ Tasdiqlangan",
        "rejected": "❌ Rad etilgan",
        "blocked": "🚫 Bloklangan",
    }
    busy_text = "🔴 Band" if m["is_busy"] else "🟢 Bo'sh"
    extra = f", zaxira: {m['extra_phone']}" if m["extra_phone"] else ""
    age_exp = f" | {m['age'] or '—'} yosh, {m['experience_years'] or '—'} tajriba"
    return (
        f"#{m['id']} | {m['full_name']} | {m['phone']}{extra} | "
        f"{SERVICE_TYPES.get(m['service_type'], m['service_type'])}{age_exp} | "
        f"{status_labels.get(m['status'], m['status'])} | {busy_text} | "
        f"⭐{m['rating']:.1f} | 💰{m['balance']:.0f} so'm"
    )


def format_customer_line(c) -> str:
    return (
        f"#{c['id']} | {c['full_name'] or '(ism kiritilmagan)'} | "
        f"{c['phone'] or '(telefon yo`q)'} | ⭐{c['rating']:.1f}"
    )
