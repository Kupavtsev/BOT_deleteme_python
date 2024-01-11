from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton


choice = InlineKeyboardMarkup(row_width=2)

accept = InlineKeyboardButton(text='Подтвердить', callback_data='accept')
choice.insert(accept)

reject = InlineKeyboardButton(text='Заполнить заново', callback_data='reject')
choice.insert(reject)



key_words = InlineKeyboardMarkup(row_width=2)

corruption = InlineKeyboardButton(text='Коррупция', callback_data='corruption')
blackmailing = InlineKeyboardButton(text='Шантаж', callback_data='blackmailing')
scandal = InlineKeyboardButton(text='Скандал', callback_data='scandal')
rob = InlineKeyboardButton(text='Воровство', callback_data='rob')
con = InlineKeyboardButton(text='Мошенник', callback_data='con')
suspect = InlineKeyboardButton(text='Подозревается', callback_data='suspect')
invest = InlineKeyboardButton(text='Расследование', callback_data='invest')
caught = InlineKeyboardButton(text='Задержан', callback_data='caught')
cheat = InlineKeyboardButton(text='Измена', callback_data='cheat')
sliv = InlineKeyboardButton(text='Слив', callback_data='sliv')
intim = InlineKeyboardButton(text='Интим', callback_data='intim')
spam = InlineKeyboardButton(text='Спам', callback_data='spam')
accept = InlineKeyboardButton(text='Подтвердить', callback_data='accept')

arr = [corruption, blackmailing, scandal, rob, con, suspect, invest, caught, cheat, sliv, intim, spam, accept]

for i in arr:
    key_words.insert(i)



choice2 = InlineKeyboardMarkup(row_width=1).row(InlineKeyboardButton(text='Добавить новые', callback_data='add')).row(InlineKeyboardButton(text='Удалить все и добавить новые', callback_data='delete'))

# choice2 = InlineKeyboardMarkup(row_width=1).row(
#     InlineKeyboardButton(text='Произвести поиск по заданным словам', callback_data='search'),
# ).row(InlineKeyboardButton(text='Добавить новые', callback_data='add')).row(InlineKeyboardButton(text='Удалить все и добавить новые', callback_data='delete'))


# reject = InlineKeyboardButton(text='Добавить новые', callback_data='reject')
# choice.insert(reject)