from database import UsersInfo


async def update_user_alert(user_id: int, alert: bool) -> None:
    """update alert for user in database.

    Args:
        user_id (int): Telegram user id.
        alert (str): True - alert is on, False - alert is off.
    """

    await UsersInfo.update.values(alert=alert) \
        .where(UsersInfo.user_id == user_id).gino.status()
