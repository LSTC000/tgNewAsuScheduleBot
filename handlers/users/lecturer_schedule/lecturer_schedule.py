from loader import dp, bot

from data.callbacks import LECTURER_SCHEDULE_CALLBACK_DATA

from data.messages import ENTER_LECTURER_MESSAGE

from functions import clear_last_ikb

from states import MainMenuStatesGroup, LecturerScheduleStatesGroup

from aiogram import types
from aiogram.dispatcher.storage import FSMContext


@dp.callback_query_handler(lambda c: c.data == LECTURER_SCHEDULE_CALLBACK_DATA, state=MainMenuStatesGroup.main_menu)
async def lecturer_schedule(callback: types.CallbackQuery, state: FSMContext) -> None:
    user_id = callback.from_user.id

    # Clear last inline keyboard.
    await clear_last_ikb(user_id=user_id, state=state)
    # Message about enter student.
    await bot.send_message(chat_id=user_id, text=ENTER_LECTURER_MESSAGE)
    # Set enter_lecturer state.
    await LecturerScheduleStatesGroup.enter_lecturer.set()
