from loader import logger

from asyncpg import UniqueViolationError

from database import UsersInfo


async def add_user_info(user_id: int) -> None:
    """add user info in database.

    Args:
        user_id (int): Telegram user id.
    """

    try:
        user_info = UsersInfo(
            user_id=user_id,
            student_name=None,
            student_url=None,
            lecturer_name=None,
            lecturer_url=None,
            alert=True
        )
        await user_info.create()
    except UniqueViolationError:
        logger.info('Error to user info! User info already exists in the database.')
