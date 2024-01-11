from aiogram.dispatcher.filters.state import StatesGroup, State


class AuthState(StatesGroup):
    name = State()
    surname = State()
    patronymic = State()
    date_of_birth = State()
    phone = State()
    city = State()


class SearchState(StatesGroup):
    key_words = State()
    amount = State()


class SearchStateUn(StatesGroup):
    key_words = State()
    amount = State()


