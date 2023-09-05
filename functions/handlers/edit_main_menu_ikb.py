from data.redis import LAST_IKB_REDIS_KEY

from functions import UserInfoCache

from keyboards import main_menu_ikb

from loader import bot

from aiogram.dispatcher.storage import FSMContext


async def edit_main_menu_ikb(user_id: int, state: FSMContext) -> None:
    """edit main inline keyboard menu.

    Args:
        user_id (int): Telegram user id.
        state (FSMContext): FSMContext.
    """

    user_info = UserInfoCache(user_id)

    student_name = await user_info.get_student_name_cache()
    lecturer_name = await user_info.get_lecturer_name_cache()

    async with state.proxy() as data:
        # Edit main inline menu.
        await bot.edit_message_reply_markup(
            chat_id=user_id,
            message_id=data[LAST_IKB_REDIS_KEY],
            reply_markup=main_menu_ikb(
                student_name=student_name,
                lecturer_name=lecturer_name,
                alert=await user_info.get_user_alert_cache()
            )
        )
