from data.config import ROW_WIDTH

from data.callbacks import (
    VIEW_ALL_REVIEWS_CALLBACK_DATA,
    VIEW_LIMIT_REVIEWS_CALLBACK_DATA,
    CANCEL_TO_ADMIN_MENU_CALLBACK_DATA
)

from data.messages import (
    VIEW_ALL_REVIEWS_IKB_MESSAGE,
    VIEW_LIMIT_REVIEWS_IKB_MESSAGE,
    CANCEL_TO_ADMIN_MENU_IKB_MESSAGE
)

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def view_reviews_menu_ikb() -> InlineKeyboardMarkup:
    """
    Returns:
        InlineKeyboardMarkup: View reviews menu inline keyboard.
    """

    ikb = InlineKeyboardMarkup(row_width=ROW_WIDTH)

    ikb.row(InlineKeyboardButton(text=VIEW_ALL_REVIEWS_IKB_MESSAGE, callback_data=VIEW_ALL_REVIEWS_CALLBACK_DATA))
    ikb.row(InlineKeyboardButton(text=VIEW_LIMIT_REVIEWS_IKB_MESSAGE, callback_data=VIEW_LIMIT_REVIEWS_CALLBACK_DATA))
    ikb.row(InlineKeyboardButton(
        text=CANCEL_TO_ADMIN_MENU_IKB_MESSAGE,
        callback_data=CANCEL_TO_ADMIN_MENU_CALLBACK_DATA)
    )

    return ikb
