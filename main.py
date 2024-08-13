import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InputFile
from config import token
from state import Download
from pytube import YouTube
from button import choice
import os

logging.basicConfig(level=logging.INFO)
bot = Bot(token=token)
dp = Dispatcher(storage=MemoryStorage())

@dp.message(Command('start'))
async def start_command(message: types.Message, state: FSMContext):
    await state.set_state(Download.url)
    await message.answer(
        text=f"Salom <b>{message.from_user.full_name}</b>!\nMenga video havolasini jo'nating.",
        parse_mode="HTML",
    )

@dp.message(Download.url)
async def handle_video_url(message: types.Message, state: FSMContext):
    video_url = message.text
    await state.update_data(url=video_url)
    await message.answer_photo(photo=video_url, reply_markup=choice)

@dp.callback_query(F.data == 'audio')
async def send_video_callback(call: CallbackQuery, state: FSMContext):
    await call.message.answer("🙏 Iltimos biroz kuting...")
    data = await state.get_data()
    video_url = data.get('url')
    yt = YouTube(video_url)
    stream = yt.streams.get_highest_resolution()
    video_file = stream.download()
    
    try:
        audio = types.FSInputFile(path=video_file, filename=video_file)
        await call.message.answer_audio(audio=audio)
        os.remove(video_file)
    except Exception as e:
        logging.error(f"Error downloading video: {e}")
        await call.message.answer("Failed to download video. Please try again.")
    await state.set_state(Download.url)

@dp.callback_query(F.data == 'video')
async def send_video_callback(call: CallbackQuery, state: FSMContext):
    await call.message.answer("🙏 Iltimos biroz kuting...")
    data = await state.get_data()
    video_url = data.get('url')
    yt = YouTube(video_url)
    stream = yt.streams.get_highest_resolution()
    video_file = stream.download()
    
    try:
        video = types.FSInputFile(path=video_file, filename=video_file)
        await call.message.answer_video(video=video)
        os.remove(video_file)
    except Exception as e:
        logging.error(f"Error downloading video: {e}")
        await call.message.answer("Failed to download video. Please try again.")
    await state.set_state(Download.url)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())