import logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Настройки
TOKEN = "7189567503:AAGv-4sZSIfX_nwvaz0NMxrB5lC8Si8ndUs"
ADMIN_USERNAME = "@Xsfvbdd"
ADMIN_ID = 6862660218

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Данные о подписках
SUBSCRIPTIONS = {
    "all": {
        "name": "🔥 ВСЕ ЮЗЕРНЕЙМЫ",
        "price": 830,
        "desc": "Полный доступ ко всем юзернеймам из базы"
    },
    "month": {
        "name": "⏳ ПОДПИСКА НА МЕСЯЦ", 
        "price": 415,
        "desc": "Доступ к новым юзернеймам в течение 30 дней"
    },
    "numbers": {
        "name": "📞 ВСЕ НОМЕРА",
        "price": 830,
        "desc": "Полная база номеров телефонов"
    },
    "five": {
        "name": "5️⃣ 5 ЮЗЕРНЕЙМОВ",
        "price": 42,
        "desc": "5 юзернеймов на выбор"
    },
    "twenty": {
        "name": "2️⃣0️⃣ 20 ЮЗЕРНЕЙМОВ",
        "price": 166,
        "desc": "20 юзернеймов на выбор (выбор в ЛС)"
    }
}

# Клавиатуры
def main_menu():
    return ReplyKeyboardMarkup(
        [
            ["💎 ПОДКЛЮЧИТЬ ПОДПИСКУ"],
            ["ℹ️ ИНФОРМАЦИЯ", "🕘 ПОДДЕРЖКА (9:00-21:00)"],
            ["🔙 ГЛАВНОЕ МЕНЮ"]
        ],
        resize_keyboard=True
    )

def subscriptions_menu():
    buttons = []
    for sub in SUBSCRIPTIONS.values():
        buttons.append([f"{sub['name']} - {sub['price']}₽"])
    buttons.append(["🔙 НАЗАД"])
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)

def back_to_menu():
    return ReplyKeyboardMarkup([["🔙 НАЗАД"]], resize_keyboard=True)

# Обработчики команд
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "🔐 <b>ДОБРО ПОЖАЛОВАТЬ В БОТ ПОДПИСОК!</b>\n\n"
        "📢 Бесплатные юзернеймы в нашем канале:\n"
        "👉 https://t.me/kashvaIdimerr46\n\n"
        "💎 <b>Хотите полный доступ?</b> Выбирайте подписку:"
    )
    await update.message.reply_text(
        welcome_text, 
        reply_markup=main_menu(),
        parse_mode='HTML'
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    
    if text == "💎 ПОДКЛЮЧИТЬ ПОДПИСКУ":
        await show_subscriptions(update, context)
    elif text == "ℹ️ ИНФОРМАЦИЯ":
        await show_general_info(update, context)
    elif text == "🕘 ПОДДЕРЖКА (9:00-21:00)":
        await show_support_info(update, context)
    elif text == "🔙 ГЛАВНОЕ МЕНЮ":
        await start(update, context)
    elif text == "🔙 НАЗАД":
        await start(update, context)
    elif any(sub["name"] in text for sub in SUBSCRIPTIONS.values()):
        await handle_subscription(update, context)
    else:
        await update.message.reply_text(
            "Пожалуйста, используйте кнопки меню",
            reply_markup=main_menu()
        )

async def show_subscriptions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "💰 <b>ДОСТУПНЫЕ ПОДПИСКИ:</b>\n\nВыберите нужный вариант:"
    await update.message.reply_text(
        text,
        reply_markup=subscriptions_menu(),
        parse_mode='HTML'
    )

async def handle_subscription(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    sub_name = text.split(" - ")[0]
    
    sub = None
    for s in SUBSCRIPTIONS.values():
        if s["name"] == sub_name:
            sub = s
            break
    
    if not sub:
        await update.message.reply_text(
            "Подписка не найдена",
            reply_markup=main_menu()
        )
        return
    
    response = (
        f"🎉 <b>{sub['name']}</b>\n\n"
        f"📝 <i>{sub['desc']}</i>\n\n"
        f"💵 Стоимость: <b>{sub['price']}₽</b>\n\n"
        f"<b>Как оплатить:</b>\n"
        f"1. Напишите администратору: {ADMIN_USERNAME}\n"
        f"2. Укажите подписку: <b>{sub['name']}</b>\n"
        f"3. Оплатите <b>{sub['price']}₽</b>\n\n"
    )
    
    if "20 ЮЗЕРНЕЙМОВ" in sub['name']:
        response += "ℹ️ Укажите в сообщении нужные вам 20 юзернеймов\n\n"
    elif "5 ЮЗЕРНЕЙМОВ" in sub['name']:
        response += "ℹ️ Укажите какие 5 юзернеймов вам нужны\n\n"
    
    response += "⏳ Доступ будет открыт в течение 15 минут после оплаты\n\n"
    response += "🕘 Поддержка работает с 9:00 до 21:00"
    
    await update.message.reply_text(
        response,
        reply_markup=back_to_menu(),
        parse_mode='HTML'
    )

async def show_general_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "ℹ️ <b>ИНФОРМАЦИЯ О БОТЕ:</b>\n\n"
        "🔐 Этот бот предоставляет доступ к базе данных\n\n"
        "💎 <b>Доступные подписки:</b>\n"
        "- Полные базы юзернеймов/номеров\n"
        "- Доступ на месяц\n"
        "- Выбор конкретных юзернеймов\n\n"
        "⚡ <b>Преимущества:</b>\n"
        "- Мгновенный доступ после оплаты\n"
        "- Поддержка с 9:00 до 21:00\n"
        "- Актуальные данные\n\n"
        "🕘 <b>Поддержка работает:</b> с 9:00 до 21:00\n"
        "❌ <b>Не спамите!</b> Ответ может занять время"
    )
    await update.message.reply_text(
        text,
        reply_markup=main_menu(),
        parse_mode='HTML'
    )

async def show_support_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "🕘 <b>ИНФОРМАЦИЯ О ПОДДЕРЖКЕ:</b>\n\n"
        "⏰ <b>Часы работы:</b> с 9:00 до 21:00 ежедневно\n\n"
        "📩 <b>Связь с администратором:</b>\n"
        f"👉 {ADMIN_USERNAME}\n\n"
        "❗ <b>Важно:</b>\n"
        "- Не спамите сообщениями\n"
        "- Один вопрос - одно сообщение\n"
        "- Ответ может занять некоторое время\n\n"
        "📌 По вопросам оплаты и доступа обращайтесь в указанные часы"
    )
    await update.message.reply_text(
        text,
        reply_markup=main_menu(),
        parse_mode='HTML'
    )

# Основная функция
def main():
    application = Application.builder().token(TOKEN).build()
    
    # Обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Запуск
    logger.info("Бот запущен и готов к работе!")
    application.run_polling()

if __name__ == "__main__":
    main()