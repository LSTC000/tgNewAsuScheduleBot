from data.redis import (
    LAST_IKB_REDIS_KEY, 
    LAST_STUDENT_NAME_REDIS_KEY,
    LAST_STUDENT_URL_REDIS_KEY,
    LAST_LECTURER_NAME_REDIS_KEY,
    LAST_LECTURER_URL_REDIS_KEY
)

from data.messages import MAIN_MENU_MESSAGE

from functions import UserInfoCache

from keyboards import main_menu_ikb

from loader import bot

from aiogram.dispatcher.storage import FSMContext


async def call_main_menu_ikb(user_id: int, state: FSMContext) -> None:
    """call main inline keyboard menu.

    Args:
        user_id (int): Telegram user id.
        state (FSMContext): FSMContext.
    """

    user_info = UserInfoCache(user_id)

    student_name = await user_info.get_student_name_cache()
    lecturer_name = await user_info.get_lecturer_name_cache()

    async with state.proxy() as data:
        if student_name is not None:
            student_url = await user_info.get_student_url_cache()
            data[LAST_STUDENT_NAME_REDIS_KEY] = student_name
            data[LAST_STUDENT_URL_REDIS_KEY] = student_url

        if lecturer_name is not None:
            lecturer_url = await user_info.get_lecturer_url_cache()
            data[LAST_LECTURER_NAME_REDIS_KEY] = lecturer_name
            data[LAST_LECTURER_URL_REDIS_KEY] = lecturer_url

        # Call main inline menu.
        msg = await bot.send_message(
            chat_id=user_id,
            text=MAIN_MENU_MESSAGE,
            reply_markup=main_menu_ikb(
                student_name=student_name,
                lecturer_name=lecturer_name,
                alert=await user_info.get_user_alert_cache()
            )
        )
        # Remember id of the last inline keyboard.
        data[LAST_IKB_REDIS_KEY] = msg.message_id
