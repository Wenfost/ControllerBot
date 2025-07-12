import asyncio
import json
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardMarkup, KeyboardButton

API_TOKEN = '7621791983:AAHCImD9kmHDfg3r1DK4dRvB1sSyPeZmwHQ'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Память с флагами
control = {"feature": False}

# FastAPI
app = FastAPI()

# HTTP endpoint для Lua
@app.get("/status")
async def get_status():
    return JSONResponse(content=control)

# Клавиатура
main_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="⚙ Включить фичу"), KeyboardButton(text="⚙ Выключить фичу")],
    [KeyboardButton(text="⚙ Статус фичи")]
], resize_keyboard=True)

# Команды
@dp.message(Command("start"))
async def start(message: Message):
    await message.answer("Привет! Бот + API для Lua", reply_markup=main_kb)

@dp.message(lambda m: m.text == "⚙ Включить фичу")
async def enable_feature(message: Message):
    control["feature"] = True
    await message.answer("✅ Фича включена!")

@dp.message(lambda m: m.text == "⚙ Выключить фичу")
async def disable_feature(message: Message):
    control["feature"] = False
    await message.answer("⛔ Фича выключена!")

@dp.message(lambda m: m.text == "⚙ Статус фичи")
async def status_feature(message: Message):
    state = "✅ Включена" if control["feature"] else "⛔ Выключена"
    await message.answer(f"⚙ Фича сейчас: {state}")

# Запуск
async def main():
    # Запускаем aiogram
    asyncio.create_task(dp.start_polling(bot))
    # Запускаем FastAPI
    import uvicorn
    config = uvicorn.Config(app, host="127.0.0.1", port=8000, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()

if __name__ == "__main__":
    asyncio.run(main())
