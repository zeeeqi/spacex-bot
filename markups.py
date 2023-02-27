from telegram import ReplyKeyboardMarkup


yes_no_keyboard = [
    ["Yes", "No"],
    ["End"],
]
YES_NO_MARKUP = ReplyKeyboardMarkup(yes_no_keyboard, one_time_keyboard=True)

first_choice_keyboard = [
    ["Yes, I will help!"],
    ["No, sorry..."],
]
FIRST_CHOICE_MARKUP = ReplyKeyboardMarkup(first_choice_keyboard, one_time_keyboard=True)
