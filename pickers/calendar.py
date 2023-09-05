import calendar

from datetime import datetime, timedelta

from data.callbacks import (
    IGNORE_CALLBACK_DATA,
    PREV_YEAR_CALLBACK_DATA,
    NEXT_YEAR_CALLBACK_DATA,
    PREV_MONTH_CALLBACK_DATA,
    NEXT_MONTH_CALLBACK_DATA,
    CANCEL_TO_SCHEDULE_MENU_CALLBACK_DATA
)

from data.messages import CANCEL_TO_SCHEDULE_MENU_IKB_MESSAGE

from data.redis import CALENDAR_DATE_REDIS_KEY

from data.config import RU_MONTH_NAME

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class Calendar:
    async def start_calendar(self, year: int, month: int, state: FSMContext) -> InlineKeyboardMarkup:
        # Create a dictionary in the user memory storage for storing the year and month.
        async with state.proxy() as data:
            data[CALENDAR_DATE_REDIS_KEY] = {
                'year': year,
                'month': month
            }

        inline_kb = InlineKeyboardMarkup(row_width=7)

        # First row - Month and Year.
        inline_kb.row()
        inline_kb.insert(InlineKeyboardButton(
            text="<<",
            callback_data=PREV_YEAR_CALLBACK_DATA
        ))
        inline_kb.insert(InlineKeyboardButton(
            text=f'{RU_MONTH_NAME[calendar.month_name[month]]} {str(year)}',
            callback_data=IGNORE_CALLBACK_DATA
        ))
        inline_kb.insert(InlineKeyboardButton(
            text=">>",
            callback_data=NEXT_YEAR_CALLBACK_DATA
        ))

        # Second row - Week Days.
        inline_kb.row()
        for day in ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]:
            inline_kb.insert(InlineKeyboardButton(text=day, callback_data=IGNORE_CALLBACK_DATA))

        # Calendar rows - Days of month.
        month_calendar = calendar.monthcalendar(year, month)
        for week in month_calendar:
            inline_kb.row()
            for day in week:
                if day == 0:
                    inline_kb.insert(InlineKeyboardButton(text=" ", callback_data=IGNORE_CALLBACK_DATA))
                    continue
                inline_kb.insert(InlineKeyboardButton(text=str(day), callback_data=str(day)))

        # Last row - Buttons.
        inline_kb.row()
        inline_kb.insert(InlineKeyboardButton(
            text="<", callback_data=PREV_MONTH_CALLBACK_DATA
        ))
        inline_kb.insert(InlineKeyboardButton(text=" ", callback_data=IGNORE_CALLBACK_DATA))
        inline_kb.insert(InlineKeyboardButton(
            text=">", callback_data=NEXT_MONTH_CALLBACK_DATA
        ))

        inline_kb.row(InlineKeyboardButton(
            text=CANCEL_TO_SCHEDULE_MENU_IKB_MESSAGE,
            callback_data=CANCEL_TO_SCHEDULE_MENU_CALLBACK_DATA)
        )

        return inline_kb

    async def process_selection(self, callback: types.CallbackQuery, callback_data: str, state: FSMContext) -> tuple:
        return_data = (False, None)

        async with state.proxy() as data:
            year = int(data[CALENDAR_DATE_REDIS_KEY]['year'])
            month = int(data[CALENDAR_DATE_REDIS_KEY]['month'])
            temp_date = datetime(year, month, 1)

        if callback_data == IGNORE_CALLBACK_DATA:
            await callback.answer(cache_time=60)
        elif callback_data == PREV_YEAR_CALLBACK_DATA:
            prev_date = temp_date - timedelta(days=365)
            await callback.message.edit_reply_markup(
                await self.start_calendar(year=int(prev_date.year), month=int(prev_date.month), state=state)
            )
        elif callback_data == NEXT_YEAR_CALLBACK_DATA:
            next_date = temp_date + timedelta(days=365)
            await callback.message.edit_reply_markup(
                await self.start_calendar(year=int(next_date.year), month=int(next_date.month), state=state)
            )
        elif callback_data == PREV_MONTH_CALLBACK_DATA:
            prev_date = temp_date - timedelta(days=1)
            await callback.message.edit_reply_markup(
                await self.start_calendar(year=int(prev_date.year), month=int(prev_date.month), state=state)
            )
        elif callback_data == NEXT_MONTH_CALLBACK_DATA:
            next_date = temp_date + timedelta(days=31)
            await callback.message.edit_reply_markup(
                await self.start_calendar(year=int(next_date.year), month=int(next_date.month), state=state)
                )
        else:
            return_data = True, datetime(year, month, int(callback_data)).strftime('%Y%m%d')

        return return_data
