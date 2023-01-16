import random

import telebot
from telebot import types

letters = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"


def vigenere(msg, key, mul):
    new_str = ''
    c = 0
    key = key.replace(' ', '').upper()
    for i in msg.upper():
        if i in letters:
            new_str += (letters[(letters.index(i) + (letters.index(key[c]) * mul)) % 33])
            c += 1
        else:
            new_str += i
            c += 1
        if c == len(key):
            c = 0
    return str(new_str)


def caesar(msg, key, mul):
    new_str = ''
    for i in msg.upper():
        if i in letters:
            new_str += letters[(letters.index(i) + (key * mul)) % 33]
        else:
            new_str += i
    return new_str


def atbash(msg):
    new_str = ''
    for i in msg.upper():
        if i in letters:
            new_str += letters[-letters.index(i)]
        else:
            new_str += i
    return new_str


bot = telebot.TeleBot("token", parse_mode=None)
waiting_key = False
waiting_text = True
err = False
msg = ''
key = ''
chip_met = ''
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	global waiting_text
	bot.reply_to(message, "Введи текст")
	waiting_text = True


@bot.message_handler(content_types=['text'])
def wait_for_msg(message):
	global msg, key, waiting_key, chip_met, err
	if message.text not in ['Атбаш', 'Виженер', 'Цезарь', 'Зашифровать', 'Расшифровать','Помощь','Сброс','Назад']:
		if waiting_key:
			key = message.text
			if chip_met == 'Цезарь':
				if message.text == 'Случайный ключ':
					key = random.randint(1,32)
					print(key)
					waiting_key = False
					err = False
				elif key.isdigit():
					waiting_key = False
					err = False
				else:
					bot.reply_to(message, 'Ошибка, ключ должен быть числом')
					markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
					btnrnd = types.KeyboardButton('Случайный ключ')
					markup.row(btnrnd)
					bot.reply_to(message, 'Введите ключ', reply_markup=markup)
					err = True
			elif chip_met == 'Виженер':
				if message.text == 'Случайный ключ':
					key = ''
					for i in range(5):
						key += letters[random.randint(0,32)]
						print(key)
					waiting_key = False
					err = False
				elif key.isalpha():
					waiting_key = False
					err = False
				else:
					bot.reply_to(message, 'Ошибка, ключ должен быть буквенным')
					markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
					btnrnd = types.KeyboardButton('Случайный ключ')
					markup.row(btnrnd)
					bot.reply_to(message, 'Введите ключ', reply_markup=markup)
					err = True
			if not err:
				markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
				btnen = types.KeyboardButton('Расшифровать')
				btnde = types.KeyboardButton('Зашифровать')
				markup.row(btnen)
				markup.row(btnde)
				bot.reply_to(message, 'Ключ принят', reply_markup=markup)
		else:
			msg = message.text
			markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
			btna = types.KeyboardButton('Атбаш')
			btnv = types.KeyboardButton('Виженер')
			btnc = types.KeyboardButton('Цезарь')
			btnback = types.KeyboardButton('Назад')
			markup.row(btna)
			markup.row(btnv)
			markup.row(btnc)
			markup.row(btnback)
			bot.reply_to(message, "Текст принят, выбери способ шифрования", reply_markup=markup)
	if message.text == 'Атбаш':
		bot.reply_to(message, f'Изначалный текст:\n{msg}\nМетод шифрования атбаш.\nРасшифровка:')
		bot.reply_to(message, atbash(msg))
	elif message.text == 'Виженер':
		waiting_key = True
		chip_met = 'Виженер'
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
		btnrnd = types.KeyboardButton('Случайный ключ')
		markup.row(btnrnd)
		bot.reply_to(message, 'Введите ключ', reply_markup=markup)
	elif message.text == 'Цезарь':
		waiting_key = True
		chip_met = 'Цезарь'
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
		btnrnd = types.KeyboardButton('Случайный ключ')
		markup.row(btnrnd)
		bot.reply_to(message, 'Введите ключ', reply_markup=markup)

	if message.text in ['Расшифровать', 'Зашифровать']:
		if message.text == 'Зашифровать':
			mul = 1
		else:
			mul = -1
		if chip_met == 'Цезарь':
			res = caesar(msg, int(key), mul)
		else:
			res = vigenere(msg, key, mul)
		bot.reply_to(message,f'Изначалный текст:\n{msg}\nМетод шифрования {chip_met}.\nКлюч: {key}\nРезульат:')
		bot.reply_to(message, res)
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
		btna = types.KeyboardButton('Атбаш')
		btnv = types.KeyboardButton('Виженер')
		btnc = types.KeyboardButton('Цезарь')
		btnback = types.KeyboardButton('Назад')
		markup.row(btna)
		markup.row(btnv)
		markup.row(btnc)
		markup.row(btnback)
		bot.reply_to(message, "Выбери способ шифрования", reply_markup=markup)
	if message.text == 'Назад':
		msg = ''
		bot.reply_to(message, 'введи текст')

	if message.text == 'Сброс':
		waiting_key = False
		err = False
		msg = ''
		key = ''
		chip_met = ''
		bot.reply_to(message, 'Все параметры сброшены')





bot.infinity_polling()

