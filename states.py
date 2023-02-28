from telegram import Update, ReplyKeyboardRemove
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
)

from markups import FIRST_CHOICE_MARKUP, YES_NO_MARKUP
from api import SpaceXAPI

import logging

logger = logging.getLogger(__name__)


async def initialize_user_data(context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Receive a context and initialize the user data. Fetching info from the API
    """
    video_info = SpaceXAPI().get_video_info()
    context.user_data['left'] = 0
    context.user_data['right'] = video_info['frames']
    context.user_data['frame'] = video_info['frames'] // 2


FIRST_CHOOSE, FINDING_LAUNCH = range(2)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Start the conversation and ask the user if they are willing to help.
    """

    await initialize_user_data(context)

    await update.message.reply_text(
        "Hi! I need to find the exact frame when the FalconX Heavy launch.\nWill you help me?",
        reply_markup=FIRST_CHOICE_MARKUP,
    )

    return FIRST_CHOOSE


async def handle_first_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Process if the user will help or not.
    """

    message = update.message.text
    if message.lower() in ["yes, i will help!", "yes", "si"]:
        await update.message.reply_text(
            "Great! I will show you frames from the SpaceX Falcon Heavy launch. "
            "Please tell me if it has launched yet.",
        )
        frame_url = SpaceXAPI().get_frame_url(context.user_data['frame'])
        await update.message.reply_photo(
            frame_url,
            caption=f'{context.user_data["frame"]} - Has it launched yet?',
            reply_markup=YES_NO_MARKUP,
        )
        return FINDING_LAUNCH
    else:
        await update.message.reply_text("Oh, that's too bad... Hope to see you back soon!")
        return ConversationHandler.END


def check_if_launch(user: dict) -> bool:
    """
    Check if the user has found the launch frame.
    """
    video_info = SpaceXAPI().get_video_info()
    frame_rate = video_info['frame_rate'][0] / video_info['frame_rate'][1]
    logger.log(logging.INFO, f"left: {user['left']}, right: {user['right']}, frame: {user['frame']}, frame_rate: {frame_rate}")
    return user['left'] >= user['right'] - frame_rate


def get_next_frame(user: dict, message: str) -> int:
    """
    Get the next frame to show to the user.
    """
    if message.lower() == "yes":
        user['right'] = user['frame']
    else:
        user['left'] = user['frame']
    user['frame'] = (user['left'] + user['right']) // 2
    return user['frame']


async def finding_launch(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ask the user if the SpaceX Falcon Heavy has launched yet."""
    user = context.user_data
    message = update.message.text
    next_frame = get_next_frame(user, message)
    if check_if_launch(user):
        await update.message.reply_text(
            f"I think the launch happened on frame {user['frame']}. "
            "Thanks for helping me!",
            reply_markup=ReplyKeyboardRemove()
        )
        return ConversationHandler.END

    frame_url = SpaceXAPI().get_frame_url(next_frame)
    await update.message.reply_photo(
        frame_url,
        caption=f'{next_frame} - Has it launched yet?',
        reply_markup=YES_NO_MARKUP,
    )
    return FINDING_LAUNCH


async def handle_end(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    End Conversation.
    """
    await update.message.reply_text(
        "Bye! I hope we can talk again soon!.", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END
