from database import get_users_alert

from loader import bot, logger

from aiogram.utils.exceptions import (
    BotBlocked,
    ChatNotFound,
    UserDeactivated,
    MigrateToChat,
    Unauthorized,
    BadRequest,
    RetryAfter
)


async def send_alert(
    text_alert: str,
    disable_notification: bool = True
) -> None:
    """send alert for users.

    Args:
        text_alert (str): Text for alert.
        disable_notification (bool, optional): Disable notification (check aiogram documentation). Defaults to True.
    """

    users_alert = await get_users_alert()

    for user_alert in users_alert:
        user_id = user_alert[0]
        try:
            await bot.send_message(
                chat_id=user_id,
                text=text_alert,
                disable_notification=disable_notification
            )
        except (BotBlocked, ChatNotFound, UserDeactivated, MigrateToChat, Unauthorized, BadRequest, RetryAfter):
            logger.info('Error to send users alert!')
