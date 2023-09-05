from data.config import ROW_WIDTH

from data.callbacks import CONFIRM_CHAT_GPT_CLEAR_HISTORY_CALLBACK_DATA, CANCEL_CHAT_GPT_CLEAR_HISTORY_CALLBACK_DATA

from data.messages import CONFIRM_CHAT_GPT_CLEAR_HISTORY_IKB_MESSAGE, CANCEL_CHAT_GPT_CLEAR_HISTORY_IKB_MESSAGE

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def confirm_chat_gpt_clear_history_menu_ikb() -> InlineKeyboardMarkup:
    """
    Returns:
        InlineKeyboardMarkup: Confirm clear history of ChatGPT inline keyboard.
    """

    ikb = InlineKeyboardMarkup(row_width=ROW_WIDTH)

    ikb.row(InlineKeyboardButton(
        text=CONFIRM_CHAT_GPT_CLEAR_HISTORY_IKB_MESSAGE,
        callback_data=CONFIRM_CHAT_GPT_CLEAR_HISTORY_CALLBACK_DATA)
    )
    ikb.row(InlineKeyboardButton(
        text=CANCEL_CHAT_GPT_CLEAR_HISTORY_IKB_MESSAGE,
        callback_data=CANCEL_CHAT_GPT_CLEAR_HISTORY_CALLBACK_DATA)
    )

    return ikb
