from database import UsersInfo

from sqlalchemy import select
from sqlalchemy.exc import ArgumentError


async def get_user_info(user_id: int) -> list:
    """get user info from the database.

    Args:
        user_id (int): The id of the user.

    Returns:
        list: A list with user info containing student_name, student_url, lecturer_name, lecturer_url, and alert.
    """

    try:
        return await select([
            UsersInfo.student_name,
            UsersInfo.student_url,
            UsersInfo.lecturer_name,
            UsersInfo.lecturer_url,
            UsersInfo.alert
        ]).where(UsersInfo.user_id == user_id).gino.all()
    except ArgumentError:
        return []
