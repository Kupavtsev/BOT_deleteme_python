from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.storage import RESULT
from loader import dp, bot
from .states import AuthState
from aiogram.dispatcher.filters import Command
from aiogram.types import CallbackQuery, InputFile
from keyboards.choise_buttons import choise, choise2, choise3, markup_request, choise22, button_link
import datetime, re, time
from asgiref.sync import sync_to_async
import hashlib
from urllib.parse import quote
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
import smtplib


def get_description(service, price):
    description = f'Оплата за оказание услуги "{service}". Сумма на оплату: {price} рублей'
    result = quote(description, safe='/')
    # result = description.replace(' ', '%20')
    return result


def make_hash(phone, price, telegram_id):
    hash_obj = hashlib.md5("infsectest_ru:'.{price}.':0'.':qNI1cl89rPWbFMkb9Ls0'.':Shp_phone='.{phone}.':Shp_telegram='.{telegram_id}".encode())
    return hash_obj.hexdigest()


def get_final_price(service):
    if service == 'Тест на взлом':
        price = 300
    elif service == 'Тест на утечку данных':
        price = 500
    elif service == 'Выяснить попытки взлома аккаунта':
        price = 3000
    elif service == 'Мониторинг безопасности':
        price = 5000
    elif service == 'Расследование взлома':
        price = 30000
    return price
    
def post_data_to_email():
    HOST = 'smtp.yandex.ru'
    SUBJECT = "Заказ №"
    TO = "pavel.k@dot-tech.ru"
    FROM = "order@infsectest.ru"
    text = "Python 3.4 rules them all!"
    BODY = 'hello'
    server = smtplib.SMTP(HOST)
    server.sendmail(FROM, [TO], BODY)
    server.quit()

@sync_to_async
def make_link(data):
    # $shp_item = '234234235';
    # $shp_phone = '79522329395';
    # $sum = 1;
    # $desc = urlencode('Тест на взлом: email [sjdhfkjsd@dsfsdad.ru]');
    # echo $md5 = md5('infsectest_ru:'.$sum.':0'.':qNI1cl89rPWbFMkb9Ls0'.':Shp_phone='.$shp_phone.':Shp_telegram='.$shp_item);
    # echo '<br>';
    # echo 'https://auth.robokassa.ru/Merchant/Index.aspx?MerchantLogin=infsectest_ru&InvId=0&Culture=ru&Encoding=utf-8&Shp_phone='.$shp_phone.'&Shp_telegram='.$shp_item.'&OutSum='.$sum.'&Description='.$desc.'&SignatureValue='.$md5;
    phone=data['phone']
    telegram_id=data['telegram_id']
    service=data['service']
    social_net=data['social_net']
    link=data['link']
    final_price = get_final_price(service)
    md5 = make_hash(phone, final_price, telegram_id)
    description = get_description(service, final_price)
    post_data_to_email()
    link_to_pay = f"https://auth.robokassa.ru/Merchant/Index.aspx?MerchantLogin=infsectest_ru&InvId=0&Culture=ru&Encoding=utf-8&Shp_phone='.{phone}'&Shp_telegram='.{telegram_id}'&OutSum='.{final_price}'.&Description='.{description}'.&SignatureValue='.{md5}'"
    return link_to_pay

orders_data = []
permitted = [
    'тест на взлом', 'тест на утечку данных', 'выяснить попытки взлома аккаунта', 'мониторинг безопасности', 'расследование взлома'
    ]

nets = ['vk',
'instagram',
'facebook',
'email',
'telegram',
"what's app",
'web-site',]

user_data = []
user_data_dict = {}

@dp.message_handler(Command('start'))
async def answer(message: types.Message):
    username = message.from_user.full_name
    await message.answer(f'Здравствуйте, {username}')
    await AuthState.service.set()
    await message.answer('Выберите тип услуги', reply_markup=choise)



