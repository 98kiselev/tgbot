from aiogram import Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from pymongo import MongoClient
from flask import Flask

app = Flask(__name__)

# Create the client
client = MongoClient('localhost', 27017)

# Connect to our database
db = client['zakaz']

# Fetch our series collection
stol_collection = db['stol']


@app.route('/')
def hello():
    return 'stol_collection.find()'

TOKEN = "2127256365:AAHEYdBqkcg9piAvxvvRaxewAeSbRaNornE"
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
button_yes = KeyboardButton('Да')
button_no = KeyboardButton('Нет')
greet_kb1 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
greet_kb1.add(button_yes)
greet_kb1.add(button_no)

keyboard = InlineKeyboardMarkup()
menu_1 = InlineKeyboardButton(text='Стол 1', callback_data="menu_1")
menu_2 = InlineKeyboardButton(text='Стол 2', callback_data="menu_2")
menu_3 = InlineKeyboardButton(text='Стол 3', callback_data="menu_3")
menu_4 = InlineKeyboardButton(text='Стол 4', callback_data="menu_4")
menu_5 = InlineKeyboardButton(text='Стол 5', callback_data="menu_5")
menu_6 = InlineKeyboardButton(text='Стол 6', callback_data="menu_6")
menu_7 = InlineKeyboardButton(text='Стол 7', callback_data="menu_7")
menu_8 = InlineKeyboardButton(text='Стол 8', callback_data="menu_8")
menu_9 = InlineKeyboardButton(text='Стол 9', callback_data="menu_9")
menu_10 = InlineKeyboardButton(text='Стол 10', callback_data="menu_10")
keyboard.add(menu_1, menu_2, menu_3, menu_4, menu_5, menu_6, menu_7, menu_8, menu_9, menu_10)

# greet_kb1 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add([button_yes,button_no])

class reg(StatesGroup):
    name = State()
    stol = State()

dp = Dispatcher(bot, storage=MemoryStorage())

@dp.message_handler(commands='start')
async def send_welcome(msg):
    await msg.answer('Привет! Чтобы продолжить, введи имя и фамилию.')

@dp.message_handler(content_types=['text'])
async def get_text_messages(msg: types.Message, state: FSMContext):
   if msg.text=='Да':
       await msg.answer('Выбери столик:\n Стол 1. Анненков Павел. Тренды десителетия\n Стол 2. Роман Копосов. Длинные тренды \n Стол 3. Ярослав Савин. Дробление бизнеса\n Стол 4 Дмитрий Мишин. Тренды в маркетинге. \n Стол 5. Дмитрий Зацепин. Тренды в развитии орг структур\n Стол 6. Эдуард Шмидт. Тренды в управлении продажами\n Стол 7. Вероника Шкарбань. Тренды работы с командой. Как вовлекать \n Стол 8. Борис Комендантов. Куда лучше инвестировать в 2022 году\n Стол 9. Киларь Наталья. Как искать таланты и удержать их \n Стол 10. Константин Шихалёв. Забота о здоровье. Тренд или рутина. ',reply_markup=keyboard)
   elif msg.text=='Нет':
       await msg.answer('Введи имя и фамилию еще раз')
   else :
       await msg.answer('Ты '+msg.text+'?',reply_markup=greet_kb1)
       await state.update_data(name=msg.text)


@dp.callback_query_handler(text_contains='menu_')
async def menu(call: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    print(user_data['name'])
    if call.data and call.data.startswith("menu_"):
        code = call.data[-1:]
        print(code)
        new_stol = {
            "name": user_data['name'],
            "stol": int(code)
        }
        stol_collection.insert_one(new_stol)
        if code.isdigit():
            code = int(code)
        if code == 1:
            await call.message.edit_text('Выбран стол 1')
        if code == 2:
            await call.message.edit_text('Выбран стол 2')
        if code == 3:
            await call.message.edit_text('Выбран стол 3')
        if code == 4:
            await call.message.edit_text('Выбран стол 4')
        if code == 5:
            await call.message.edit_text('Выбран стол 5')
        if code == 6:
            await call.message.edit_text('Выбран стол 6')
        if code == 7:
            await call.message.edit_text('Выбран стол 7')
        if code == 8:
            await call.message.edit_text('Выбран стол 8')
        if code == 9:
            await call.message.edit_text('Выбран стол 9')
        if code == 10:
            await call.message.edit_text('Выбран стол 10')

        else:
            await bot.answer_callback_query(call.id)


if __name__ == '__main__':
   executor.start_polling(dp)

