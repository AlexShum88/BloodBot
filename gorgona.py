"""горгулья.
это вход в лабу, письма, панель отключения капеллы, возможно и сама лаба тут тоже"""


"""нужна конопка на панели действий игрока горгулья или лаба?  сама горгулья это отдельный юзер 
(чат, что стартует с отдельной команды), в нем 5  кнопок с именами пользователей + одна не кнопка, но суперюзер
еужноуюру нуного пароля выдаст код и комментария что надо его внести в ваше усстройство для открытия дверей 
и взаимодействия с лабой"""
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler,
                          ConversationHandler)
import data

class Gorgona:

    current_user = ""

    def form_bord_user(self, upd, con):
        keyb = []
        for user in data.gorguls_user.keys():
            bt = InlineKeyboardButton(text=user, callback_data=user)
            row = [bt]
            keyb.append(row)
        reply_markup = InlineKeyboardMarkup(keyb)
        upd.message.reply_text(data.menu_chouse, reply_markup=reply_markup)
        return

    def listen_password(self, upd, con):
        answer = upd.message.text
        if answer == data.gorguls_user[self.current_user]:
            con.bot.send_message(chat_id=upd.effective_chat.id, text="great. you autorization on lab {n}".format(n=1247))




    def listener(self, upd, con):
        """в дате должен лежать словарь в котором будут ключи - имена сотрудников, а содержимое - их рпароли
        должен быть метод, что формирует кнопки из ключей
        должен быть метод, что после нажатия кнопки слушает что напишет игрок (слушает пароль)"""
        cq = upd.callback_query.data
        con.bot.send_message(chat_id=upd.effective_chat.id, text="hello my lord. its realy you? enter pass please")
        self.current_user = cq
