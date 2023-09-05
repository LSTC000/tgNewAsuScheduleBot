from loader import db

from database import Reviews

from sqlalchemy.exc import ArgumentError


async def get_count_reviews() -> int:
    """get count users reviews from the database.

    Returns:
        int: Count users reviews from the database.
    """

    try:
        return await db.func.count(Reviews.id).gino.scalar()
    except ArgumentError:
        return 0
