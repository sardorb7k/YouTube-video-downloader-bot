from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

choice = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='video 📺', callback_data="video"), InlineKeyboardButton(text='audio 🔉', callback_data="audio")]
    ]
)