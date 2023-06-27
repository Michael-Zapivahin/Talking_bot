import os

from telegram import Update
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackContext,
    MessageHandler,
    Filters
)
from dotenv import load_dotenv
from dialog_flow_utils import detect_intent_texts


def start(update: Update, context: CallbackContext):
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_text(f'Hi {user.username}, i\'am bot speaker!')


def send_answer(update: Update, context: CallbackContext):
    message_text = [update.message.text]
    (answer_text, find) = detect_intent_texts(
                        os.environ.get('PROJECT_ID'),
                        update.effective_user,
                        message_text
    )
    update.message.reply_text(answer_text)


def main():
    load_dotenv()
    telegram_bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')

    updater = Updater(telegram_bot_token)

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(
        MessageHandler(
            Filters.text & ~Filters.command,
            send_answer
        )
    )

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
