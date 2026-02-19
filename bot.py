import os
import telebot
from telebot import types

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

ADMIN_ID = 5497155434  # <-- твой Telegram ID

# Товары
PRODUCTS = {
    "Встреча с родственником из прошлого": "Описание товара 1",
    "Я с собой в детстве": "Описание товара 2",
    "Встреча с любимым персонажем": "Описание товара 3",
    "Превращение, морфинг": "Описание товара 4",
    "Свой вариант и стиль": "Описание товара 5",
}

# Храним выбранный товар пользователя
user_product = {}


# ---------- /start ----------
@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("Поехали!")

    bot.send_message(
        message.chat.id,
        "Привет! Спасибо, что перешли в наш бот. Готовы начать?",
        reply_markup=keyboard
    )

    bot.send_message(
        ADMIN_ID,
        f"Пользователь @{message.from_user.username} нажал /start"
    )


# ---------- Старт ----------
@bot.message_handler(func=lambda m: m.text == "Поехали!")
def choose_service(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("Выбрать сценарий")

    bot.send_message(
        message.chat.id,
        "Отлично. Сейчас вам нужно выбрать сценарий для вашего видео 👇",
        reply_markup=keyboard
    )

    bot.send_message(
        ADMIN_ID,
        f"Пользователь @{message.from_user.username} нажал кнопку 'Поехали!'"
    )


# ---------- Выбрать услугу ----------
@bot.message_handler(func=lambda m: m.text == "Выбрать сценарий")
def show_products(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for product in PRODUCTS:
        keyboard.add(product)

    bot.send_message(
        message.chat.id,
        "Супер. Не стесняйтесь кликать и читать описания :) Как подберёте - нужно будет нажать Оформить заявку. Вам напишут на ваш аккаунт в телеграм. Не забудьте проверить, чтобы вам могли писать неконтакты! Это можно сделать в настройках конфиденциальности",
        reply_markup=keyboard
    )

    bot.send_message(
        ADMIN_ID,
        f"Пользователь @{message.from_user.username} нажал кнопку 'Выбрать сценарий'"
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
        "Спасибо! ✍️\nМожете написать любой вопрос, который хотите задать.",
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