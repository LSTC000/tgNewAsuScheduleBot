from loader import logger

from asyncpg import UniqueViolationError

from database import Reviews


async def add_user_review(user_id: int, review: str) -> None:
    """add user review in database.

    Args:
        user_id (int): Telegram user id.
        review (str): User review about the bot.
    """
    
    try:
        review = Reviews(user_id=user_id, review=review)
        await review.create()
    except UniqueViolationError:
        logger.info('Error to user review! User review already exists in the database.')
