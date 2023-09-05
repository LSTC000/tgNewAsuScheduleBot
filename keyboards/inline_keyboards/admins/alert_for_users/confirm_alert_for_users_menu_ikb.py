from data.config import ROW_WIDTH

from data.callbacks import CONFIRM_ALERT_FOR_USERS_CALLBACK_DATA, CANCEL_ALERT_FOR_USERS_CALLBACK_DATA

from data.messages import CONFIRM_ALERT_FOR_USERS_IKB_MESSAGE, CANCEL_ALERT_FOR_USERS_IKB_MESSAGE

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def confirm_alert_for_users_menu_ikb() -> InlineKeyboardMarkup:
    """
    Returns:
        InlineKeyboardMarkup: Confirm sending alert for users inline keyboard.
    """

    ikb = InlineKeyboardMarkup(row_width=ROW_WIDTH)

    ikb.row(InlineKeyboardButton(
        text=CONFIRM_ALERT_FOR_USERS_IKB_MESSAGE,
        callback_data=CONFIRM_ALERT_FOR_USERS_CALLBACK_DATA)
    )
    ikb.row(InlineKeyboardButton(
        text=CANCEL_ALERT_FOR_USERS_IKB_MESSAGE,
        callback_data=CANCEL_ALERT_FOR_USERS_CALLBACK_DATA)
    )

    return ikb
