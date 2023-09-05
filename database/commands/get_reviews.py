from database import Reviews

from sqlalchemy import select, desc
from sqlalchemy.exc import ArgumentError


async def get_reviews(limit_reviews: int) -> list:
    """get users reviews from the database.

    Args:
        limit_reviews (int): Limit of reviews.

    Returns:
        list: A list with users reviews.
    """

    try:
        return await select([
            Reviews.id,
            Reviews.user_id,
            Reviews.review,
            Reviews.created_date
        ]).order_by(desc(Reviews.created_date)).limit(limit_reviews).gino.all()
    except ArgumentError:
        return []
