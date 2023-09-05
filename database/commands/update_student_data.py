from database import UsersInfo


async def update_student_data(user_id: int, student_name: str, student_url: str) -> None:
    """update student data for user in database.

    Args:
        user_id (int): Telegram user id.
        student_name (str): Last student name.
        student_url (str): Last student schedule url.
    """

    await UsersInfo.update.values(student_name=student_name) \
        .where(UsersInfo.user_id == user_id).gino.status()
    
    await UsersInfo.update.values(student_url=student_url) \
        .where(UsersInfo.user_id == user_id).gino.status()
