from aiogram.fsm.state import State, StatesGroup

class Download(StatesGroup):
    url = State()