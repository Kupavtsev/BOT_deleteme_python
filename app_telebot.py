# -*- coding: utf-8 -*-
# Telegram
import telebot
from telebot import types
# Mail sending
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# RoboCassa
import hashlib
from urllib.parse import quote

from config import TOKEN, EMAIL_PASSWORD



# API_TOKEN = ('example')
bot = telebot.TeleBot(TOKEN)

user_dict = {}
user_private_dict = {}

class UserPrivate:
    def __init__(self, name):
        self.name = name
        self.job_study = None
        self.nickname = None
        self.social = None
        self.phones = None
        self.email = None
        self.pay_phone = None

class User:
    def __init__(self, name):
        self.name = name
        self.inn = None
        self.address = None
        self.area = None
        self.social = None
        self.phones = None
        self.emails = None
        self.pay_phone = None

# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add('Юр. лицо', 'Физ. лицо')
    msg = bot.reply_to(message, 'Оформление заявки, выберете форму:',  reply_markup=markup)
    bot.register_next_step_handler(msg, process_scenario_step)

def process_scenario_step(message):
    try:
        chat_id = message.chat.id
        form = message.text
        if (form == u'Юр. лицо'):
            msg = bot.send_message(chat_id, 'Введите название организации: ')
            bot.register_next_step_handler(msg, process_company_name_step)
        elif (form == u'Физ. лицо'):
            msg = bot.send_message(chat_id, 'Введите ФИО: ')
            bot.register_next_step_handler(msg, process_private_name_step)
        
    except Exception as e:
        bot.reply_to(message, 'process_scenario_step') 

# ============= Company ================

def process_company_name_step(message):
    try:
        chat_id = message.chat.id
        name = message.text
        user = User(name)
        user_dict[chat_id] = user
        msg = bot.reply_to(message, 'Введите ИНН организации:')
        bot.register_next_step_handler(msg, process_company_inn_step)
    except Exception as e:
        bot.reply_to(message, 'oooops, process_company_name_step')



def process_company_inn_step(message):
    try:
        chat_id = message.chat.id
        inn = message.text
        if not inn.isdigit():
            msg = bot.reply_to(message, 'Должно быть число. Введите ИНН')
            bot.register_next_step_handler(msg, process_company_inn_step)
            return
        user = user_dict[chat_id]
        user.inn = inn
        msg = bot.reply_to(message, 'Адрес организации:')
        bot.register_next_step_handler(msg, process_company_address_step)
    except Exception as e:
        bot.reply_to(message, 'oooops, process_company_inn_step') 


def process_company_address_step(message):
    try:
        chat_id = message.chat.id
        address = message.text
        user = user_dict[chat_id]
        user.address = address
        msg = bot.reply_to(message, 'Сфера деятельности (общими словами):')
        bot.register_next_step_handler(msg, process_company_area_step)
    except Exception as e:
        bot.reply_to(message, 'oooops, process_company_address_step')

def process_company_area_step(message):
    try:
        chat_id = message.chat.id
        area = message.text
        user = user_dict[chat_id]
        user.area = area
        msg = bot.reply_to(message, 'Ссылки на аккаунты в соцсетях, если есть (instagram, vk, facebook):')
        bot.register_next_step_handler(msg, process_company_social_step)
    except Exception as e:
        bot.reply_to(message, 'oooops, process_company_area_step')


def process_company_social_step(message)        :
    try:
        chat_id = message.chat.id
        social = message.text
        user = user_dict[chat_id]
        user.social = social
        msg = bot.reply_to(message, 'Телефоны организации:')
        bot.register_next_step_handler(msg, process_company_phones_step)
    except Exception as e:
        bot.reply_to(message, 'oooops, process_company_social_step')

def process_company_phones_step(message):
    try:
        chat_id = message.chat.id
        phones = message.text
        user = user_dict[chat_id]
        user.phones = phones
        msg = bot.reply_to(message, 'Email-адреса организации:')
        bot.register_next_step_handler(msg, process_company_emails_step)
    except Exception as e:
        bot.reply_to(message, 'oooops, process_company_phones_step')


def process_company_emails_step(message):
    try:
        chat_id = message.chat.id
        emails = message.text
        user = user_dict[chat_id]
        user.emails = emails
        bot.send_message(chat_id,
         'Организация:  ' + user.name
          + '\n ИНН: ' + str(user.inn)
           + '\n Адрес: ' + user.address
            + '\n Сфера деятельности: ' + user.area
             + '\n Ссылки на социальные сети: ' + user.social
              + '\n Телефоны организации: ' + user.phones
               + '\n E-mails организации: ' + user.emails )
        msg = bot.reply_to(message, 'Оплата за первичный анализ 199 руб. Введите номер телефона в формате 123XXXX, без пробелов и тире: ')
        post_data_to_email_company(user.name, user.inn, user.address, user.area, user.social, user.phones, user.emails)
        bot.register_next_step_handler(msg, process_company_payment_step)
    except Exception as e:
        bot.reply_to(message, 'oooops, process_company_emails_step')

