import asyncio
import os
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardMarkup, KeyboardButton
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums import ParseMode

API_TOKEN = '7621791983:AAHCImD9kmHDfg3r1DK4dRvB1sSyPeZmwHQ'

bot = Bot(
    token=API_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()

control = {"feature": False}
app = FastAPI()

@app.get("/status")
async def get_status():
    return JSONResponse(content=control)

main_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="⚙ Включить фичу"), KeyboardButton(text="⚙ Выключить фичу")],
    [KeyboardButton(text="⚙ Статус фичи")]
], resize_keyboard=True)

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

async def main():
    asyncio.create_task(dp.start_polling(bot))
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    config = uvicorn.Config(app, host="0.0.0.0", port=port, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()

if __name__ == "__main__":
    asyncio.run(main())