# @dp.callback_query_handler(text_contains='vzlom')
# async def del_keywords(call: CallbackQuery, state: FSMContext):
#     await call.answer(cache_time=60)
#     await AuthState.service.set()
#     await state.update_data(service='Тест на взлом')
#     await call.message.answer('Выберите тестируемый объект', reply_markup=choise2)
#     await AuthState.next()

# @dp.callback_query_handler(text_contains='utechka')
# async def del_keywords(call: CallbackQuery, state: FSMContext):
#     await call.answer(cache_time=60)
#     await AuthState.service.set()
#     await state.update_data(service='Тест на утечку данных')
#     await call.message.answer('Выберите тестируемый объект', reply_markup=choise2)
#     await AuthState.next()

# @dp.callback_query_handler(text_contains='attempts')
# async def del_keywords(call: CallbackQuery, state: FSMContext):
#     await call.answer(cache_time=60)
#     await AuthState.service.set()
#     await state.update_data(service='Выяснить попытки взлома аккаунта')
#     await call.message.answer('Выберите тестируемый объект', reply_markup=choise2)
#     await AuthState.next()

# @dp.callback_query_handler(text_contains='safe')
# async def del_keywords(call: CallbackQuery, state: FSMContext):
#     await call.answer(cache_time=60)
#     # await AuthState.service.set()
#     await state.update_data(service='Мониторинг безопасности')
#     await call.message.answer('Выберите тестируемый объект', reply_markup=choise2)
#     # await AuthState.next()


# @dp.message_handler(state=AuthState.service)  
# @dp.callback_query_handler(text_contains='invest')
# async def del_keywords(call: CallbackQuery, state: FSMContext):
#     await call.answer(cache_time=60)
#     await AuthState.service.set()
#     data = call.message.data
#     await call.message.answer(f'data: {data}')
#     await state.update_data(service='Расследование взлома')
#     await call.message.answer('Выберите тестируемый объект', reply_markup=choise2)
#     await AuthState.next()


# @dp.callback_query_handler(text_contains='VK')
# async def add_keywords(call: CallbackQuery, state: FSMContext):
#     await call.answer(cache_time=60)
#     data = await state.get_data()
#     await call.message.answer(f'data: {data}')


@dp.message_handler(state=AuthState.service)
async def get_service(message: types.Message, state: FSMContext):
    await AuthState.service.set()
    service = message.text
    if not service.lower() in permitted:
        await message.answer('Выберите услугу из предложенных')
        return
    await state.update_data(service=service)
    await AuthState.next()
    await message.answer('Выберите тестируемый объект', reply_markup=choise2)


@dp.message_handler(state=AuthState.social_net)
async def get_social(message: types.Message, state: FSMContext):
    await AuthState.social_net.set()
    social_net = message.text
    if not social_net.lower() in nets:
        await message.answer('Выберите тестируемый объект из предложенных')
        return
    await state.update_data(social_net=social_net)
    await AuthState.next()
    await message.answer('Введите ID, login или ссылку на аккаунт')


@dp.message_handler(state=AuthState.link)
async def get_link(message: types.Message, state: FSMContext):
    await AuthState.link.set()
    link = message.text
    await state.update_data(link=link)
    # telegram_id = int(message.from_user.id)
    # data = await state.get_data()
    # user_data.append({telegram_id: data})
    # user_data_dict[telegram_id] = data
    # await state.finish()
    await AuthState.next()
    await message.answer('Введите номер телефона, привязанный к выбранному аккаунту')


@dp.message_handler(state=AuthState.phone)
async def get_phone(message: types.Message, state: FSMContext):
    phone = message.text
    try:
        phone = int(phone)
    except ValueError:
        await message.answer('Неверный формат номера')
        return
    await state.update_data(phone=phone)
    telegram_id = int(message.from_user.id)
    data = await state.get_data()
    data.setdefault('telegram_id', telegram_id)
    link = await make_link(data)
    await state.finish()
    button_link = InlineKeyboardMarkup(row_width=3).add(InlineKeyboardButton('Перейти к оплате', url=link))
    await message.answer('Для оплаты перейдите по ссылке', reply_markup=button_link)





