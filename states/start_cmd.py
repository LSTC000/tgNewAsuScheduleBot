from aiogram.dispatcher.filters.state import StatesGroup, State


class StartCmdStatesGroup(StatesGroup):
    start_ikb = State()
