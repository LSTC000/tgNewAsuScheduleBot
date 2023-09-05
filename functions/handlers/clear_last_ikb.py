from data.redis import LAST_IKB_REDIS_KEY

from loader import bot, logger

from aiogram.dispatcher.storage import FSMContext
from aiogram.utils.exceptions import (
    MessageCantBeEdited, 
    MessageToDeleteNotFound, 
    MessageCantBeDeleted, 
    MessageNotModified
)


async def clear_last_ikb(user_id: int, state: FSMContext, delete: bool = True) -> None:
    """clear last inline keyboard message.

    Args:
        user_id (int): Telegram user id.
        state (FSMContext): FSMContext.
        delete (bool, optional): True - delete message, False - delete only ikb. Defaults to True.
    """

    async with state.proxy() as data:
        if LAST_IKB_REDIS_KEY in data:
            try:
                if delete:
                    await bot.delete_message(chat_id=user_id, message_id=data[LAST_IKB_REDIS_KEY])
                else:
                    await bot.edit_message_reply_markup(
                        chat_id=user_id,
                        message_id=data[LAST_IKB_REDIS_KEY],
                        reply_markup=None
                    )
            except (
                MessageCantBeEdited, 
                MessageToDeleteNotFound, 
                MessageCantBeDeleted, 
                MessageNotModified
            ):
                logger.info('Error to clear last inline keyboard!')
