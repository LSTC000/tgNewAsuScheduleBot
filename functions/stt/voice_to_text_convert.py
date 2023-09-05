import os
import random
from typing import Union

from data.messages import START_VOICE_TO_TEXT_CONVERT_MESSAGE

from loader import bot


async def voice_to_text_convert(user_id: int, file_id: str, stt) -> Union[str, None]:
    """
    :param user_id: Telegram user id.
    :param file_id: Telegram voice file id.
    :param stt: Stt model from loader:
        schedule_stt if you want to know the schedule,
        chat_gpt_stt if you want to talk to ChatGPT.
    :return: Text if the voice is recognized else None.
    """

    msg = await bot.send_message(chat_id=user_id, text=START_VOICE_TO_TEXT_CONVERT_MESSAGE)

    file_info = await bot.get_file(file_id)
    file_path = file_info.file_path
    file_name = f"{file_id}_{random.randint(0, 100000)}.tmp"

    await bot.download_file(file_path=file_path, destination=file_name)

    text = await stt.audio_to_text(file_name)

    os.remove(file_name)

    await bot.delete_message(chat_id=user_id, message_id=msg.message_id)

    return text if text else None
