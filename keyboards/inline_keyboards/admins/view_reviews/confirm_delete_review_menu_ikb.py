from data.config import ROW_WIDTH

from data.callbacks import CONFIRM_DELETE_REVIEW_CALLBACK_DATA, CANCEL_DELETE_REVIEW_CALLBACK_DATA

from data.messages import CONFIRM_DELETE_REVIEW_IKB_MESSAGE, CANCEL_DELETE_REVIEW_IKB_MESSAGE

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def confirm_delete_review_menu_ikb() -> InlineKeyboardMarkup:
    """
    Returns:
        InlineKeyboardMarkup: Confirm delete review inline keyboard.
    """

    ikb = InlineKeyboardMarkup(row_width=ROW_WIDTH)

    ikb.row(InlineKeyboardButton(
        text=CONFIRM_DELETE_REVIEW_IKB_MESSAGE,
        callback_data=CONFIRM_DELETE_REVIEW_CALLBACK_DATA)
    )
    ikb.row(InlineKeyboardButton(
        text=CANCEL_DELETE_REVIEW_IKB_MESSAGE,
        callback_data=CANCEL_DELETE_REVIEW_CALLBACK_DATA)
    )

    return ikb
