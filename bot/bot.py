from ast import arg, keyword
from atexit import register
from distutils import text_file
from os import sendfile
from pickle import TRUE
from posixpath import supports_unicode_filenames
from random import random
from string import printable
from tkinter import N
from unicodedata import name
from unittest import result
from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.utils.markdown import text
from aiogram.dispatcher import Dispatcher, FSMContext
from bs4 import ResultSet
from click import command
from matplotlib.text import Text
from more_itertools import first
from numpy import meshgrid, number
from regex import R
from sphinx import RemovedInNextVersionWarning
from config import TOKEN, ADMIN
import random

import keyboard as kb
import kbadmin
import logging
from aiogram.utils.markdown import hide_link
from telegram import ParseMode
import config
import sqlite3
import re
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup

from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

# connect data.db

con = sqlite3.connect('data.db', check_same_thread=False)
cur = con.cursor() 


class SQLither:
    
    def __init__(self, data):
        self.conn = sqlite3.connect(data)
        self.cur = self.conn.cursor()

    def exists_user(self, user_id):
        'exists user in data'
        return (self.cur.execute("SELECT * FROM test WHERE user_id=?", (user_id, ))).fetchone()
    
    def exists_list(self, user_id):
        'exists user in list'
        return (self.cur.execute('SELECT * FROM list WHERE user_id=?', (user_id, ))).fetchone()
    
    def add_to_list(self, user_id, username, realname, surname):
        'add user to list'
        self.cur.execute("INSERT INTO list (user_id, username, realname, surname) VALUES(?,?,?,?)", (user_id, username, realname, surname))
        self.conn.commit()

    def add_to_db(self, user_id, username, firstname, lastname):
        'add user to data'
        self.cur.execute("INSERT INTO test (user_id, username, firstname, lastname) VALUES(?,?,?,?)", (user_id, username, firstname, lastname))
        self.conn.commit()
        
    def add_0_to_status_id(self): # open reg
        'add_0_to_status_id'
        self.cur.execute("INSERT INTO reg (status_id) VALUES(0)")
        self.conn.commit()
         
    def add_1_to_status_id(self): # closed reg
        'add_1_to_status_id'
        self.cur.execute("INSERT INTO reg (status_id) VALUES(1)")
        self.conn.commit()       
        
    def last_value(self):
        'exists last_value in data'
        #return self.cur.execute("SELECT * FROM reg WHERE status_id=?").fetchone()
        return self.cur.execute("SELECT *, LAST_VALUE(status_id) OVER (ORDER BY status_id) FROM reg").fetchone()
    
        
        
    
    
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
db = SQLither("data.db")

# Admin menu start

Admin = ADMIN

@dp.message_handler(commands='admin')
async def admin_menu(message: types.Message):
    if message.from_user.id == ADMIN:
        await message.answer('Это меню управления ботом. \n\nЗдесь можно получить список всех зарегистрировавшихся нажав "Показать список", \
а потом выбрать из них рандомом несколько человек (Розыгрыш). \
\n\nТак же можно скачать всю базу данных (в ней два списка: Всех, кто когда-либо использовал бот, и список всех, кто зарегистрировался) \
\n\nЕще здесь можно включить или выключить возможность регистрации, что в главном меню. Или же изменить сообщение, которое высвечивается \
при нажатии кнопки регистрации. \
\n \nВыберите действие:', reply_markup=kbadmin.menu)
    else:
        await message.answer('Доступ запрещён!')
        
# buttons 

class Adminmenu(StatesGroup):
    view = State() 

#viewbutton

