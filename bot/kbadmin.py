from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
    
menu = InlineKeyboardMarkup(row_width=1)
viewlist = InlineKeyboardButton("Показать список", callback_data = 'viewbutton')
winners = InlineKeyboardButton("Выбрать победителей", callback_data = 'randombutton')

winmenu = InlineKeyboardMarkup(row_width = 3)
one = InlineKeyboardButton("1", callback_data = 'onebutton')
two = InlineKeyboardButton("2", callback_data = 'twobutton')
three = InlineKeyboardButton("3", callback_data = 'threebutton')

winmenu.add(one, two, three)

savelist = InlineKeyboardButton("Скачать базу данных", callback_data = 'savebutton')
on_off_reg = InlineKeyboardButton("ON / OFF регистрация", callback_data = 'regbutton')
edit_textreg = InlineKeyboardButton("Изменить текст кнопки регистрации", callback_data = 'editregbutton')

close_menu = InlineKeyboardMarkup(row_width = 1)
close_reg = InlineKeyboardButton("Дата и время закрытия", callback_data = 'close_reg_button')
close_now = InlineKeyboardButton("Закрыть список сейчас", callback_data = 'close_now')

close_menu.add(close_reg, close_now)

menu.add(viewlist, winners, savelist, on_off_reg, edit_textreg)
