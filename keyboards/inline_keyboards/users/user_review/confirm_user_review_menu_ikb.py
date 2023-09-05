from data.config import ROW_WIDTH

from data.callbacks import CONFIRM_USER_REVIEW_CALLBACK_DATA, CANCEL_USER_REVIEW_CALLBACK_DATA

from data.messages import CONFIRM_USER_REVIEW_IKB_MESSAGE, CANCEL_USER_REVIEW_IKB_MESSAGE

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def confirm_user_review_menu_ikb() -> InlineKeyboardMarkup:
    """
    Returns:
        InlineKeyboardMarkup: Confirm user review inline keyboard.
    """

    ikb = InlineKeyboardMarkup(row_width=ROW_WIDTH)

    ikb.row(InlineKeyboardButton(
        text=CONFIRM_USER_REVIEW_IKB_MESSAGE,
        callback_data=CONFIRM_USER_REVIEW_CALLBACK_DATA)
    )
    ikb.row(InlineKeyboardButton(
        text=CANCEL_USER_REVIEW_IKB_MESSAGE,
        callback_data=CANCEL_USER_REVIEW_CALLBACK_DATA)
    )

    return ikb
