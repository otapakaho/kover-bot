import os
import random
import logging
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    KeyboardButton,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

# ==== НАСТРОЙКИ ====
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "8880712933:AAHMWKpLPPmUH6Kekfvn3s4DZa6J0GoHTWM")

# ==== НАСТРОЙКИ ПОДПИСКИ ====
CHANNEL_USERNAME = "@chillaviaa"          # замени на username канала, с @
CHANNEL_URL = "https://t.me/chillaviaa"   # замени на ссылку на канал

# ==== БАЗА АЭРОПОРТОВ ====
AIRPORTS = {
    "KLF": {"name": "Калуга (Грабцево)", "city": "Калуга", "icao": "UUBC", "chance": 1.00},
    "GDZ": {"name": "Геленджик", "city": "Геленджик", "icao": "URKG", "chance": 0.72},
    "AER": {"name": "Сочи (Адлер)", "city": "Сочи", "icao": "URSS", "chance": 0.52},
    "GSV": {"name": "Саратов (Гагарин)", "city": "Саратов", "icao": "UWSG", "chance": 0.50},
    "PEZ": {"name": "Пенза", "city": "Пенза", "icao": "UWPP", "chance": 0.50},
    "VKO": {"name": "Москва (Внуково)", "city": "Москва", "icao": "UUWW", "chance": 0.42},
    "DME": {"name": "Москва (Домодедово)", "city": "Москва", "icao": "UUDD", "chance": 0.38},
    "KUF": {"name": "Самара (Курумоч)", "city": "Самара", "icao": "UWWW", "chance": 0.33},
    "SVO": {"name": "Москва (Шереметьево)", "city": "Москва", "icao": "UUEE", "chance": 0.20},
    "UFA": {"name": "Уфа", "city": "Уфа", "icao": "UWUU", "chance": 0.19},
    "SKX": {"name": "Саранск", "city": "Саранск", "icao": "UWPS", "chance": 0.16},
    "IJK": {"name": "Ижевск", "city": "Ижевск", "icao": "USII", "chance": 0.15},
    "ZIA": {"name": "Жуковский (Раменское)", "city": "Жуковский", "icao": "UUBW", "chance": 0.36},
    "KZN": {"name": "Казань", "city": "Казань", "icao": "UWKD", "chance": 0.35},
    "ULV": {"name": "Ульяновск (Баратаевка)", "city": "Ульяновск", "icao": "UWLL", "chance": 0.35},
    "GOJ": {"name": "Нижний Новгород (Чкалов)", "city": "Нижний Новгород", "icao": "UWGG", "chance": 0.34},
    "NBC": {"name": "Нижнекамск (Бегишево)", "city": "Нижнекамск", "icao": "UWKE", "chance": 0.31},
    "KRR": {"name": "Краснодар (Пашковский)", "city": "Краснодар", "icao": "URKK", "chance": 0.30},
    "UUA": {"name": "Бугульма", "city": "Бугульма", "icao": "UWKB", "chance": 0.29},
    "IAR": {"name": "Ярославль (Туношна)", "city": "Ярославль", "icao": "UUDL", "chance": 0.29},
    "CSY": {"name": "Чебоксары", "city": "Чебоксары", "icao": "UWKS", "chance": 0.28},
    "TBW": {"name": "Тамбов (Донское)", "city": "Тамбов", "icao": "UUOT", "chance": 0.27},
    "PEE": {"name": "Пермь (Большое Савино)", "city": "Пермь", "icao": "USPP", "chance": 0.19},
    "REN": {"name": "Оренбург", "city": "Оренбург", "icao": "UWOO", "chance": 0.17},
    "KVX": {"name": "Киров (Победилово)", "city": "Киров", "icao": "USKK", "chance": 0.16},
    "VOG": {"name": "Волгоград (Гумрак)", "city": "Волгоград", "icao": "URWW", "chance": 0.15},
    "SVX": {"name": "Екатеринбург (Кольцово)", "city": "Екатеринбург", "icao": "USSS", "chance": 0.11},
    "CEE": {"name": "Череповец", "city": "Череповец", "icao": "ULWC", "chance": 0.10},
    "MCX": {"name": "Махачкала (Уйташ)", "city": "Махачкала", "icao": "URML", "chance": 0.09},
    "PKV": {"name": "Псков", "city": "Псков", "icao": "ULOO", "chance": 0.09},
    "LED": {"name": "Санкт-Петербург (Пулково)", "city": "Санкт-Петербург", "icao": "ULLI", "chance": 0.08},
    "IWA": {"name": "Иваново (Южный)", "city": "Иваново", "icao": "UUBI", "chance": 0.07},
    "KMW": {"name": "Кострома (Сокеркино)", "city": "Кострома", "icao": "UUBD", "chance": 0.05},
    "TJM": {"name": "Тюмень (Рощино)", "city": "Тюмень", "icao": "USTR", "chance": 0.05},
    "OSW": {"name": "Орск", "city": "Орск", "icao": "UWOR", "chance": 0.05},
    "CEK": {"name": "Челябинск (Баландино)", "city": "Челябинск", "icao": "USCC", "chance": 0.05},
    "OMS": {"name": "Омск (Центральный)", "city": "Омск", "icao": "UNOO", "chance": 0.04},
    "SGC": {"name": "Сургут", "city": "Сургут", "icao": "USRR", "chance": 0.04},
    "GRV": {"name": "Грозный (Северный)", "city": "Грозный", "icao": "URMG", "chance": 0.03},
    "KRO": {"name": "Курган", "city": "Курган", "icao": "USUU", "chance": 0.03},
    "OVS": {"name": "Советский", "city": "Советский", "icao": "USHS", "chance": 0.03},
    "URJ": {"name": "Урай", "city": "Урай", "icao": "USHU", "chance": 0.03},
    "UCT": {"name": "Ухта", "city": "Ухта", "icao": "UUYH", "chance": 0.03},
    "ASF": {"name": "Астрахань (Нариманово)", "city": "Астрахань", "icao": "URWA", "chance": 0.02},
    "OGZ": {"name": "Владикавказ (Беслан)", "city": "Владикавказ", "icao": "URMO", "chance": 0.02},
    "KSZ": {"name": "Котлас", "city": "Котлас", "icao": "ULKK", "chance": 0.02},
    "MQF": {"name": "Магнитогорск", "city": "Магнитогорск", "icao": "USCM", "chance": 0.02},
    "SCW": {"name": "Сыктывкар", "city": "Сыктывкар", "icao": "UUYY", "chance": 0.02},
    "TOX": {"name": "Тобольск (Ремезов)", "city": "Тобольск", "icao": "USTO", "chance": 0.02},
    "HMA": {"name": "Ханты-Мансийск", "city": "Ханты-Мансийск", "icao": "USHH", "chance": 0.02},
    "VUS": {"name": "Великий Устюг", "city": "Великий Устюг", "icao": "ULWU", "chance": 0.003},
    "NYM": {"name": "Надым", "city": "Надым", "icao": "USMM", "chance": 0.003},
    "NYA": {"name": "Нягань", "city": "Нягань", "icao": "USHN", "chance": 0.003},
    "SBT": {"name": "Сабетта", "city": "Сабетта", "icao": "USDA", "chance": 0.003},
    "ARH": {"name": "Архангельск (Талаги)", "city": "Архангельск", "icao": "ULAA", "chance": 0.003},
    "BVJ": {"name": "Бованенково", "city": "Бованенково", "icao": "USDB", "chance": 0.003},
    "IRM": {"name": "Игрим", "city": "Игрим", "icao": "USHI", "chance": 0.003},
    "NUX": {"name": "Новый Уренгой", "city": "Новый Уренгой", "icao": "USMU", "chance": 0.003},
    "PES": {"name": "Петрозаводск", "city": "Петрозаводск", "icao": "ULPB", "chance": 0.003},
    "STW": {"name": "Ставрополь (Шпаковское)", "city": "Ставрополь", "icao": "URMT", "chance": 0.003},
    "VLG": {"name": "Вологда", "city": "Вологда", "icao": "ULWW", "chance": 0.003},
    "KGD": {"name": "Калининград (Храброво)", "city": "Калининград", "icao": "UMKK", "chance": 0.003},
    "IGT": {"name": "Магас", "city": "Магас", "icao": "URMS", "chance": 0.003},
    "MRV": {"name": "Минеральные Воды", "city": "Минеральные Воды", "icao": "URMM", "chance": 0.003},
    "MMK": {"name": "Мурманск", "city": "Мурманск", "icao": "ULMM", "chance": 0.003},
    "NAL": {"name": "Нальчик", "city": "Нальчик", "icao": "URMN", "chance": 0.003},
    "OVB": {"name": "Новосибирск (Толмачёво)", "city": "Новосибирск", "icao": "UNNT", "chance": 0.003},
}

