from aiogram.dispatcher.filters.state import StatesGroup, State


class ViewReviewsStatesGroup(StatesGroup):
    view_reviews_menu = State()
    enter_limit_view_reviews = State()
    view_review = State()
    confirm_delete_review = State()