@dp.callback_query_handler(text_contains = 'viewbutton')
async def viewlist(message: types.CallbackQuery):
    if message.from_user.id == ADMIN:
        if message.data == 'viewbutton': # see all registered users
            sql = ("SELECT realname, surname, username FROM list")
            cur.execute(sql)
            results = cur.fetchall()
        
        n = '\n'.join(sorted(map(' '.join, results))) # 'a1,a2,a3;b1,b2,b3' преобразование всего кортежа results в отдельные строки
        print(n)

        await bot.send_message(chat_id=message.message.chat.id, text = n) # вывод из кортежа без скобок (преобразовано в строку)
        await bot.send_message(chat_id=message.message.chat.id, text = 'Всего зарегистрировалось: 'f'{len(results)}')
        await message.answer() 

# savebutton        

@dp.callback_query_handler(text_contains = 'savebutton')
async def savelist(message: types.CallbackQuery):
    if message.from_user.id == ADMIN:
        if message.data == 'savebutton': # bot send database
            print('loading database')
            await bot.send_document(chat_id=message.message.chat.id, document=open('/Users/artem/Documents/Python projects/tgbot1/app/data.db', 'rb'))
            print('successfull')
            await message.answer() 
        
# randombutton     

@dp.callback_query_handler(text_contains = 'randombutton')
async def input_winnernum(message: types.CallbackQuery):
    if message.from_user.id == ADMIN:
        if message.data == 'randombutton':
            await bot.send_message(chat_id=message.message.chat.id, text='Сколько будет победителей?', reply_markup = kbadmin.winmenu)
            await message.answer() 

@dp.callback_query_handler(text_contains = 'onebutton')
async def input_winnernum1(message: types.CallbackQuery):
    if message.data == 'onebutton':
        sql = ("SELECT realname, surname, username FROM list")
        cur.execute(sql)
        results = cur.fetchall()
        list = results
        wins = random.sample(list,1)
        winsstr = '\n'.join(map(' '.join, wins)) # 'a1,a2,a3;b1,b2,b3' преобразование всего кортежа wins в отдельные строки
        await bot.send_message(chat_id=message.message.chat.id, text=winsstr)
        await message.answer() 
        
@dp.callback_query_handler(text_contains = 'twobutton')
async def input_winnernum2(message: types.CallbackQuery):
    if message.data == 'twobutton':
        sql = ("SELECT realname, surname, username FROM list")
        cur.execute(sql)
        results = cur.fetchall()
        list = results
        wins = random.sample(list,2)
        winsstr = '\n'.join(map(' '.join, wins)) # 'a1,a2,a3;b1,b2,b3' преобразование всего кортежа wins в отдельные строки
        await bot.send_message(chat_id=message.message.chat.id, text=winsstr)
        await message.answer()
        
@dp.callback_query_handler(text_contains = 'threebutton')
async def input_winnernum3(message: types.CallbackQuery):
    if message.data == 'threebutton':
        sql = ("SELECT realname, surname, username FROM list")
        cur.execute(sql)
        results = cur.fetchall()
        list = results
        wins = random.sample(list,3)
        winsstr = '\n'.join(map(' '.join, wins)) # 'a1,a2,a3;b1,b2,b3' преобразование всего кортежа wins в отдельные строки
        await bot.send_message(chat_id=message.message.chat.id, text=winsstr)
        await message.answer()  
        
# on/off registration button     

@dp.callback_query_handler(text_contains = 'regbutton')
async def regbutton(message: types.CallbackQuery):
    if message.data == 'regbutton':
        if message.from_user.id == ADMIN:
            await bot.send_message(chat_id=message.message.chat.id, text='Меню закрытия регистрации \n \
                \nС помощью кнопки Дата и время закрытия можно настроить параметры автоматического отключения регистрации. \
После закрытия регистрации в назначенное время вам придет уведомление о закрытии регистрации, а так же список \
всех зарегистрированных.\n \nПосле нажатия кнопки Закрыть список сейчас - отключается дальнейшая возможность регистрации \
новых пользователей.', reply_markup = kbadmin.close_menu)
            await message.answer()
            
# change date & time for reg button

