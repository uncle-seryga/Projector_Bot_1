import telebot
from telebot import types

import db_controller
import payments
from localization import Lang

# @prjctr_demo_bot
bot = telebot.TeleBot('5971276481:AAFEI89d5Cr9bPzsPJOkc08Gy0FLo09K2CU')
keyboard_transport_types = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
keyboard_transport_lp = types.ReplyKeyboardMarkup(resize_keyboard=True)


@bot.message_handler(commands=['start'])
def handle_start(message: types.Message):
    print(get_tel_id(message))
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button = types.KeyboardButton(str(Lang(message.from_user.language_code, 1)))
    keyboard.add(button)
    bot.send_message(message.chat.id, str(Lang(message.from_user.language_code, 0)),  # e.g how to use localization
                     reply_markup=keyboard)


@bot.message_handler(func=lambda message: True)
def handle_application(message: types.Message):
    if message.text == str(Lang(message.from_user.language_code, 1)):
        request_access = payments.Payments().get_if_debt(tel_id=message.chat.id)
        if request_access:
            for x in [str(Lang(message.from_user.language_code, 5)),
                      str(Lang(message.from_user.language_code, 6)),
                      str(Lang(message.from_user.language_code, 7))]:
                keyboard_transport_types.add(x)
            bot.send_message(message.chat.id, str(Lang(message.from_user.language_code, 9)),
                             reply_markup=keyboard_transport_types)
            bot.register_next_step_handler(message, process_transport_type)
        elif request_access == 3:
            bot.send_message(message.chat.id, str(Lang(message.from_user.language_code, 8)))
        else:
            bot.send_message(message.chat.id, str(Lang(message.from_user.language_code, 8)))


@bot.message_handler(content_types=['contact'])
def action(message: telebot.types.Message):
    get_phone_number(message)


query = []


def process_transport_type(message: telebot.types.Message):
    vehicle_type = message.text
    keyboard_transport_lp.add(str(Lang(message.from_user.language_code, 10)))
    bot.send_message(message.chat.id, str(Lang(message.from_user.language_code, 11)),
                     reply_markup=keyboard_transport_lp)
    query.append(vehicle_type)
    bot.register_next_step_handler(message, process_license_plate)


def process_license_plate(message: telebot.types.Message):
    send_request(message)


def send_request(message: telebot.types.Message):
    lp = message.text
    apt_id = db_controller.Residents().select(columns=["apartment_id"], key_word="tel_id", value=message.chat.id)[0][0]
    apt_code = db_controller.Apartments().select_apt_code(apt_id)
    for x in db_controller.Residents().select(columns=['tel_id'], key_word='user_type', value=3):
        bot.send_message(x[0],
                         f'{str(Lang(message.from_user.language_code, 13))}\n'
                         f'<b>{apt_code}</b>\n'
                         f'..........\n'
                         f'{str(Lang(message.from_user.language_code, 14))}'
                         f' <u>{query[0]}</u>\n'
                         f'{str(Lang(message.from_user.language_code, 15))}'
                         f' <b>{lp.upper()}</b>',parse_mode="html")


def get_tel_id(message: telebot.types.Message):
    return message.chat.id


def get_phone_number(message: telebot.types.Message):
    return message.contact.phone_number


bot.polling()