# ==== ФРАЗЫ ====
FLY_PHRASES = [
    "🛫 Улёт разрешён! Экипаж уже греет двигатели.",
    "✅ Борт подан. Счастливого пути!",
    "🛫 Небо сегодня благосклонно. Взлетаем!",
    "✈️ Полоса свободна, диспетчер в хорошем настроении.",
    "🛫 Всё чисто. Даже чай в термосе не расплещется.",
]

COVER_PHRASES = [
    "🟥 РЕЖИМ «КОВЁР»! Все по домам, небо закрыто.",
    "🚫 «Ковёр» объявлен. Самолётики стоят, чайки гуляют.",
    "🟥 Ковёр! Диспетчер ушёл пить чай и не вернулся.",
    "🚫 Не сегодня. Планёр «Ковёр» разложен на всё небо.",
    "🟥 Взлёт отменён. Виноват кто-то важный, но не мы.",
]

UNCERTAIN_PHRASES = [
    "🤔 Неопределённость. То ли полетим, то ли нет — как повезёт.",
    "🌫 Туман неясности. Ждём у моря погоды.",
    "🟨 «Ковёр» на паузе. Все смотрят в небо и гадают.",
    "🎲 50 на 50. Можно попробовать ещё раз.",
]


# ==== ПРОВЕРКА ПОДПИСКИ ====
async def is_subscribed(context: ContextTypes.DEFAULT_TYPE, user_id: int) -> bool:
    try:
        member = await context.bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return member.status in ["member", "administrator", "creator", "restricted"]
    except Exception as e:
        error_text = str(e)
        if "User not found" in error_text:
            print(f"Пользователь {user_id} не запускал бота — нужен /start")
            return False
        print(f"Ошибка проверки подписки: {e}")
        return False


