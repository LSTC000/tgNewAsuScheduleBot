from data.config import ROW_WIDTH

from data.callbacks import CANCEL_TO_MAIN_MENU_CALLBACK_DATA

from data.messages import CANCEL_TO_MAIN_MENU_IKB_MESSAGE

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def pick_student_menu_ikb(students: list, students_ids: list) -> InlineKeyboardMarkup:
    """
    Args:
        students (list): List with students names.
        students_ids (list): List with students id`s.

    Returns:
        InlineKeyboardMarkup: Pick student menu inline keyboard.
    """

    ikb = InlineKeyboardMarkup(row_width=ROW_WIDTH)

    for i in range(len(students)):
        ikb.row(InlineKeyboardButton(text=students[i], callback_data=students_ids[i]))

    ikb.row(InlineKeyboardButton(text=CANCEL_TO_MAIN_MENU_IKB_MESSAGE, callback_data=CANCEL_TO_MAIN_MENU_CALLBACK_DATA))

    return ikb
