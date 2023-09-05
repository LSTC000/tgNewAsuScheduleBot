import datetime

from loader import dp, bot

from data.callbacks import CALENDER_SCHEDULE_CALLBACK_DATA

from data.messages import CALENDAR_PICKER_MESSAGE

from data.redis import LAST_IKB_REDIS_KEY

from functions import clear_last_ikb

from pickers import Calendar

from states import StudentScheduleStatesGroup

from aiogram import types
from aiogram.dispatcher.storage import FSMContext


@dp.callback_query_handler(
    lambda c: c.data == CALENDER_SCHEDULE_CALLBACK_DATA,
    state=StudentScheduleStatesGroup.schedule_menu
)
async def calendar_student_schedule(callback: types.CallbackQuery, state: FSMContext) -> None:
    user_id = callback.from_user.id

    now = datetime.datetime.now()

    # Clear last inline keyboard.
    await clear_last_ikb(user_id=user_id, state=state)

    msg = await bot.send_message(
        chat_id=user_id,
        text=CALENDAR_PICKER_MESSAGE,
        reply_markup=await Calendar().start_calendar(year=now.year, month=now.month, state=state)
    )

    async with state.proxy() as data:
        data[LAST_IKB_REDIS_KEY] = msg.message_id

    # Set calendar_picker state.
    await StudentScheduleStatesGroup.calendar_picker.set()
