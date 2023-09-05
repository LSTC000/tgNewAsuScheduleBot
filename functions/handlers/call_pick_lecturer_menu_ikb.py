from data.redis import LAST_IKB_REDIS_KEY, LECTURERS_DATA_REDIS_KEY

from data.messages import PICK_LECTURER_MENU_MESSAGE

from keyboards import pick_lecturer_menu_ikb

from loader import bot

from aiogram.dispatcher.storage import FSMContext


async def call_pick_lecturer_menu_ikb(user_id: int, lecturers_data: dict, state: FSMContext) -> None:
    """call pick lecturer inline keyboard menu.

    Args:
        user_id (int): Telegram user id.
        lecturers_data (dict): Dictionary with all matching groups found.
        state (FSMContext): FSMContext.
    """

    async with state.proxy() as data:
        lecturers = [''] * len(lecturers_data)
        lecturers_ids = list(lecturers_data.keys())

        for lecturer_id in lecturers_ids:
            lecturers[int(lecturer_id)] = lecturers_data[lecturer_id]['name']

        data[LECTURERS_DATA_REDIS_KEY] = lecturers_data

        # Call pick lecturer inline menu.
        msg = await bot.send_message(
            chat_id=user_id,
            text=PICK_LECTURER_MENU_MESSAGE,
            reply_markup=pick_lecturer_menu_ikb(lecturers=lecturers, lecturers_ids=lecturers_ids)
        )
        # Remember id of the last inline keyboard.
        data[LAST_IKB_REDIS_KEY] = msg.message_id
