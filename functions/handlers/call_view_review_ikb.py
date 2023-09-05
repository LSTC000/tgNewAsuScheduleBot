from data.callbacks import PREV_REVIEW_CALLBACK_DATA, DELETE_REVIEW_CALLBACK_DATA

from data.redis import LAST_IKB_REDIS_KEY, COUNT_REVIEWS_REDIS_KEY, REVIEW_NUMBER_REDIS_KEY, REVIEWS_DATA_REDIS_KEY

from data.messages import CONFIRM_DELETE_REVIEW_MENU_MESSAGE

from database import get_reviews

from keyboards import view_review_ikb, confirm_delete_review_menu_ikb

from utils import create_review_report

from loader import bot

from aiogram.dispatcher.storage import FSMContext


async def call_view_review_ikb(user_id: int, state: FSMContext, callback_data: str = None) -> None:
    """call view review keyboard.

    Args:
        user_id (int): Telegram user id.
        state (FSMContext): FSMContext.
        callback_data (str): Callback data (PREV_REVIEW_CALLBACK_DATA, NEXT_REVIEW_CALLBACK_DATA).
    """

    text, ikb = None, None

    async with state.proxy() as data:
        count_reviews = int(data[COUNT_REVIEWS_REDIS_KEY])

        if REVIEW_NUMBER_REDIS_KEY in data:
            review_number = int(data[REVIEW_NUMBER_REDIS_KEY])
            reviews_data = data[REVIEWS_DATA_REDIS_KEY]
        else:
            review_number = 0
            data[REVIEW_NUMBER_REDIS_KEY] = review_number

            reviews_data = await get_reviews(limit_reviews=count_reviews)
            for i in range(len(reviews_data)):
                reviews_data[i] = list(reviews_data[i])
                reviews_data[i][3] = str(reviews_data[i][3])
            data[REVIEWS_DATA_REDIS_KEY] = reviews_data

        if callback_data is not None:
            if callback_data == DELETE_REVIEW_CALLBACK_DATA:
                text = CONFIRM_DELETE_REVIEW_MENU_MESSAGE
                ikb = confirm_delete_review_menu_ikb()
            else:
                if callback_data == PREV_REVIEW_CALLBACK_DATA:
                    review_number -= 1
                else:
                    review_number += 1

                data[REVIEW_NUMBER_REDIS_KEY] = review_number

        # Call view review inline menu.
        msg = await bot.send_message(
            chat_id=user_id,
            text=create_review_report(
                review_id=reviews_data[review_number][0],
                user_id=reviews_data[review_number][1],
                review=reviews_data[review_number][2],
                created_date=reviews_data[review_number][3]
            ) if text is None else text,
            reply_markup=view_review_ikb(
                review_number=review_number,
                count_reviews=count_reviews
            ) if ikb is None else ikb
        )
        # Remember id of the last inline keyboard.
        data[LAST_IKB_REDIS_KEY] = msg.message_id
