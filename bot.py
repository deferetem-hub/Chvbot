import os
import telebot
from telebot import types  # <-- добавили

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

ADMIN_ID = 123456789  # вставь свой ID


@bot.message_handler(commands=['start'])
def start(message):
    # создаём клавиатуру
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton("Начать"))

    # приветствие + кнопка
    bot.send_message(
        message.chat.id,
        "Привет! Добро пожаловать в бот.\nНажми «Начать» 👇",
        reply_markup=keyboard
    )

    # уведомление админу
    bot.send_message(
        ADMIN_ID,
        f"Пользователь @{message.from_user.username} "
        f"нажал /start (ID: {message.from_user.id})"
    )


print("Бот запущен...")
bot.infinity_polling()