def subscription_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📢 Подписаться", url=CHANNEL_URL)],
        [InlineKeyboardButton("✅ Я подписался", callback_data="check_sub")]
    ])


async def require_subscription(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    user_id = update.effective_user.id
    if await is_subscribed(context, user_id):
        return True

    msg = (
        "🔒 *Доступ только для подписчиков!*\n\n"
        f"Чтобы крутить рулетку, подпишись на канал: {CHANNEL_USERNAME}\n"
        "После подписки нажми «Я подписался»."
    )

    if update.callback_query:
        await update.callback_query.edit_message_text(
            msg, parse_mode="Markdown", reply_markup=subscription_keyboard()
        )
    else:
        await update.message.reply_text(
            msg, parse_mode="Markdown", reply_markup=subscription_keyboard()
        )
    return False


def main_menu_keyboard():
    keyboard = [
        [KeyboardButton("🎲 Крутить"), KeyboardButton("🔀 Случайный")],
        [KeyboardButton("📊 Топ-10"), KeyboardButton("🔍 Найти")],
        [KeyboardButton("🎯 Ставка"), KeyboardButton("ℹ️ Помощь")],
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


# ==== ЛОГИКА РУЛЕТКИ ====
def roll_verdict(base_cover_chance: float):
    cover_chance = base_cover_chance + random.uniform(-0.10, 0.10)
    cover_chance = max(0.001, min(0.99, cover_chance))
    fly_chance = 1 - cover_chance

    r = random.random()
    if r < cover_chance:
        outcome = "cover"
    elif r < cover_chance + 0.10:
        outcome = "uncertain"
    else:
        outcome = "fly"

    return round(fly_chance * 100, 1), round(cover_chance * 100, 1), outcome


def bar(p: float) -> str:
    filled = int(p / 10)
    return "█" * filled + "░" * (10 - filled)


def find_airport_by_code(query: str):
    q = query.strip().upper()
    if q in AIRPORTS:
        return q, AIRPORTS[q]
    for iata, info in AIRPORTS.items():
        if info.get("icao", "").upper() == q:
            return iata, info
    return None, None


def build_roll_text(code: str):
    info = AIRPORTS[code]
    fly, cover, outcome = roll_verdict(info["chance"])

    if outcome == "fly":
        phrase = random.choice(FLY_PHRASES)
    elif outcome == "cover":
        phrase = random.choice(COVER_PHRASES)
    else:
        phrase = random.choice(UNCERTAIN_PHRASES)

    title = info["name"]

    text = (
        f"🎰 *Рулетка: {title}* (`{code}` / `{info.get('icao', '—')}`)\n\n"
        f"{phrase}\n\n"
        f"🛫 Шанс улёта: *{fly}%*\n`{bar(fly)}`\n\n"
        f"🟥 Шанс «Ковра»: *{cover}%*\n`{bar(cover)}`\n\n"
        f"_…это шутка, конечно._"
    )

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🎲 Крутить ещё раз", callback_data=f"reroll:{code}"),
            InlineKeyboardButton("🔀 Случайный", callback_data="reroll:RANDOM"),
        ]
    ])
    return text, keyboard