def process_company_payment_step(message):
    try:
        telegram_id = int(message.from_user.id)
        chat_id = message.chat.id
        pay_phone = message.text
        if not pay_phone.isdigit():
            msg = bot.reply_to(message, 'Не верный формат телефона, укажите числом без пробелов, скобок и тире. Введите номер телефона')
            bot.register_next_step_handler(msg, process_company_payment_step)
            return
        user = user_private_dict[chat_id]
        user.pay_phone = pay_phone
        phone = user.pay_phone
        link = make_link(phone, telegram_id)
        msg = bot.reply_to(message, 'Проверка оплаты и подготовка предварительного отчета займут 30 минут, итоговый отчет придет Вам в течение суток с момента заказа. Просим ожидать. Ссылка для оплаты: ' + link)
        # bot.register_next_step_handler(msg, process_private_email_step)
    except Exception as e:
        bot.reply_to(message, 'oooops, process_company_payment_step')



# ============= Private Person ================

def process_private_name_step(message):
    try:
        chat_id = message.chat.id
        name = message.text
        user = UserPrivate(name)
        user_private_dict[chat_id] = user
        msg = bot.reply_to(message, 'Организации, в которых Вы работали/учились (вводить просто названия в любом порядке). Чем больше введете - тем лучше будет проведен анализ.')
        bot.register_next_step_handler(msg, process_private_job_study_step)
    except Exception as e:
        bot.reply_to(message, 'oooops, process_private_name_step')

def process_private_job_study_step(message):
    try:
        chat_id = message.chat.id
        job_study = message.text
        user = user_private_dict[chat_id]
        user.job_study = job_study
        msg = bot.reply_to(message, 'Используемые Вами Nickname в сети. Чем больше введете - тем лучше будет проведен анализ.')
        bot.register_next_step_handler(msg, process_private_nickname_step)
    except Exception as e:
        bot.reply_to(message, 'oooops, process_private_job_study_step')

def process_private_nickname_step(message):
    try:
        chat_id = message.chat.id
        nickname = message.text
        user = user_private_dict[chat_id]
        user.nickname = nickname
        msg = bot.reply_to(message, 'Ссылки на аккаунты в соцсетях, если есть (instagram, vk, facebook).')
        bot.register_next_step_handler(msg, process_private_social_step)
    except Exception as e:
        bot.reply_to(message, 'oooops, process_private_nickname_step')

def process_private_social_step(message):
    try:
        chat_id = message.chat.id
        social = message.text
        user = user_private_dict[chat_id]
        user.social = social
        msg = bot.reply_to(message, 'Ваши телефоны (в любом формате):')
        bot.register_next_step_handler(msg, process_private_phones_step)
    except Exception as e:
        bot.reply_to(message, 'oooops, process_private_social_step')

def process_private_phones_step(message):
    try:
        chat_id = message.chat.id
        phones = message.text
        user = user_private_dict[chat_id]
        user.phones = phones
        msg = bot.reply_to(message, 'Ваши email:')
        bot.register_next_step_handler(msg, process_private_email_step)
    except Exception as e:
        bot.reply_to(message, 'oooops, process_private_phones_step')

def process_private_email_step(message):
    try:
        
        chat_id = message.chat.id
        email = message.text
        user = user_private_dict[chat_id]
        user.email = email
        bot.send_message(chat_id,
         'ФИО:  ' + user.name
          + '\n Организации, в которых Вы работали/учились:   ' + user.job_study
           + '\n Используемые Вами Nickname в сети:   ' + user.nickname
            + '\n Ссылки на аккаунты в соцсетях:   ' + user.social
             + '\n Ваши телефоны:   ' + user.phones
              + '\n Ваши email:   ' + user.email)
        msg = bot.reply_to(message, 'Оплата за первичный анализ 199 руб. Введите номер телефона в формате 123XXXX, без пробелов и тире: ')
        # print('Start Sending')
        post_data_to_email(user.name, user.job_study, user.nickname, user.social, user.phones, user.email)
        # print('Sent an email')
        bot.register_next_step_handler(msg, process_private_payment_step)
    except Exception as e:
        bot.reply_to(message, 'oooops, process_private_email_step')


def process_private_payment_step(message):
    try:
        telegram_id = int(message.from_user.id)
        chat_id = message.chat.id
        pay_phone = message.text
        if not pay_phone.isdigit():
            msg = bot.reply_to(message, 'Не верный формат телефона, укажите числом без пробелов, скобок и тире. Введите номер телефона')
            bot.register_next_step_handler(msg, process_private_payment_step)
            return
        user = user_private_dict[chat_id]
        user.pay_phone = pay_phone
        phone = user.pay_phone
        link = make_link(phone, telegram_id)
        msg = bot.reply_to(message, 'Проверка оплаты и подготовка предварительного отчета займут 30 минут, итоговый отчет придет Вам в течение суток с момента заказа. Просим ожидать. Ссылка для оплаты: ' + link)
        # bot.register_next_step_handler(msg, process_private_email_step)
    except Exception as e:
        bot.reply_to(message, 'oooops, process_private_payment_step')


