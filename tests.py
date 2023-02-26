#!/usr/bin/env python
# pylint: disable=unused-argument, wrong-import-position


import logging
from typing import Dict

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

FIRST_CHOOSE, FINDING_LAUNCH = range(2)

first_choice_keyboard = [
    ["Yes, I will help!"],
    ["No, sorry..."]
]
first_choice_markup = ReplyKeyboardMarkup(first_choice_keyboard, one_time_keyboard=True)

yes_no_keyboard = [
    ["Yes", "No"],
    ["End"],
]
yes_no_markup = ReplyKeyboardMarkup(yes_no_keyboard, one_time_keyboard=True)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Start the conversation and ask user for input."""
    context.user_data["left_pointer"] = 0
    context.user_data["right_pointer"] = 61696
    context.user_data["current_frame"] = 30848
    await update.message.reply_text(
        "Hi! I need find the exact frame when the FalconX Heavy launchs.\nWill you help me?",
        reply_markup=first_choice_markup,
    )

    return FIRST_CHOOSE


async def handle_first_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Process if the user will help or not."""
    message = update.message.text
    if message == "Yes, I will help!":
        await update.message.reply_text(
            "Great! I will show you a frame from the SpaceX Falcon Heavy launch. "
            "Please tell me if it has launched yet.",
            reply_markup=yes_no_markup,
        )
        await update.message.reply_photo(f"https://framex-dev.wadrid.net/api/video/Falcon%20Heavy%20Test%20Flight%20(Hosted%20Webcast)-wbSwFU6tY1c/frame/{context.user_data['current_frame']}/")
        return FINDING_LAUNCH
    else:
        await update.message.reply_text("Oh, that's too bad. Maybe next time.")
        return ConversationHandler.END


async def finding_launch(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Checks if the SpaceX Falcon Heavy has launched yet."""
    user = context.user_data
    message = update.message.text
    user["right_pointer"] = user["current_frame"] if message == "Yes" else user["right_pointer"]
    user["left_pointer"] = user["current_frame"] if message == "No" else user["left_pointer"]
    user["current_frame"] = (user["left_pointer"] + user["right_pointer"]) // 2
    logging.log(logging.INFO, f"left_pointer: {user['left_pointer']}")
    logging.log(logging.INFO, f"right_pointer: {user['right_pointer']}")
    logging.log(logging.INFO, f"current_frame: {user['current_frame']}")
    await update.message.reply_text(
        f"Please tell me if it has launched yet.",
        reply_markup=yes_no_markup,
    )
    await update.message.reply_photo(f"https://framex-dev.wadrid.net/api/video/Falcon%20Heavy%20Test%20Flight%20(Hosted%20Webcast)-wbSwFU6tY1c/frame/{user['current_frame']}/")
    return FINDING_LAUNCH


async def done(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """End Conversation by command."""
    await update.message.reply_text(
        "Bye! I hope we can talk again some day.", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


def main() -> None:
    """Run the bot."""
    application = Application.builder().token('6207733786:AAF2cSSIJTgxldRT7IwkH2Tm1clSKLGU9jk').build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            FIRST_CHOOSE: [
                MessageHandler(filters.Regex("^(Yes, I will help!|No, sorry...)$"), handle_first_choice),
            ],
            FINDING_LAUNCH: [
                MessageHandler(filters.Regex("^(Yes|No)$"), finding_launch),
            ]
        },
        fallbacks=[MessageHandler(filters.Regex("^End$"), done)],
    )

    application.add_handler(conv_handler)

    application.run_polling()


if __name__ == "__main__":
    main()