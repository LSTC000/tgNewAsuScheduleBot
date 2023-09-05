from data.redis import CHAT_GPT_HISTORY_REDIS_KEY

from data.config import (
    CHAT_GPT_TOKEN,
    MODEL,
    MAX_TOKENS,
    TEMPERATURE,
    CHAT_GPT_ROLE,
    CHAT_GPT_ASSISTANT_SYSTEM_MESSAGE,
    MAX_CHAT_GPT_CONTENT_LENGTH,
    MAX_CHAT_GPT_HISTORY_LENGTH,
)

from data.messages import (
    START_CHAT_GPT_WORK_MESSAGE,
    LIMIT_CHAT_GPT_HISTORY_LENGTH_MESSAGE,
    LIMIT_CHAT_GPT_MAX_CONTENT_LENGTH_MESSAGE,
    VOICE_TO_TEXT_CONVERT_ERROR_MESSAGE,
    CHAT_GPT_ERROR_MESSAGE,
)

from functions import voice_to_text_convert, clear_last_ikb, call_chat_gpt_menu_ikb

from loader import dp, bot, logger, chat_gpt_stt

from states import ChatGptStatesGroup

from aiogram import types
from aiogram.dispatcher import FSMContext

import openai


openai.api_key = CHAT_GPT_TOKEN


@dp.message_handler(
    content_types=[types.ContentType.TEXT, types.ContentType.VOICE],
    state=ChatGptStatesGroup.chat_gpt_menu
)
async def chat_gpt_response(message: types.Message, state: FSMContext) -> None:
    user_id = message.from_user.id

    # Clear last inline keyboard.
    await clear_last_ikb(user_id=user_id, state=state)

    # If the message is voice then we process it.
    if message.content_type == 'voice':
        content = await voice_to_text_convert(
            user_id=user_id,
            file_id=message.voice.file_id,
            stt=chat_gpt_stt
        )
    else:
        # Check if the MAX_CONTENT_LENGTH is exceeded.
        content = message.text if len(message.text) <= MAX_CHAT_GPT_CONTENT_LENGTH else None
    # If we failed to process a voice message or the MAX_CONTENT_LENGTH was exceeded, then we send a message about it.
    if content is None:
        if message.content_type == 'voice':
            await bot.send_message(chat_id=user_id, text=VOICE_TO_TEXT_CONVERT_ERROR_MESSAGE)
        else:
            await bot.send_message(
                chat_id=user_id,
                text=LIMIT_CHAT_GPT_MAX_CONTENT_LENGTH_MESSAGE.format(MAX_CHAT_GPT_CONTENT_LENGTH)
            )
    else:
        msg = await bot.send_message(chat_id=user_id, text=START_CHAT_GPT_WORK_MESSAGE)

        async with state.proxy() as data:
            try:
                # Add the user message to the history of the ChatGPT dialog.
                data[CHAT_GPT_HISTORY_REDIS_KEY].append({"role": "user", "content": content})
                # Send a request to receive a response from ChatGPT.
                response = await openai.ChatCompletion.acreate(
                    model=MODEL,
                    messages=data[CHAT_GPT_HISTORY_REDIS_KEY],
                    temperature=TEMPERATURE
                )
                # Delete start ChatGPT work message.
                await bot.delete_message(chat_id=user_id, message_id=msg.message_id)
                # If the response from ChatGPT has arrived then add it to the history of the dialog.
                # And assign a message counter to the response.
                content = response['choices'][0]['message']['content']
                data[CHAT_GPT_HISTORY_REDIS_KEY].append({"role": CHAT_GPT_ROLE, "content": content})
                content = f"{len(data[CHAT_GPT_HISTORY_REDIS_KEY]) // 2}/{MAX_CHAT_GPT_HISTORY_LENGTH}: " + content
                # Counting length.
                content_length = len(content)
                # If the number of tokens is greater than the MAX_TOKENS.
                # Then we split the response from ChatGPT into several parts.
                if content_length > MAX_TOKENS:
                    for i in range(0, content_length, MAX_TOKENS):
                        if content_length - i > MAX_TOKENS:
                            text = content[i:(MAX_TOKENS * (i + 1))]
                            await bot.send_message(chat_id=message.from_user.id, text=text, parse_mode='')
                        else:
                            text = content[i:content_length]
                            await bot.send_message(chat_id=message.from_user.id, text=text, parse_mode='')
                else:
                    await bot.send_message(chat_id=message.from_user.id, text=content, parse_mode='')
                # If the message limit for one dialog with ChatGPT is reached.
                # Then we clear it and send a message to the user about it.
                if len(data[CHAT_GPT_HISTORY_REDIS_KEY]) // 2 == MAX_CHAT_GPT_HISTORY_LENGTH:
                    data[CHAT_GPT_HISTORY_REDIS_KEY].clear()
                    data[CHAT_GPT_HISTORY_REDIS_KEY].append(CHAT_GPT_ASSISTANT_SYSTEM_MESSAGE)
                    await bot.send_message(
                        chat_id=user_id,
                        text=LIMIT_CHAT_GPT_HISTORY_LENGTH_MESSAGE.format(MAX_CHAT_GPT_HISTORY_LENGTH)
                    )
            except Exception as ex:
                logger.info(f'Error to ChatGPT: {ex}')
                await message.reply(text=CHAT_GPT_ERROR_MESSAGE)

    # Call ChatGPT inline menu.
    await call_chat_gpt_menu_ikb(user_id=user_id, state=state)
