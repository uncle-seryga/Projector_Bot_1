import telebot
from telebot import types

import db_controller
from localization import Lang

bot = telebot.TeleBot('5971276481:AAFEI89d5Cr9bPzsPJOkc08Gy0FLo09K2CU')
keyboard_transport_types = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
keyboard_transport_lp = types.ReplyKeyboardMarkup(resize_keyboard=True)


@bot.message_handler(commands=['start'])
def handle_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button = types.KeyboardButton(str(Lang(message.from_user.language_code, 1)))
    keyboard.add(button)
    bot.send_message(message.chat.id, str(Lang(message.from_user.language_code, 0)),  # e.g how to use localization
                     reply_markup=keyboard)


@bot.message_handler(func=lambda message: True)
def handle_application(message: types.Message):
    print(message)
    if message.text == str(Lang(message.from_user.language_code, 1)):
        for x in [str(Lang(message.from_user.language_code, 6)),
                  str(Lang(message.from_user.language_code, 7)),
                  str(Lang(message.from_user.language_code, 8))]:
            keyboard_transport_types.add(x)
        bot.send_message(message.chat.id, "Будь ласка, оберіть тип ТЗ для пропуску:",  # todo add localization
                         reply_markup=keyboard_transport_types)
        bot.register_next_step_handler(message, process_transport_type)


query = []


def process_transport_type(message):
    vehicle_type = message.text
    keyboard_transport_lp.add("Немає номера")
    bot.send_message(message.chat.id, "Будь ласка, додайте номер ТЗ", reply_markup=keyboard_transport_lp)
    query.append(vehicle_type)
    bot.register_next_step_handler(message, process_license_plate)


def process_license_plate(message: telebot.types.Message):
    lp = message.text
    for x in db_controller.Residents().select(columns=['tel_id'], key_word='user_type', value='security'):
        bot.send_message(x,
                         f'Request from APT {db_controller.Residents().select(columns=["apartments_id"], key_word="tel_id", value=message.chat.id)} for {query[0]} with LP {lp}')


bot.polling()
