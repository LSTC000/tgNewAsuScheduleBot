from data.redis import LAST_IKB_REDIS_KEY, STUDENTS_DATA_REDIS_KEY

from data.messages import PICK_STUDENT_MENU_MESSAGE

from keyboards import pick_student_menu_ikb

from loader import bot

from aiogram.dispatcher.storage import FSMContext


async def call_pick_student_menu_ikb(user_id: int, students_data: dict, state: FSMContext) -> None:
    """call pick student inline keyboard menu.

    Args:
        user_id (int): Telegram user id.
        students_data (dict): Dictionary with all matching groups found.
        state (FSMContext): FSMContext.
    """

    async with state.proxy() as data:
        students = [''] * len(students_data)
        students_ids = list(students_data.keys())

        for student_id in students_ids:
            students[int(student_id)] = students_data[student_id]['name']

        data[STUDENTS_DATA_REDIS_KEY] = students_data

        # Call pick student inline menu.
        msg = await bot.send_message(
            chat_id=user_id,
            text=PICK_STUDENT_MENU_MESSAGE,
            reply_markup=pick_student_menu_ikb(students=students, students_ids=students_ids)
        )
        # Remember id of the last inline keyboard.
        data[LAST_IKB_REDIS_KEY] = msg.message_id
