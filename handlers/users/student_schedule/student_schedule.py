from loader import dp, bot

from data.callbacks import STUDENT_SCHEDULE_CALLBACK_DATA

from data.messages import ENTER_STUDENT_MESSAGE

from functions import clear_last_ikb

from states import MainMenuStatesGroup, StudentScheduleStatesGroup

from aiogram import types
from aiogram.dispatcher.storage import FSMContext


@dp.callback_query_handler(lambda c: c.data == STUDENT_SCHEDULE_CALLBACK_DATA, state=MainMenuStatesGroup.main_menu)
async def student_schedule(callback: types.CallbackQuery, state: FSMContext) -> None:
    user_id = callback.from_user.id

    # Clear last inline keyboard.
    await clear_last_ikb(user_id=user_id, state=state)
    # Message about enter student.
    await bot.send_message(chat_id=user_id, text=ENTER_STUDENT_MESSAGE)
    # Set enter_student state.
    await StudentScheduleStatesGroup.enter_student.set()
