import logging
from os import getenv
import re

from telegram.ext import (
    Application,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)

from states import (
    FIRST_CHOOSE,
    FINDING_LAUNCH,
    start,
    handle_first_choice,
    finding_launch,
    handle_end,
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

BOT_TOKEN = getenv('BOT_TOKEN', None)


def main() -> None:
    """Run the bot."""
    application = Application.builder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            FIRST_CHOOSE: [
                MessageHandler(filters.Regex(re.compile(r'(yes|no)', re.IGNORECASE)), handle_first_choice),
            ],
            FINDING_LAUNCH: [
                MessageHandler(filters.Regex(re.compile(r'(yes|no)', re.IGNORECASE)), finding_launch),
            ],

        },
        fallbacks=[MessageHandler(filters.Regex(re.compile(r'end', re.IGNORECASE)), handle_end)],
    )

    application.add_handler(conv_handler)

    application.run_polling()


if __name__ == "__main__":
    main()
