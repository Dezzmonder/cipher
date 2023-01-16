import telebot
from telebot import types
import random

letters = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"


def vigenere(msg, key, mul):
    new_str = ''
    c = 0
    key = key.replace(' ', '')
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
key = ''
msg = ''
mul = -1
crypt = 'расшифровка'


@bot.message_handler(commands=['start', 'help', 'restart'])
def send_welcome(message):
    bot.reply_to(message, 'привет! Я умею шифровать и расшифровывать сообщение в трех шифрах: шифре Виженера, шифре Цезаря и шифре атбаш. \n'
                          'Для начала работы введи текст командой /set_text "текст" и ключ, командой /set_key "ключ". \n Выбери режим, командами /decrypt или /encrypt\n'
                          'Если оставить ключ пустым, будет выбран случайный.\nДля ширфа атбаш ключ и режим НЕ требуются\n'
                          'Когда текст введен, введи команду \n/atbash, /caesar или /vigenere \nдля шифровки или расшифровки.\n'
                          'проверить введенный текст и ключ можно командой /params, отчистить командой /clear. Вызвать этот текст /help\n'
                          'P.S. с телефона можно зажать команду и это будет удобнее, чем писать её самостоятельно.')


@bot.message_handler(commands=['encrypt', 'decrypt'])
def set_mul(message):
    global mul, crypt
    if message.text == '/encrypt':
        mul = -1
        crypt = 'расшифровка'
    else:
        mul = 1
        crypt = 'шифровка'
    bot.reply_to(message, f'выбран режим: {crypt}')


@bot.message_handler(commands=['set_text', 'set_key', 'clear'])
def seting(message):
    global msg, key
    if message.text[:8] == '/set_key':
        key = message.text[9:]
        bot.reply_to(message, f'Ключ установлен: \n {key}')
    elif message.text[:9] == '/set_text':
        msg = message.text[10:]
        bot.reply_to(message, f'Текст установлен: \n {msg}')
    else:
        bot.reply_to(message, 'Ключ и текст очищены')
        msg = ''
        key = ''


@bot.message_handler(commands=['params'])
def params(message):
    bot.reply_to(message, f'текущие параметры: \nТекст: {msg}\nКлюч: {key}\nРежим: {crypt}')


@bot.message_handler(commands=['atbash', 'caesar', 'vigenere'])
def encrypt(message):
    global key
    if not msg:
        bot.reply_to(message, 'Нет, так нельзя, нужно ввести собщение с помощью команды /set_text "сообщение"')
    elif message.text == '/atbash':
        bot.reply_to(message, f'Изначльное сообщение: {msg}, расшифровка:')
        bot.reply_to(message, f'{atbash(msg.upper())}')
    elif message.text == '/caesar':
        if key and not key.isdigit():
            bot.reply_to(message, 'Ключ для шифра Цезаря должен быть числом, будет установлен случайный ключ')
            key = random.randint(1, 32)
        else:
            key = random.randint(1, 32)
        bot.reply_to(message, f'Изначальное сообщение: {msg}\nКлюч: {key}\n{crypt}:')
        bot.reply_to(message, caesar(msg.upper(), int(key), mul))
    else:
        if not str(key).isalpha():
            bot.reply_to(message, f'Ключ для шифра Виженера должен быть словом(буквами), будет установлен случайный ключ')
            key = ''
        if not key:
            for i in range(5):
                key += letters[random.randint(0, 32)]
        bot.reply_to(message, f'Изначальное сообщение: {msg}\nКлюч: {key}\n{crypt}:')
        bot.reply_to(message, vigenere(msg.upper(), key.upper(), mul))


@bot.message_handler(content_types=['text'])
def error(message):
    bot.reply_to(message, 'Я не понимаю, пожалуйста, введи\n/help')


bot.infinity_polling()
