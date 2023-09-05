from data.config import ROW_WIDTH

from data.callbacks import START_COMMAND_CALLBACK_DATA

from data.messages import START_COMMAND_IKB_MESSAGE

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def start_ikb() -> InlineKeyboardMarkup:
    """
    Returns:
        InlineKeyboardMarkup: Start command inline keyboard.
    """

    ikb = InlineKeyboardMarkup(row_width=ROW_WIDTH)

    ikb.row(InlineKeyboardButton(text=START_COMMAND_IKB_MESSAGE, callback_data=START_COMMAND_CALLBACK_DATA))

    return ikb