# ======= Mail Sending ========================
def post_data_to_email_company(name, inn, address, area, social, phones, emails):
    me = "support@deleteme.ru"
    # my_password = r"uxsbldbcbhtpkjpf"
    my_password = EMAIL_PASSWORD
    you = "oleg.k@dot-tech.ru"

    # name = user_private_dict['name']

    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Заказ №"
    msg['From'] = me
    msg['To'] = you


    # Plain text
    # body = "Оповещение из системы заказов для " + name
    # msg.attach(MIMEText(body, 'plain'))

    # HTML
    html = f'<html><body><h1>Оповещение из системы заказов</h1>\
        <h2>Организация: {name}</h2>\
            <p>ИНН Организации: {inn}</p>\
                <p>Адрес: {address}</p>\
                    <p>Сфера деятельности: {area}</p>\
                        <p>Ссылки на социальные сети: {social}</p>\
                            <p>Телефоны организации: {phones}</p>\
                                <p>E-mails организации: {emails}</p></body></html>'
    part2 = MIMEText(html, 'html')
    msg.attach(part2)


    # Send the message via gmail's regular server, over SSL - passwords are being sent, afterall
    # s = smtplib.SMTP_SSL('smtp.gmail.com')
    s = smtplib.SMTP_SSL('smtp.yandex.ru:465')
    # uncomment if interested in the actual smtp conversation
    # s.set_debuglevel(1)
    # do the smtp auth; sends ehlo if it hasn't been sent already
    s.login(me, my_password)

    s.sendmail(me, you, msg.as_string())
    s.quit()



def post_data_to_email(name, job_study, nickname, social, phones, email):
    me = "support@deleteme.ru"
    my_password = EMAIL_PASSWORD
    you = "oleg.k@dot-tech.ru"

    # name = user_private_dict['name']

    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Заказ №"
    msg['From'] = me
    msg['To'] = you


    # Plain text
    # body = "Оповещение из системы заказов для " + name
    # msg.attach(MIMEText(body, 'plain'))

    # HTML
    html = f'<html><body><h1>Оповещение из системы заказов</h1>\
        <h2>ФИО: {name}</h2>\
            <p>Организации, в которых Вы работали/учились: {job_study}</p>\
                <p>Используемые Вами Nickname в сети: {nickname}</p>\
                    <p>Ссылки на аккаунты в соцсетях: {social}</p>\
                        <p>Ваши телефоны: {phones}</p>\
                            <p>Ваши email: {email}</p></body></html>'
    part2 = MIMEText(html, 'html')
    msg.attach(part2)


    # Send the message via gmail's regular server, over SSL - passwords are being sent, afterall
    # s = smtplib.SMTP_SSL('smtp.gmail.com')
    s = smtplib.SMTP_SSL('smtp.yandex.ru:465')
    # uncomment if interested in the actual smtp conversation
    # s.set_debuglevel(1)
    # do the smtp auth; sends ehlo if it hasn't been sent already
    s.login(me, my_password)

    s.sendmail(me, you, msg.as_string())
    s.quit()
# ======== End of Mail Sending ========================


# =================== Make payment Link =============== 
def make_hash(price, phone, telegram_id):

    # hash_obj = hashlib.pbkdf2_hmac('sha1', f"deleteme_ru_:{price}:0:dkX749p3enERQuY7cVpd:Shp_phone={phone}:Shp_telegram={telegram_id}".encode(), salt=b'')
    hash_obj = hashlib.sha1(f"deleteme_ru_:{price}:0:dkX749p3enERQuY7cVpd:Shp_phone={phone}:Shp_telegram={telegram_id}".encode()).hexdigest()
    return hash_obj

def get_description(service, price):
    description = f'Оплата за оказание услуги "{service}". Сумма на оплату: {price} рублей'
    result = quote(description, safe='/')
    return result

def make_link(phone, telegram_id):
    price = 199
    service = 'Название услуги'
    # print('sha1 start')
    sha1 = make_hash(price, phone, telegram_id)
    description = get_description(service, price)
    # print('sha1 end')

    # post_data_to_email()
    link_to_pay = f"https://auth.robokassa.ru/Merchant/Index.aspx?MerchantLogin=deleteme_ru_&InvId=0&Culture=ru&Encoding=utf-8&Shp_phone={phone}&Shp_telegram={telegram_id}&OutSum={price}&Description={description}&SignatureValue={sha1}"
    return link_to_pay
# =================== Make payment Link End ===========







bot.enable_save_next_step_handlers(delay=2)

# Load next_step_handlers from save file (default "./.handlers-saves/step.save")
# WARNING It will work only if enable_save_next_step_handlers was called!
bot.load_next_step_handlers()

bot.polling()