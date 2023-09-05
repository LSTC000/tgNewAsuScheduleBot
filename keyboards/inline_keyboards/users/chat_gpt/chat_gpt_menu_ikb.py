from data.config import ROW_WIDTH

from data.callbacks import CHAT_GPT_CLEAR_HISTORY_CALLBACK_DATA, CHAT_GPT_CANCEL_TO_MAIN_MENU_CALLBACK_DATA

from data.messages import CHAT_GPT_CLEAR_HISTORY_IKB_MESSAGE, CHAT_GPT_CANCEL_TO_MAIN_MENU_IKB_MESSAGE

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def chat_gpt_menu_ikb() -> InlineKeyboardMarkup:
    """
    Returns:
        InlineKeyboardMarkup: ChatGPT inline keyboard.
    """

    ikb = InlineKeyboardMarkup(row_width=ROW_WIDTH)

    ikb.row(InlineKeyboardButton(
        text=CHAT_GPT_CLEAR_HISTORY_IKB_MESSAGE,
        callback_data=CHAT_GPT_CLEAR_HISTORY_CALLBACK_DATA)
    )
    ikb.row(InlineKeyboardButton(
        text=CHAT_GPT_CANCEL_TO_MAIN_MENU_IKB_MESSAGE,
        callback_data=CHAT_GPT_CANCEL_TO_MAIN_MENU_CALLBACK_DATA)
    )

    return ikb
