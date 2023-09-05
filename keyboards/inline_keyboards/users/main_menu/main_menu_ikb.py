from data.config import ROW_WIDTH

from data.callbacks import (
    CHANGE_USER_ALERT_CALLBACK_DATA,
    LAST_STUDENT_SCHEDULE_CALLBACK_DATA,
    LAST_LECTURER_SCHEDULE_CALLBACK_DATA,
    STUDENT_SCHEDULE_CALLBACK_DATA,
    LECTURER_SCHEDULE_CALLBACK_DATA,
    CHAT_GPT_MENU_CALLBACK_DATA,
    ASU_BUILDINGS_CALLBACK_DATA,
    SOCIAL_CALLBACK_DATA,
    USER_REVIEW_CALLBACK_DATA,
    HELP_CALLBACK_DATA
)

from data.messages import (
    STUDENT_SCHEDULE_IKB_MESSAGE,
    LECTURER_SCHEDULE_IKB_MESSAGE,
    CHAT_GPT_MENU_IKB_MESSAGE,
    ASU_BUILDINGS_IKB_MASSAGE,
    USER_ALERT_ON_IKB_MESSAGE,
    USER_ALERT_OFF_IKB_MESSAGE,
    SOCIAL_IKB_MESSAGE,
    USER_REVIEW_IKB_MESSAGE,
    HELP_IKB_MESSAGE
)

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def main_menu_ikb(
    student_name: str,
    lecturer_name: str,
    alert: bool,
) -> InlineKeyboardMarkup:
    """
    Args:
        student_name (str): Last user student name.
        lecturer_name (str): Last user lecturer name.
        alert (bool): True if the user has enabled alerts, else False.

    Returns:
        InlineKeyboardMarkup: Main menu inline keyboard.
    """

    ikb = InlineKeyboardMarkup(row_width=ROW_WIDTH)

    if student_name is not None:
        ikb.row(InlineKeyboardButton(
            text=f'👨‍🎓 {student_name}',
            callback_data=LAST_STUDENT_SCHEDULE_CALLBACK_DATA)
        )

    if lecturer_name is not None:
        ikb.row(InlineKeyboardButton(
            text=f'👩‍🏫 {lecturer_name}',
            callback_data=LAST_LECTURER_SCHEDULE_CALLBACK_DATA)
        )

    ikb.row(
        InlineKeyboardButton(text=STUDENT_SCHEDULE_IKB_MESSAGE, callback_data=STUDENT_SCHEDULE_CALLBACK_DATA),
        InlineKeyboardButton(text=LECTURER_SCHEDULE_IKB_MESSAGE, callback_data=LECTURER_SCHEDULE_CALLBACK_DATA)
    )

    ikb.row(InlineKeyboardButton(text=CHAT_GPT_MENU_IKB_MESSAGE, callback_data=CHAT_GPT_MENU_CALLBACK_DATA))

    ikb.row(
        InlineKeyboardButton(text=ASU_BUILDINGS_IKB_MASSAGE, callback_data=ASU_BUILDINGS_CALLBACK_DATA),
        InlineKeyboardButton(text=SOCIAL_IKB_MESSAGE, callback_data=SOCIAL_CALLBACK_DATA)
    )

    ikb.row(
        InlineKeyboardButton(
            text=USER_ALERT_OFF_IKB_MESSAGE if alert else USER_ALERT_ON_IKB_MESSAGE,
            callback_data=CHANGE_USER_ALERT_CALLBACK_DATA
        ),
        InlineKeyboardButton(text=USER_REVIEW_IKB_MESSAGE, callback_data=USER_REVIEW_CALLBACK_DATA)
    )

    ikb.row(InlineKeyboardButton(text=HELP_IKB_MESSAGE, callback_data=HELP_CALLBACK_DATA))

    return ikb
