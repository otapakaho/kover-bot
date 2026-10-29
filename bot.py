import os
import random
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

# ==== НАСТРОЙКИ ====
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "8880712933:AAHMWKpLPPmUH6Kekfvn3s4DZa6J0GoHTWM")

# ==== НАСТРОЙКИ ПОДПИСКИ ====
CHANNEL_USERNAME = "@chillaviaa"          # замени на username канала, с @
CHANNEL_URL = "https://t.me/chillaviaa"   # замени на ссылку на канал

# ==== БАЗА АЭРОПОРТОВ ====
AIRPORTS = {
    "KLF": {"name": "Калуга (Грабцево)", "city": "Калуга", "chance": 1.00},
    "GDZ": {"name": "Геленджик", "city": "Геленджик", "chance": 0.72},
    "AER": {"name": "Сочи (Адлер)", "city": "Сочи", "chance": 0.52},
    "GSV": {"name": "Саратов (Гагарин)", "city": "Саратов", "chance": 0.50},
    "PEZ": {"name": "Пенза", "city": "Пенза", "chance": 0.50},
    "VKO": {"name": "Москва (Внуково)", "city": "Москва", "chance": 0.42},
    "DME": {"name": "Москва (Домодедово)", "city": "Москва", "chance": 0.38},
    "KUF": {"name": "Самара (Курумоч)", "city": "Самара", "chance": 0.33},
    "SVO": {"name": "Москва (Шереметьево)", "city": "Москва", "chance": 0.20},
    "UFA": {"name": "Уфа", "city": "Уфа", "chance": 0.19},
    "SKX": {"name": "Саранск", "city": "Саранск", "chance": 0.16},
    "IJK": {"name": "Ижевск", "city": "Ижевск", "chance": 0.15},
    "ZIA": {"name": "Жуковский (Раменское)", "city": "Жуковский", "chance": 0.36},
    "KZN": {"name": "Казань", "city": "Казань", "chance": 0.35},
    "ULV": {"name": "Ульяновск (Баратаевка)", "city": "Ульяновск", "chance": 0.35},
    "GOJ": {"name": "Нижний Новгород (Чкалов)", "city": "Нижний Новгород", "chance": 0.34},
    "NBC": {"name": "Нижнекамск (Бегишево)", "city": "Нижнекамск", "chance": 0.31},
    "KRR": {"name": "Краснодар (Пашковский)", "city": "Краснодар", "chance": 0.30},
    "UUA": {"name": "Бугульма", "city": "Бугульма", "chance": 0.29},
    "IAR": {"name": "Ярославль (Туношна)", "city": "Ярославль", "chance": 0.29},
    "CSY": {"name": "Чебоксары", "city": "Чебоксары", "chance": 0.28},
    "TBW": {"name": "Тамбов (Донское)", "city": "Тамбов", "chance": 0.27},
    "PEE": {"name": "Пермь (Большое Савино)", "city": "Пермь", "chance": 0.19},
    "REN": {"name": "Оренбург", "city": "Оренбург", "chance": 0.17},
    "KVX": {"name": "Киров (Победилово)", "city": "Киров", "chance": 0.16},
    "VOG": {"name": "Волгоград (Гумрак)", "city": "Волгоград", "chance": 0.15},
    "SVX": {"name": "Екатеринбург (Кольцово)", "city": "Екатеринбург", "chance": 0.11},
    "CEE": {"name": "Череповец", "city": "Череповец", "chance": 0.10},
    "MCX": {"name": "Махачкала (Уйташ)", "city": "Махачкала", "chance": 0.09},
    "PKV": {"name": "Псков", "city": "Псков", "chance": 0.09},
    "LED": {"name": "Санкт-Петербург (Пулково)", "city": "Санкт-Петербург", "chance": 0.08},
    "IWA": {"name": "Иваново (Южный)", "city": "Иваново", "chance": 0.07},
    "KMW": {"name": "Кострома (Сокеркино)", "city": "Кострома", "chance": 0.05},
    "TJM": {"name": "Тюмень (Рощино)", "city": "Тюмень", "chance": 0.05},
    "OSW": {"name": "Орск", "city": "Орск", "chance": 0.05},
    "CEK": {"name": "Челябинск (Баландино)", "city": "Челябинск", "chance": 0.05},
    "OMS": {"name": "Омск (Центральный)", "city": "Омск", "chance": 0.04},
    "SGC": {"name": "Сургут", "city": "Сургут", "chance": 0.04},
    "GRV": {"name": "Грозный (Северный)", "city": "Грозный", "chance": 0.03},
    "KRO": {"name": "Курган", "city": "Курган", "chance": 0.03},
    "OVS": {"name": "Советский", "city": "Советский", "chance": 0.03},
    "URJ": {"name": "Урай", "city": "Урай", "chance": 0.03},
    "UCT": {"name": "Ухта", "city": "Ухта", "chance": 0.03},
    "ASF": {"name": "Астрахань (Нариманово)", "city": "Астрахань", "chance": 0.02},
    "OGZ": {"name": "Владикавказ (Беслан)", "city": "Владикавказ", "chance": 0.02},
    "KSZ": {"name": "Котлас", "city": "Котлас", "chance": 0.02},
    "MQF": {"name": "Магнитогорск", "city": "Магнитогорск", "chance": 0.02},
    "SCW": {"name": "Сыктывкар", "city": "Сыктывкар", "chance": 0.02},
    "TOX": {"name": "Тобольск (Ремезов)", "city": "Тобольск", "chance": 0.02},
    "HMA": {"name": "Ханты-Мансийск", "city": "Ханты-Мансийск", "chance": 0.02},
    "VUS": {"name": "Великий Устюг", "city": "Великий Устюг", "chance": 0.003},
    "NYM": {"name": "Надым", "city": "Надым", "chance": 0.003},
    "NYA": {"name": "Нягань", "city": "Нягань", "chance": 0.003},
    "SBT": {"name": "Сабетта", "city": "Сабетта", "chance": 0.003},
    "ARH": {"name": "Архангельск (Талаги)", "city": "Архангельск", "chance": 0.003},
    "BVJ": {"name": "Бованенково", "city": "Бованенково", "chance": 0.003},
    "IRM": {"name": "Игрим", "city": "Игрим", "chance": 0.003},
    "NUX": {"name": "Новый Уренгой", "city": "Новый Уренгой", "chance": 0.003},
    "PES": {"name": "Петрозаводск", "city": "Петрозаводск", "chance": 0.003},
    "STW": {"name": "Ставрополь (Шпаковское)", "city": "Ставрополь", "chance": 0.003},
    "VLG": {"name": "Вологда", "city": "Вологда", "chance": 0.003},
    "KGD": {"name": "Калининград (Храброво)", "city": "Калининград", "chance": 0.003},
    "IGT": {"name": "Магас", "city": "Магас", "chance": 0.003},
    "MRV": {"name": "Минеральные Воды", "city": "Минеральные Воды", "chance": 0.003},
    "MMK": {"name": "Мурманск", "city": "Мурманск", "chance": 0.003},
    "NAL": {"name": "Нальчик", "city": "Нальчик", "chance": 0.003},
    "OVB": {"name": "Новосибирск (Толмачёво)", "city": "Новосибирск", "chance": 0.003},
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
    """Проверяет, подписан ли пользователь на канал."""
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
    """Кнопки «Подписаться» и «Я подписался»."""
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📢 Подписаться", url=CHANNEL_URL)],
        [InlineKeyboardButton("✅ Я подписался", callback_data="check_sub")]
    ])


