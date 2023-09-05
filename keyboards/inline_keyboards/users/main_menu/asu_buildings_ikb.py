from data.config import ROW_WIDTH

from data.callbacks import CANCEL_TO_MAIN_MENU_CALLBACK_DATA

from data.messages import CANCEL_TO_MAIN_MENU_IKB_MESSAGE

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def asu_buildings_ikb() -> InlineKeyboardMarkup:
    """
    Returns:
        InlineKeyboardMarkup: ASU buildings menu inline keyboard.
    """

    ikb = InlineKeyboardMarkup(row_width=ROW_WIDTH)

    ikb.row(InlineKeyboardButton(text=CANCEL_TO_MAIN_MENU_IKB_MESSAGE, callback_data=CANCEL_TO_MAIN_MENU_CALLBACK_DATA))

    return ikb
