from data.config import ROW_WIDTH

from data.callbacks import (
    TOMORROW_SCHEDULE_CALLBACK_DATA,
    WEEKLY_SCHEDULE_CALLBACK_DATA,
    CALENDER_SCHEDULE_CALLBACK_DATA,
    CANCEL_TO_MAIN_MENU_CALLBACK_DATA
)

from data.messages import (
    TOMORROW_SCHEDULE_IKB_MESSAGE,
    WEEKLY_SCHEDULE_IKB_MESSAGE,
    CALENDER_SCHEDULE_IKB_MESSAGE,
    CANCEL_TO_MAIN_MENU_IKB_MESSAGE
)

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def schedule_menu_ikb() -> InlineKeyboardMarkup:
    """
    Returns:
        InlineKeyboardMarkup: Schedule menu inline keyboard.
    """

    ikb = InlineKeyboardMarkup(row_width=ROW_WIDTH)

    ikb.row(InlineKeyboardButton(text=TOMORROW_SCHEDULE_IKB_MESSAGE, callback_data=TOMORROW_SCHEDULE_CALLBACK_DATA))
    ikb.row(InlineKeyboardButton(text=WEEKLY_SCHEDULE_IKB_MESSAGE, callback_data=WEEKLY_SCHEDULE_CALLBACK_DATA))
    ikb.row(InlineKeyboardButton(text=CALENDER_SCHEDULE_IKB_MESSAGE, callback_data=CALENDER_SCHEDULE_CALLBACK_DATA))
    ikb.row(InlineKeyboardButton(text=CANCEL_TO_MAIN_MENU_IKB_MESSAGE, callback_data=CANCEL_TO_MAIN_MENU_CALLBACK_DATA))

    return ikb
