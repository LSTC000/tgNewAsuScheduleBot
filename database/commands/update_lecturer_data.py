from database import UsersInfo


async def update_lecturer_data(user_id: int, lecturer_name: str, lecturer_url: str) -> None:
    """update lecturer data for user in database.

    Args:
        user_id (int): Telegram user id.
        lecturer_name (str): Last lecturer name.
        lecturer_url (str): Last lecturer schedule url.
    """

    await UsersInfo.update.values(lecturer_url=lecturer_url) \
        .where(UsersInfo.user_id == user_id).gino.status()
    
    await UsersInfo.update.values(lecturer_name=lecturer_name) \
        .where(UsersInfo.user_id == user_id).gino.status()
