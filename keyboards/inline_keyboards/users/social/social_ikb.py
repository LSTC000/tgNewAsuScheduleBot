from data.config import ROW_WIDTH

from data.callbacks import CANCEL_TO_MAIN_MENU_CALLBACK_DATA

from data.messages import (
    CANCEL_TO_MAIN_MENU_IKB_MESSAGE,
    ASU_OFFICIAL_WEB_URL_IKB_MESSAGE,
    ASU_TELEGRAM_NEWS_URL_IKB_MESSAGE,
    ASU_VK_NEWS_URL_IKB_MESSAGE,
    ASU_OK_NEWS_URL_IKB_MESSAGE,
    ASU_DZEN_NEWS_URL_IKB_MESSAGE,
    ASU_RUTUBE_NEWS_URL_IKB_MESSAGE,
)

from data.urls import (
    ASU_OFFICIAL_WEB_URL, 
    ASU_TELEGRAM_NEWS_URL, 
    ASU_VK_NEWS_URL,
    ASU_OK_NEWS_URL,
    ASU_DZEN_NEWS_URL,
    ASU_RUTUBE_NEWS_URL,
)

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def social_ikb() -> InlineKeyboardMarkup:
    """
    Returns:
        InlineKeyboardMarkup: Social inline keyboard.
    """

    ikb = InlineKeyboardMarkup(row_width=ROW_WIDTH)

    ikb.row(InlineKeyboardButton(
        text=ASU_OFFICIAL_WEB_URL_IKB_MESSAGE,
        url=ASU_OFFICIAL_WEB_URL)
    )
    ikb.row(InlineKeyboardButton(
        text=ASU_TELEGRAM_NEWS_URL_IKB_MESSAGE,
        url=ASU_TELEGRAM_NEWS_URL)
    )
    ikb.row(InlineKeyboardButton(
        text=ASU_VK_NEWS_URL_IKB_MESSAGE, 
        url=ASU_VK_NEWS_URL)
    )
    ikb.row(InlineKeyboardButton(
        text=ASU_OK_NEWS_URL_IKB_MESSAGE,
        url=ASU_OK_NEWS_URL)
    )
    ikb.row(InlineKeyboardButton(
        text=ASU_DZEN_NEWS_URL_IKB_MESSAGE,
        url=ASU_DZEN_NEWS_URL)
    )
    ikb.row(InlineKeyboardButton(
        text=ASU_RUTUBE_NEWS_URL_IKB_MESSAGE,
        url=ASU_RUTUBE_NEWS_URL)
    )
    ikb.row(InlineKeyboardButton(
        text=CANCEL_TO_MAIN_MENU_IKB_MESSAGE, 
        callback_data=CANCEL_TO_MAIN_MENU_CALLBACK_DATA)
    )

    return ikb
