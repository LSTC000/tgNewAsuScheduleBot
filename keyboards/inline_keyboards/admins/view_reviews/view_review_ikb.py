from data.config import ROW_WIDTH

from data.callbacks import (
    IGNORE_CALLBACK_DATA,
    PREV_REVIEW_CALLBACK_DATA,
    NEXT_REVIEW_CALLBACK_DATA,
    DELETE_REVIEW_CALLBACK_DATA,
    CANCEL_TO_ADMIN_MENU_CALLBACK_DATA
)

from data.messages import DELETE_REVIEW_IKB_MESSAGE, CANCEL_TO_ADMIN_MENU_IKB_MESSAGE

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def view_review_ikb(review_number: int, count_reviews: int) -> InlineKeyboardMarkup:
    """
    Args:
        review_number (int): Number of review.
        count_reviews (int): Count reviews.

    Returns:
        InlineKeyboardMarkup: View review inline keyboard.
    """

    ikb = InlineKeyboardMarkup(row_width=ROW_WIDTH)

    ikb.row(
        InlineKeyboardButton(
            text='<<' if review_number > 0 else ' ',
            callback_data=PREV_REVIEW_CALLBACK_DATA if review_number > 0 else IGNORE_CALLBACK_DATA
        ),
        InlineKeyboardButton(
            text=f'{review_number + 1}/{count_reviews}',
            callback_data=IGNORE_CALLBACK_DATA
        ),
        InlineKeyboardButton(
            text='>>' if review_number < count_reviews - 1 else ' ',
            callback_data=NEXT_REVIEW_CALLBACK_DATA if review_number < count_reviews - 1 else IGNORE_CALLBACK_DATA
        )
    )
    ikb.row(InlineKeyboardButton(
        text=DELETE_REVIEW_IKB_MESSAGE,
        callback_data=DELETE_REVIEW_CALLBACK_DATA)
    )
    ikb.row(InlineKeyboardButton(
        text=CANCEL_TO_ADMIN_MENU_IKB_MESSAGE,
        callback_data=CANCEL_TO_ADMIN_MENU_CALLBACK_DATA)
    )

    return ikb
