from email import message
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
    
from aiogram.types.web_app_info import WebAppInfo


# инициализируем клавиатуру с параметром row_width=1 (Кол-во ссылок в одном ряду.)

inline_kb_full = InlineKeyboardMarkup(row_width=1)

button_news = InlineKeyboardButton('NEWS', 'https://t.me/volnarecords')
button_merch = InlineKeyboardButton('VOLNA MERCH', 'https://vk.com/market-156157044')
button_reg = InlineKeyboardButton('ONLINE REG & TICKETS', callback_data = 'reg')
donate_reg = InlineKeyboardButton('Поддержать / Donate 🏧', callback_data = 'donate')

#button_photo = (InlineKeyboardButton('Photo button', callback_data = 'photobutton'))

inline_kb_full.add(button_news, button_merch, button_reg, donate_reg)


