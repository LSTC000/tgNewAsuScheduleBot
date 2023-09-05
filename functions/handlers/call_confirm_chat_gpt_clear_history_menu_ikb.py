from data.redis import LAST_IKB_REDIS_KEY

from data.messages import CONFIRM_CHAT_GPT_CLEAR_HISTORY_MESSAGE

from keyboards import confirm_chat_gpt_clear_history_menu_ikb

from loader import bot

from aiogram.dispatcher.storage import FSMContext


async def call_confirm_chat_gpt_clear_history_menu_ikb(user_id: int, state: FSMContext) -> None:
    """call confirm ChatGPT clear history inline keyboard menu.

    Args:
        user_id (int): Telegram user id.
        state (FSMContext): FSMContext.
    """

    async with state.proxy() as data:
        # Call confirm ChatGPT clear history inline menu.
        msg = await bot.send_message(
            chat_id=user_id,
            text=CONFIRM_CHAT_GPT_CLEAR_HISTORY_MESSAGE,
            reply_markup=confirm_chat_gpt_clear_history_menu_ikb()
        )
        # Remember id of the last inline keyboard.
        data[LAST_IKB_REDIS_KEY] = msg.message_id
