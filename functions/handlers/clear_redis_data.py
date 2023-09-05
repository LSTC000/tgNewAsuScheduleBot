from data.redis import LAST_IKB_REDIS_KEY

from aiogram.dispatcher.storage import FSMContext


async def clear_redis_data(state: FSMContext) -> None:
    """clear all redis data on restart bot.

    Args:
        state (FSMContext): FSMContext.
    """

    async with state.proxy() as data:
        last_ikb = data[LAST_IKB_REDIS_KEY]
        data.clear()
        data[LAST_IKB_REDIS_KEY] = last_ikb
