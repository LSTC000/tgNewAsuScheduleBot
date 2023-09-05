from loader import bot, schedule_cache

from data.messages import ERROR_FIND_STUDENT_MESSAGE, ERROR_MAX_INLINE_KEYBOARD_LENGTH_STUDENT_MESSAGE

from data.redis import STUDENT_NAME_REDIS_KEY, STUDENT_URL_REDIS_KEY

from data.urls import SCHEDULE_ASU_URL

from functions import (
    clear_last_ikb,
    clear_redis_data,
    call_main_menu_ikb,
    call_pick_student_menu_ikb,
    call_schedule_menu_ikb,
    UserInfoCache
)

from states import MainMenuStatesGroup, StudentScheduleStatesGroup

from aiogram.dispatcher.storage import FSMContext


async def process_student_daily_schedule_parser(
    user_id: int,
    students_data: dict,
    schedule_report: str,
    key_cache: str,
    state: FSMContext,
    update: bool = True,
    clear: bool = False
) -> None:
    """
    :param user_id: Telegram user id.
    :param students_data: Dictionary with all matching groups found.
    :param schedule_report: A line with a schedule for the student on the selected day, if there is no schedule,
    then an empty line.
    :param key_cache: Key of schedule_cache.
    :param state: FSMContext.
    :param update: True if we want to update student data in the database, else - False. Default: True.
    :param clear: True if we want to clear the last inline keyboard, else - False. Default: False.
    """

    if clear:
        # Clear last inline keyboard.
        await clear_last_ikb(user_id=user_id, state=state)

    if students_data:
        if schedule_report:
            # Call schedule inline menu.
            await call_pick_student_menu_ikb(user_id=user_id, students_data=students_data, state=state)
            # Set pick_student state.
            await StudentScheduleStatesGroup.pick_student_menu.set()
        else:
            await bot.send_message(
                chat_id=user_id,
                text=ERROR_MAX_INLINE_KEYBOARD_LENGTH_STUDENT_MESSAGE.format(SCHEDULE_ASU_URL)
            )
            # Clear redis data.
            await clear_redis_data(state=state)
            # Call main inline menu.
            await call_main_menu_ikb(user_id=user_id, state=state)
            # Set main_menu state.
            await MainMenuStatesGroup.main_menu.set()
    else:
        if schedule_report:
            async with state.proxy() as data:
                student_name = data[STUDENT_NAME_REDIS_KEY]
                student_url = data[STUDENT_URL_REDIS_KEY]

            schedule_cache[key_cache] = {
                'name': student_name,
                'url': student_url,
                'report': schedule_report
            }

            if update:
                # Update student data in the database.
                await UserInfoCache(user_id).update_student_data_cache(
                    student_name=student_name,
                    student_url=student_url
                )

            await bot.send_message(chat_id=user_id, text=schedule_report)
            # Call schedule inline menu.
            await call_schedule_menu_ikb(user_id=user_id, state=state)
            # Set schedule_menu state.
            await StudentScheduleStatesGroup.schedule_menu.set()
        else:
            await bot.send_message(chat_id=user_id, text=ERROR_FIND_STUDENT_MESSAGE.format(SCHEDULE_ASU_URL))
            # Clear redis data.
            await clear_redis_data(state=state)
            # Call main inline menu.
            await call_main_menu_ikb(user_id=user_id, state=state)
            # Set main_menu state.
            await MainMenuStatesGroup.main_menu.set()