@dp.callback_query_handler(text_contains = 'close_reg_button')
async def close_reg_button(message: types.CallbackQuery):
    if message.data == 'close_reg_button':
        time2 = InlineKeyboardMarkup(row_with = 3)
        print(time2)
        minutes = ['00']
        for hours in range(18, 21):
            for mins in minutes:                                                
                time2.insert(InlineKeyboardButton(f'{hours}:{mins}', callback_data = f'time_{hours}{mins}'))
        await bot.send_message(chat_id=message.message.chat.id, text='Выберите дату и время закрытия списка. В выбранное время вам придет уведомление об успешном завершении регистрации.', reply_markup = time2)
        await message.answer()
        
# close reg now button
@dp.callback_query_handler(text_contains = 'close_now')
async def close_now(message: types.CallbackQuery):
    if message.data == 'close_now':

        
        if db.last_value() != 1:
            db.add_1_to_status_id() #status_id '1' added to table 'reg'
            await bot.send_message(chat_id=message.message.chat.id, text='Регистрация отключена.')
        else:
            db.add_0_to_status_id()  #status_id '0' added to table 'reg'
            await bot.send_message(chat_id=message.message.chat.id, text='Регистрация включена.')

        await message.answer()
            

# start bot & reg user in database

@dp.message_handler(commands='start')
async def start_command(message: types.Message):
    user_id = message.chat.id 
    username = 't.me/' + f'{message.from_user.username}'
    firstname = message.from_user.first_name
    lastname = message.from_user.last_name
    await message.answer("🌊 VOLNA SUPPORT BOT 🌊", reply_markup=kb.inline_kb_full)
    if not db.exists_user(user_id):
        db.add_to_db(user_id, username, firstname, lastname)

# name registration input:

class Form(StatesGroup):
    firstname = State() 
    lastname = State()

@dp.callback_query_handler(text_contains = 'reg')
async def input_name(message: types.CallbackQuery):
    if message.data == 'reg':
        if not db.exists_list(message.message.chat.id):
            await State.set(Form.firstname) # вводим имя
            await message.answer(text='')
            await bot.send_message(chat_id=message.message.chat.id, text='VOLNA 1.06.22 @ Cargocult\n \nДля регистрации введите своё имя.')
        else:
            await message.answer('Вы уже зарегистрированы')
        
# next def name reply

@dp.message_handler(state=Form.firstname)
async def input_surname(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['firstname'] = message.text
    await Form.lastname.set() # вводим фамилию
    await message.answer(text='И свою фамилию.')
    
# save surname and save all data to list

@dp.message_handler(state=Form.lastname)
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['lastname'] = message.text
    user_id = message.chat.id
    username = 't.me/' + f'{message.from_user.username}'
    realname = data['firstname']
    surname = message.text
    if not db.exists_list(user_id):
        db.add_to_list(user_id, username, realname, surname) #data added in db
    await state.finish()
    print(' --- [successful...] --- ')
    await message.answer(text='Спасибо. Вы в списке. 🤳 Чтобы попасть на мероприятие, назовите на входе имя и фамилию. Для возврата в главное меню нажмите /start.')

# Инлайт кнопка с hide-линком на pic        

#@dp.callback_query_handler()
#async def online_reg_command(message: types.CallbackQuery):
#    if message.data == 'photobutton':
#        await bot.edit_message_text(chat_id=message.message.chat.id, \
#            message_id=message.message.message_id, text = hide_link('https://i1.sndcdn.com/avatars-000387120755-h9ztcs-t500x500.jpg'), \
#                parse_mode=ParseMode.HTML, reply_markup = kb.button_test)

@dp.callback_query_handler(text_contains = 'donate')
async def donate (message: types.CallbackQuery):
    if message.data == 'donate':
            await bot.send_message(chat_id=message.message.chat.id, text='Поддержать / Donate \n \n➡ 4565 6666 6666 6666 (Сбер / Тинькофф)')

            
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)



    
