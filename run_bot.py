# https://github.com/python-telegram-bot/python-telegram-bot/wiki/Extensions-%E2%80%93-Your-first-Bot

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultArticle, InputTextMessageContent, Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler, filters, MessageHandler, InlineQueryHandler
import logging
import time
import json
import os
import requests
import utils.chat_data as chatClass

TOKEN = "TOKEN"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    greeting = f"Hello {update.effective_chat.first_name}!\nI'm a Trazumi bot, please talk to me!"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=greeting)

    print("start module")

    chatBot = chatClass.Chat(update.effective_chat.id, update.effective_chat.username, update.effective_chat.full_name)


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


async def caps(update: Update, context: ContextTypes):
    text_caps = ' '.join(context.args).upper()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)


async def inline_caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query
    if not query:
        return
    results = []
    results.append(
        InlineQueryResultArticle(
            id=query.upper(),
            title='Caps',
            input_message_content=InputTextMessageContent(query.upper())
        )
    )
    await context.bot.answer_inline_query(update.inline_query.id, results)


async def greet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Hello {update.effective_chat.first_name}!")


async def options(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a message with three inline buttons attached."""
    keyboard = [
        [
            InlineKeyboardButton("DONE", callback_data="DONE"),
            InlineKeyboardButton("FAILED", callback_data="FAILED"),
        ],
        [InlineKeyboardButton(
            "IN PROGRESS...", callback_data="IN PROGRESS...")],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Please choose:", reply_markup=reply_markup)


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    await query.answer()

    print("button module")

    chatBot = chatClass.Chat(update.effective_chat.id, update.effective_chat.username, update.effective_chat.full_name)

    await query.edit_message_text(text=f"Selected option: {query.data}")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Displays info on how to use the bot."""
    start_help_text = "Use /start to begin a conversation with the bot."
    echo_help_text = "Send any message and I'll reply with your message."
    caps_help_text = "Use /caps followed by your message and I'll reply with your message in UPPERCASE."
    greet_help_text = "Use /greet and the bot will greet you."
    options_help_text = "Use /options to test the options keyboard bot."

    help_text = start_help_text + "\n" + echo_help_text + "\n" + \
        caps_help_text + "\n" + greet_help_text + "\n" + options_help_text
    await update.message.reply_text(help_text)


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")


if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()

    start_handler = CommandHandler('start', start)
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    caps_handler = CommandHandler('caps', caps)
    inline_caps_handler = InlineQueryHandler(inline_caps)
    greet_handler = CommandHandler('greet', greet)  # added
    options_handler = CommandHandler("options", options)
    button_handler = CallbackQueryHandler(button)
    help_handler = CommandHandler("help", help_command)
    unknown_handler = MessageHandler(filters.COMMAND, unknown)

    application.add_handler(start_handler)
    application.add_handler(echo_handler)
    application.add_handler(caps_handler)
    application.add_handler(inline_caps_handler)
    application.add_handler(greet_handler)  # added
    application.add_handler(options_handler)
    application.add_handler(button_handler)
    application.add_handler(help_handler)
    application.add_handler(unknown_handler)

    application.run_polling()
