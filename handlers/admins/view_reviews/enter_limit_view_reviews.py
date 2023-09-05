from loader import dp, bot

from data.messages import ERROR_ENTER_LIMIT_VIEW_REVIEWS_MESSAGE

from data.redis import COUNT_REVIEWS_REDIS_KEY

from functions import call_view_review_ikb, call_view_reviews_menu_ikb

from utils import Validator

from states import ViewReviewsStatesGroup

from aiogram import types
from aiogram.dispatcher.storage import FSMContext


@dp.message_handler(content_types=types.ContentTypes.TEXT, state=ViewReviewsStatesGroup.enter_limit_view_reviews)
async def enter_limit_view_reviews(message: types.Message, state: FSMContext) -> None:
    user_id = message.from_user.id
    text = message.text

    async with state.proxy() as data:
        count_reviews = int(data[COUNT_REVIEWS_REDIS_KEY])

    # Check alert on valid.
    if Validator().limit_view_reviews_validation(limit=text, max_limit=count_reviews):
        async with state.proxy() as data:
            data[COUNT_REVIEWS_REDIS_KEY] = text
        # Call view review menu.
        await call_view_review_ikb(user_id=user_id, state=state)
        # Set view_review state.
        await ViewReviewsStatesGroup.view_review.set()
    else:
        await bot.send_message(chat_id=user_id, text=ERROR_ENTER_LIMIT_VIEW_REVIEWS_MESSAGE.format(count_reviews))
        # Call view reviews menu.
        await call_view_reviews_menu_ikb(user_id=user_id, state=state)
        # Set view_reviews_menu state.
        await ViewReviewsStatesGroup.view_reviews_menu.set()