async def require_subscription(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Возвращает True, если подписан. Если нет — отправляет сообщение и False."""
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
        f"🎰 *Рулетка: {title}* (`{code}`)\n\n"
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
        "• /roll SVO — крутить по коду IATA\n"
        "• /find Москва — найти по городу\n"
        "• /random — случайный аэропорт\n"
        "• /top — топ-10 самых «ковровых»"
    )
    await update.message.reply_text(text, parse_mode="Markdown")


async def find(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await require_subscription(update, context):
        return

    if not context.args:
        await update.message.reply_text(
            "Напиши город или часть названия, например: `/find Москва`",
            parse_mode="Markdown",
        )
        return

    query = " ".join(context.args).lower()
    matches = [
        (code, info) for code, info in AIRPORTS.items()
        if query in info["name"].lower() or query in info["city"].lower()
    ]

    if not matches:
        await update.message.reply_text(f"🤷 Ничего не нашёл по «{query}».")
        return

    matches = matches[:30]
    lines = [f"📍 Найдено ({len(matches)}):\n"]
    for code, info in matches:
        lines.append(f"`{code}` {info['name']}")
    lines.append("\nПример: `/roll " + matches[0][0] + "`")
    await update.message.reply_text("\n".join(lines), parse_mode="Markdown")


async def roll(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await require_subscription(update, context):
        return

    if not context.args:
        await update.message.reply_text(
            "Укажи код IATA, например: `/roll SVO`\n"
            "Или найди по городу: `/find Москва`",
            parse_mode="Markdown",
        )
        return

    code = context.args[0].upper()
    if code not in AIRPORTS:
        await update.message.reply_text(
            f"🤷 Не знаю аэропорт `{code}`. Попробуй `/find <город>`",
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


async def on_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data or ""

    # Кнопка «Я подписался»
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

    # Кнопки переброса
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
    app.add_handler(CallbackQueryHandler(on_button))

    print("Бот запущен. Ctrl+C для остановки.")
    app.run_polling()


if __name__ == "__main__":
    main()
