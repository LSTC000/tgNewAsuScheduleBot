from database import UsersInfo

from sqlalchemy import select
from sqlalchemy.exc import ArgumentError


async def get_users_alert() -> list[int]:
    """get users who have alert is True.

    Returns:
        list[int]: A list with users who have enabled notifications (alerts).
    """

    try:
        return await select([UsersInfo.user_id]).where(UsersInfo.alert == True).gino.all()
    except ArgumentError:
        return []
