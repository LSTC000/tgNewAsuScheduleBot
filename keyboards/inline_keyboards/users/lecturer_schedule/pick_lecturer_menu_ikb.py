from data.config import ROW_WIDTH

from data.callbacks import CANCEL_TO_MAIN_MENU_CALLBACK_DATA

from data.messages import CANCEL_TO_MAIN_MENU_IKB_MESSAGE

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def pick_lecturer_menu_ikb(lecturers: list, lecturers_ids: list) -> InlineKeyboardMarkup:
    """
    Args:
        lecturers (list): List with lecturers names.
        lecturers_ids (list): List with lecturers id`s.

    Returns:
        InlineKeyboardMarkup: Pick lecturer menu inline keyboard.
    """

    ikb = InlineKeyboardMarkup(row_width=ROW_WIDTH)

    for i in range(len(lecturers)):
        ikb.row(InlineKeyboardButton(text=lecturers[i], callback_data=lecturers_ids[i]))

    ikb.row(InlineKeyboardButton(text=CANCEL_TO_MAIN_MENU_IKB_MESSAGE, callback_data=CANCEL_TO_MAIN_MENU_CALLBACK_DATA))

    return ikb
