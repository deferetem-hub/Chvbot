import os
import telebot
from telebot import types

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

ADMIN_ID = 5497155434  # <-- твой Telegram ID

# Товары
PRODUCTS = {
    "Товар 1": "Описание товара 1",
    "Товар 2": "Описание товара 2",
    "Товар 3": "Описание товара 3",
    "Товар 4": "Описание товара 4",
    "Товар 5": "Описание товара 5",
}

# Храним выбранный товар пользователя
user_product = {}


# ---------- /start ----------
@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("Старт")

    bot.send_message(
        message.chat.id,
        "Привет! 👋\nДобро пожаловать в бот.",
        reply_markup=keyboard
    )

    bot.send_message(
        ADMIN_ID,
        f"Пользователь @{message.from_user.username} нажал /start"
    )


# ---------- Старт ----------
@bot.message_handler(func=lambda m: m.text == "Старт")
def choose_service(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("Выбрать услугу")

    bot.send_message(
        message.chat.id,
        "Отлично! Нажми кнопку ниже 👇",
        reply_markup=keyboard
    )

    bot.send_message(
        ADMIN_ID,
        f"Пользователь @{message.from_user.username} нажал кнопку 'Старт'"
    )


# ---------- Выбрать услугу ----------
@bot.message_handler(func=lambda m: m.text == "Выбрать услугу")
def show_products(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for product in PRODUCTS:
        keyboard.add(product)

    bot.send_message(
        message.chat.id,
        "Выберите товар, чтобы узнать подробнее:",
        reply_markup=keyboard
    )

    bot.send_message(
        ADMIN_ID,
        f"Пользователь @{message.from_user.username} нажал кнопку 'Выбрать услугу'"
    )


# ---------- Выбор товара ----------
@bot.message_handler(func=lambda m: m.text in PRODUCTS)
def product_info(message):
    user_product[message.chat.id] = message.text

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("Назад", "Оформить заявку")

    bot.send_message(
        message.chat.id,
        PRODUCTS[message.text],
        reply_markup=keyboard
    )

    bot.send_message(
        ADMIN_ID,
        f"Пользователь @{message.from_user.username} выбрал '{message.text}'"
    )


# ---------- Назад ----------
@bot.message_handler(func=lambda m: m.text == "Назад")
def back_to_products(message):
    show_products(message)

    bot.send_message(
        ADMIN_ID,
        f"Пользователь @{message.from_user.username} нажал 'Назад'"
    )


# ---------- Оформить заявку ----------
@bot.message_handler(func=lambda m: m.text == "Оформить заявку")
def make_request(message):
    product = user_product.get(message.chat.id, "Неизвестно")

    bot.send_message(
        message.chat.id,
        "Спасибо! ✍️\nНапишите ваш вопрос, менеджер скоро ответит.",
        reply_markup=types.ReplyKeyboardRemove()
    )

    bot.send_message(
        ADMIN_ID,
        f"Пользователь @{message.from_user.username} нажал 'Оформить заявку' по товару '{product}'"
    )


# ---------- Любой текст после заявки ----------
@bot.message_handler(func=lambda m: True)
def forward_to_admin(message):
    bot.send_message(
        ADMIN_ID,
        f"💬 Сообщение от клиента\n"
        f"ID: {message.from_user.id}\n"
        f"Текст: {message.text}"
    )


print("Бот запущен...")
bot.infinity_polling()