# ==== ОБРАБОТЧИКИ ====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "🎰 *Ковёр-рулетка* 🎰\n\n"
        f"В базе: *{len(AIRPORTS)}* аэропортов России.\n"
        "Шансы рассчитаны по реальной статистике закрытий "
        "(skymoments.ru, за 90 дней).\n\n"
        "Это *шутка*, но цифры настоящие.\n\n"
        "Команды:\n"
        "• /roll SVO или /roll UUEE — крутить по IATA или ICAO\n"
        "• /find Москва — найти по городу\n"
        "• /random — случайный аэропорт\n"
        "• /top — топ-10 самых «ковровых»\n"
        "• /bet ковёр — сделать ставку\n\n"
        "Или просто пользуйся кнопками внизу 👇"
    )
    await update.message.reply_text(
        text, parse_mode="Markdown", reply_markup=main_menu_keyboard()
    )


async def find(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await require_subscription(update, context):
        return

    if not context.args:
        await update.message.reply_text(
            "Напиши код IATA, ICAO, город или часть названия.\n"
            "Например: `SVO`, `UUEE` или `Москва`",
            parse_mode="Markdown",
        )
        return

    query = " ".join(context.args).strip()
    query_lower = query.lower()
    query_upper = query.upper()

    matches = []
    for code, info in AIRPORTS.items():
        if query_upper == code:
            matches.append((code, info))
            continue
        if info.get("icao", "").upper() == query_upper:
            matches.append((code, info))
            continue
        if query_lower in info["name"].lower() or query_lower in info["city"].lower():
            matches.append((code, info))

    if not matches:
        await update.message.reply_text(f"🤷 Ничего не нашёл по «{query}».")
        return

    matches = matches[:30]
    lines = [f"📍 Найдено ({len(matches)}):\n"]
    for code, info in matches:
        lines.append(f"`{code}` / `{info.get('icao', '—')}` — {info['name']}")
    lines.append("\nПример: `/roll " + matches[0][0] + "`")
    await update.message.reply_text("\n".join(lines), parse_mode="Markdown")


async def roll(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await require_subscription(update, context):
        return

    if not context.args:
        await update.message.reply_text(
            "Укажи код IATA или ICAO, например: `/roll SVO` или `/roll UUEE`\n"
            "Или найди по городу: `/find Москва`",
            parse_mode="Markdown",
        )
        return

    raw = context.args[0]
    code, info = find_airport_by_code(raw)
    if code is None:
        await update.message.reply_text(
            f"🤷 Не знаю аэропорт `{raw}`. Попробуй `/find <город>`",
            parse_mode="Markdown",
        )
        return

    text, keyboard = build_roll_text(code)
    await update.message.reply_text(
        text, parse_mode="Markdown", reply_markup=keyboard
    )


async def random_airport(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await require_subscription(update, context):
        return

    code = random.choice(list(AIRPORTS.keys()))
    text, keyboard = build_roll_text(code)
    await update.message.reply_text(
        text, parse_mode="Markdown", reply_markup=keyboard
    )


async def top(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await require_subscription(update, context):
        return

    ranked = sorted(
        AIRPORTS.items(), key=lambda kv: kv[1]["chance"], reverse=True
    )[:10]

    lines = ["🏆 *Топ-10 самых «ковровых» аэропортов России*\n"]
    medals = ["🥇", "🥈", "🥉"]
    for i, (code, info) in enumerate(ranked, start=1):
        prefix = medals[i - 1] if i <= 3 else f"{i}."
        pct = round(info["chance"] * 100, 1)
        lines.append(f"{prefix} `{code}` {info['name']} — *{pct}%*")
    lines.append(
        "\n_Данные: skymoments.ru (Росавиация, за 90 дней). Это шутка._"
    )
    await update.message.reply_text("\n".join(lines), parse_mode="Markdown")


async def bet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await require_subscription(update, context):
        return

    if not context.args:
        await update.message.reply_text(
            "🎲 *Ставка на «Ковёр»*\n\n"
            "Синтаксис:\n"
            "• `/bet ковёр` — ставка на «Ковёр» (случайный аэропорт)\n"
            "• `/bet улёт` — ставка на «Улёт»\n"
            "• `/bet ковёр SVO` — ставка на конкретный аэропорт\n\n"
            "Если выпадет «непонятно» — ничья.",
            parse_mode="Markdown",
        )
        return

    bet_raw = context.args[0].lower()
    if bet_raw in ["ковёр", "ковер", "ковра", "cover"]:
        user_bet = "cover"
    elif bet_raw in ["улёт", "улет", "fly"]:
        user_bet = "fly"
    else:
        await update.message.reply_text(
            "🤔 Не понял ставку. Напиши `ковёр` или `улёт`.\n"
            "Пример: `/bet ковёр SVO`",
            parse_mode="Markdown",
        )
        return

    if len(context.args) >= 2:
        raw = context.args[1]
        code, _ = find_airport_by_code(raw)
        if code is None:
            await update.message.reply_text(
                f"🤷 Не знаю аэропорт `{raw}`. Попробуй `/find <город>`",
                parse_mode="Markdown",
            )
            return
    else:
        code = random.choice(list(AIRPORTS.keys()))

    info = AIRPORTS[code]
    fly, cover, outcome = roll_verdict(info["chance"])

    if outcome == "fly":
        actual = "fly"
        result_text = "✈️ *Улёт!*"
    elif outcome == "cover":
        actual = "cover"
        result_text = "🟥 *Ковёр!*"
    else:
        actual = "uncertain"
        result_text = "🤔 *Непонятно...* (ничья)"

    if actual == "uncertain":
        verdict = "🤝 Ничья. Не угадал и не проиграл."
    elif user_bet == actual:
        verdict = "🎉 *Ты угадал!*"
    else:
        verdict = "😢 *Не угадал.*"

    bet_name = "«Ковёр»" if user_bet == "cover" else "«Улёт»"

    text = (
        f"🎲 *Ставка:* {bet_name}\n"
        f"📍 *Аэропорт:* {info['name']} (`{code}`)\n\n"
        f"Крутим...\n\n"
        f"{result_text}\n"
        f"🛫 Шанс улёта: *{fly}%* | 🟥 Шанс «Ковра»: *{cover}%*\n\n"
        f"{verdict}"
    )

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🎲 Ещё ставка", callback_data=f"bet_again:{user_bet}"),
            InlineKeyboardButton("🔀 Случайный", callback_data="reroll:RANDOM"),
        ]
    ])

    await update.message.reply_text(
        text, parse_mode="Markdown", reply_markup=keyboard
    )


async def menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "🎲 Крутить":
        await update.message.reply_text(
            "Напиши код аэропорта (IATA или ICAO), например: `SVO` или `UUEE`\n"
            "Или нажми /random для случайного.",
            parse_mode="Markdown",
            reply_markup=main_menu_keyboard(),
        )
        context.user_data["awaiting_airport"] = True
        return

    if text == "🔀 Случайный":
        await random_airport(update, context)
        return

    if text == "📊 Топ-10":
        await top(update, context)
        return

    if text == "🔍 Найти":
        await update.message.reply_text(
            "Напиши город или часть названия, например: `Москва`",
            parse_mode="Markdown",
            reply_markup=main_menu_keyboard(),
        )
        context.user_data["awaiting_find"] = True
        return

    if text == "🎯 Ставка":
        await update.message.reply_text(
            "Сделай ставку:\n"
            "• `ковёр` — на «Ковёр»\n"
            "• `улёт` — на «Улёт»\n\n"
            "Можно добавить код аэропорта: `ковёр SVO`",
            parse_mode="Markdown",
            reply_markup=main_menu_keyboard(),
        )
        context.user_data["awaiting_bet"] = True
        return

    if text == "ℹ️ Помощь":
        await start(update, context)
        return

    if context.user_data.get("awaiting_airport"):
        context.user_data["awaiting_airport"] = False
        context.args = [text]
        await roll(update, context)
        return

    if context.user_data.get("awaiting_find"):
        context.user_data["awaiting_find"] = False
        context.args = text.split()
        await find(update, context)
        return

    if context.user_data.get("awaiting_bet"):
        context.user_data["awaiting_bet"] = False
        context.args = text.split()
        await bet(update, context)
        return


async def on_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data or ""

    if data == "check_sub":
        user_id = query.from_user.id
        try:
            member = await context.bot.get_chat_member(CHANNEL_USERNAME, user_id)
            is_member = member.status in ["member", "administrator", "creator", "restricted"]
        except Exception as e:
            if "User not found" in str(e):
                await query.answer(
                    "Сначала нажми /start в этом боте, а потом проверяй подписку.",
                    show_alert=True
                )
                return
            is_member = False

        if is_member:
            await query.edit_message_text(
                "✅ Спасибо за подписку! Теперь можешь крутить рулетку.\n"
                "Отправь /roll SVO или нажми /random."
            )
        else:
            await query.answer("❌ Ты ещё не подписался. Попробуй ещё раз.", show_alert=True)
        return

    if data.startswith("bet_again:"):
        if not await require_subscription(update, context):
            return
        user_bet = data.split(":", 1)[1]
        code = random.choice(list(AIRPORTS.keys()))
        info = AIRPORTS[code]
        fly, cover, outcome = roll_verdict(info["chance"])

        if outcome == "fly":
            actual = "fly"
            result_text = "✈️ *Улёт!*"
        elif outcome == "cover":
            actual = "cover"
            result_text = "🟥 *Ковёр!*"
        else:
            actual = "uncertain"
            result_text = "🤔 *Непонятно...* (ничья)"

        if actual == "uncertain":
            verdict = "🤝 Ничья."
        elif user_bet == actual:
            verdict = "🎉 *Ты угадал!*"
        else:
            verdict = "😢 *Не угадал.*"

        bet_name = "«Ковёр»" if user_bet == "cover" else "«Улёт»"
        text = (
            f"🎲 *Ставка:* {bet_name}\n"
            f"📍 *Аэропорт:* {info['name']} (`{code}`)\n\n"
            f"{result_text}\n"
            f"🛫 Шанс улёта: *{fly}%* | 🟥 Шанс «Ковра»: *{cover}%*\n\n"
            f"{verdict}"
        )
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("🎲 Ещё ставка", callback_data=f"bet_again:{user_bet}"),
                InlineKeyboardButton("🔀 Случайный", callback_data="reroll:RANDOM"),
            ]
        ])
        await query.edit_message_text(
            text, parse_mode="Markdown", reply_markup=keyboard
        )
        return

    if not data.startswith("reroll:"):
        return

    if not await require_subscription(update, context):
        return

    code = data.split(":", 1)[1]
    if code == "RANDOM":
        code = random.choice(list(AIRPORTS.keys()))

    if code not in AIRPORTS:
        await query.edit_message_text("🤷 Аэропорт потерялся. Попробуй ещё раз.")
        return

    text, keyboard = build_roll_text(code)
    await query.edit_message_text(
        text, parse_mode="Markdown", reply_markup=keyboard
    )


def main():
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", start))
    app.add_handler(CommandHandler("find", find))
    app.add_handler(CommandHandler("roll", roll))
    app.add_handler(CommandHandler("random", random_airport))
    app.add_handler(CommandHandler("top", top))
    app.add_handler(CommandHandler("bet", bet))
    app.add_handler(CallbackQueryHandler(on_button))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, menu_handler))

    print("Бот запущен. Ctrl+C для остановки.")
    app.run_polling()


if __name__ == "__main__":
    main()
