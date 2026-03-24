import logging
import os

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ChatMemberStatus
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

CHANNEL_USERNAME = "@pdiddybigboss"
CHANNEL_URL = "https://t.me/pdiddybigboss"

MENU_CALLBACKS = {
    "buy_tg": "Купить ТГШки",
    "buy_packs": "Купить паки",
    "imessages": "iMessages",
    "private": "Приват",
    "support": "Поддержка",
}


def build_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Купить ТГшки", callback_data="buy_tg")],
            [InlineKeyboardButton("Купить паки", callback_data="buy_packs")],
            [InlineKeyboardButton("iMessages", callback_data="imessages")],
            [InlineKeyboardButton("Приват", callback_data="private")],
            [InlineKeyboardButton("Поддержка", callback_data="support")],
        ]
    )


def build_subscribe_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("📢 Подписаться на канал", url=CHANNEL_URL)],
            [InlineKeyboardButton("✅ Я подписался", callback_data="check_subscription")],
        ]
    )


async def is_user_subscribed(user_id: int, context: ContextTypes.DEFAULT_TYPE) -> bool:
    member = await context.bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user_id)
    return member.status in {
        ChatMemberStatus.MEMBER,
        ChatMemberStatus.ADMINISTRATOR,
        ChatMemberStatus.OWNER,
    }


async def show_main_menu(chat_id: int, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_message(
        chat_id=chat_id,
        text=(
            "Вы в меню. Выберите, что хотите приобрести из списка ниже:"
        ),
        reply_markup=build_menu_keyboard(),
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.effective_user or not update.effective_chat:
        return

    user = update.effective_user
    chat_id = update.effective_chat.id

    if await is_user_subscribed(user.id, context):
        await show_main_menu(chat_id, context)
        return

    name = user.first_name or user.username or "друг"
    await context.bot.send_message(
        chat_id=chat_id,
        text=(
            f"Привет, {name}! 👋\n\n"
            "Подпишись на канал, чтобы продолжить: "
            f"{CHANNEL_URL}"
        ),
        reply_markup=build_subscribe_keyboard(),
    )


async def on_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    if not query or not query.from_user:
        return

    await query.answer()

    if query.data == "check_subscription":
        if await is_user_subscribed(query.from_user.id, context):
            await query.message.reply_text("Отлично, подписка подтверждена ✅")
            if query.message:
                await show_main_menu(query.message.chat_id, context)
        else:
            await query.message.reply_text(
                "Пока не вижу подписку 😕\n"
                "Подпишись на канал и нажми кнопку снова.",
                reply_markup=build_subscribe_keyboard(),
            )
        return

    if query.data in MENU_CALLBACKS:
        await query.message.reply_text(
            f"Вы выбрали раздел: {MENU_CALLBACKS[query.data]}.\n"
            "Этот раздел пока в разработке — скоро добавим логику."
        )


def main() -> None:
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise RuntimeError("Переменная окружения BOT_TOKEN не задана")

    application = Application.builder().token(token).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(on_callback))

    logger.info("Bot started")
    application.run_polling()


if __name__ == "__main__":
    main()
