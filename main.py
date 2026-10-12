import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import BotCommand

from commands import add, delete, translate, update
from config import BOT_TOKEN

bot = Bot(BOT_TOKEN)
dp = Dispatcher()

class Translator(StatesGroup):
    translate = State()
    add_1 = State()
    add_2 = State()
    update_1 = State()
    update_2 = State()
    delete = State()

async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="translate", description="Перевести слово"),
        BotCommand(command="add", description="Добавить слово"),
        BotCommand(command="update", description="Обновить слово"),
        BotCommand(command="delete", description="Удалить слово"),
        BotCommand(command="list", description="Список команд"),
    ]
    await bot.set_my_commands(commands)


@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer("Добро пожаловать. Посмотрите список доступных команды: /list")

@dp.message(Command("list"))
async def help_cmd(message: types.Message):
    await message.answer(
        "📄 Список доступных команд:\n"
        "🔎 /translate - перевести слово\n"
        "➕ /add - добавить слово в словарь\n"
        "🪄 /update - обновить слово в словаре\n"
        "🗑️ /delete - удалить слово в словаре")

@dp.message(Command("translate"))
async def translate_cmd(message: types.Message, state: FSMContext):
    await message.answer("Введи слово которое хочешь перевести.")
    await state.set_state(Translator.translate)

@dp.message(Translator.translate)
async def translate_word(message: types.Message, state: FSMContext):
    word = await translate(message.text)
    if word is None:
        await message.answer(f"'{message.text}' нет такого перевода в словаре.")
    else:
        await message.answer(f"{message.text} - {word}")
    await state.clear()

@dp.message(Command("add"))
async def add_cmd(message: types.Message, state: FSMContext):
    await message.answer("Введи слово которое хочешь добавить.")
    await state.set_state(Translator.add_1)
   
@dp.message(Translator.add_1)
async def add_part_1(message: types.Message, state: FSMContext):
    await state.update_data(word=message.text)
    await message.answer(f"Введи перевод слова '{message.text}'") 
    await state.set_state(Translator.add_2)
    
@dp.message(Translator.add_2)
async def add_part_2(message: types.Message, state: FSMContext):
    data = await state.get_data() 
    failure = await add(data["word"], message.text)
    if failure:
        await message.answer(f"'{data["word"]}' уже есть в словаре.")
    else:
        await message.answer(f"'{data["word"]}' добавлено.")
    await state.clear()

@dp.message(Command("update"))
async def update_cmd(message: types.Message, state: FSMContext):
    await message.answer("Введи слово которое хочешь обновить.")
    await state.set_state(Translator.update_1)
    
@dp.message(Translator.update_1)
async def update_part_1(message: types.Message, state: FSMContext):
    await state.update_data(word=message.text)
    await message.answer(f"Введи перевод слова '{message.text}'")
    await state.set_state(Translator.update_2)
    
@dp.message(Translator.update_2)
async def update_part_2(message: types.Message, state: FSMContext):
    data = await state.get_data()
    failure = await update(data["word"], message.text)
    if failure:
        await message.answer(f"'{data["word"]}' в словаре не найдено.")
    else:
        await message.answer(f"'{data["word"]}' обновлено.")
    await state.clear()

@dp.message(Command("delete"))
async def delete_cmd(message: types.Message, state: FSMContext):
    await message.answer("Введи слово которое хочешь удалить.")
    await state.set_state(Translator.delete)
    
@dp.message(Translator.delete)
async def delete_word(message: types.Message, state: FSMContext):
    failure = await delete(message.text)
    if failure:
        await message.answer(f"'{message.text}' в словаре не найдено.")
    else:
        await message.answer(f"'{message.text}' удалено.")
    await state.clear()
    
async def main():
    print("Бот запущен...")
    await set_commands(bot)
    await dp.start_polling(bot)
    
if __name__ == '__main__':
    asyncio.run(main())