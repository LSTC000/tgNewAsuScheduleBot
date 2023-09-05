from loader import bot, schedule_cache

from data.messages import ERROR_FIND_LECTURER_MESSAGE, ERROR_MAX_INLINE_KEYBOARD_LENGTH_LECTURER_MESSAGE

from data.redis import LECTURER_NAME_REDIS_KEY, LECTURER_URL_REDIS_KEY

from data.urls import SCHEDULE_ASU_URL

from functions import (
    clear_last_ikb,
    clear_redis_data,
    call_main_menu_ikb,
    call_pick_lecturer_menu_ikb,
    call_schedule_menu_ikb,
    UserInfoCache
)

from states import MainMenuStatesGroup, LecturerScheduleStatesGroup

from aiogram.dispatcher.storage import FSMContext


async def process_lecturer_daily_schedule_parser(
    user_id: int,
    lecturers_data: dict,
    schedule_report: str,
    key_cache: str,
    state: FSMContext,
    update: bool = True,
    clear: bool = False
) -> None:
    """
    :param user_id: Telegram user id.
    :param lecturers_data: Dictionary with all matching lecturers found.
    :param schedule_report: A line with a schedule for the lecturer on the selected day, if there is no lecturer,
    then an empty line.
    :param key_cache: Key of schedule_cache.
    :param state: FSMContext.
    :param update: True if we want to update lecturer data in the database, else - False. Default: True.
    :param clear: True if we want to clear the last inline keyboard, else - False. Default: False.
    """

    if clear:
        # Clear last inline keyboard.
        await clear_last_ikb(user_id=user_id, state=state)

    if lecturers_data:
        if schedule_report:
            # Call schedule inline menu.
            await call_pick_lecturer_menu_ikb(user_id=user_id, lecturers_data=lecturers_data, state=state)
            # Set pick_student state.
            await LecturerScheduleStatesGroup.pick_lecturer_menu.set()
        else:
            await bot.send_message(
                chat_id=user_id,
                text=ERROR_MAX_INLINE_KEYBOARD_LENGTH_LECTURER_MESSAGE.format(SCHEDULE_ASU_URL)
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
                lecturer_name = data[LECTURER_NAME_REDIS_KEY]
                lecturer_url = data[LECTURER_URL_REDIS_KEY]

            schedule_cache[key_cache] = {
                'name': lecturer_name,
                'url': lecturer_url,
                'report': schedule_report
            }

            if update:
                # Update lecturer data in the database.
                await UserInfoCache(user_id).update_lecturer_data_cache(
                    lecturer_name=lecturer_name,
                    lecturer_url=lecturer_url
                )

            await bot.send_message(chat_id=user_id, text=schedule_report)
            # Call schedule inline menu.
            await call_schedule_menu_ikb(user_id=user_id, state=state)
            # Set schedule_menu state.
            await LecturerScheduleStatesGroup.schedule_menu.set()
        else:
            await bot.send_message(chat_id=user_id, text=ERROR_FIND_LECTURER_MESSAGE.format(SCHEDULE_ASU_URL))
            # Clear redis data.
            await clear_redis_data(state=state)
            # Call main inline menu.
            await call_main_menu_ikb(user_id=user_id, state=state)
            # Set main_menu state.
            await MainMenuStatesGroup.main_menu.set()
