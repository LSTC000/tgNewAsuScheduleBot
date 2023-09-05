from aiogram.dispatcher.filters.state import StatesGroup, State


class MainMenuStatesGroup(StatesGroup):
    main_menu = State()
    enter_user_review = State()
    confirm_user_review = State()
    asu_buildings = State()
    help = State()
