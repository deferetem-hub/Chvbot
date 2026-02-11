import os
import telebot

TOKEN = os.getenv("BOT_TOKEN")  # безопасный способ хранить токен
bot = telebot.TeleBot(TOKEN)

# ID администратора (твой Telegram ID)
ADMIN_ID = 5497155434  # <-- вставь сюда свой ID

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    # приветственное сообщение для пользователя
    bot.send_message(message.chat.id, "Привет! Добро пожаловать в бот.")

    # уведомление администратору, что кто-то написал
    bot.send_message(ADMIN_ID,
                     f"Пользователь @{message.from_user.username} "
                     f"нажал /start (ID: {message.from_user.id})")

print("Бот запущен...")
bot.infinity_polling()
