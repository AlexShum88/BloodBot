"""это мастер. мастер это прдвнуый игрок, ибо мне в лом было выделять отдельно пользователя
 и от него наследовать и мастера и игрока. игрок просто уже был"""
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler,
                          ConversationHandler)
import player
import data
import random as roll

class Masta (player.Player):

    def __init__(self, chatid, cur_game):
        super().__init__(chatid)
        self.chat_id = chatid
        self.__name: str = "master"
        self.clan = "master"
        self.flag1 = "ready"  # its pl status: ono registration, on game, on torpor, dead?....
        self.flag2 = "master_start"  # its for change callback listener
        self.role = ""
        self.cando = ["monitor"]
        self.cur_game = cur_game


    def reg_role(self, upd, cont):
        """это для определения роли мастера, скорее всего не нужная хрень"""
        keyb = []
        for role in data.master_roles:
            bt = InlineKeyboardButton(text=role, callback_data=role)
            row = [bt]
            keyb.append(row)
        reply_markup = InlineKeyboardMarkup(keyb)
        self.flag2 = "master_role"
        upd.message.reply_text("select role:", reply_markup=reply_markup)
        return

    def master_callback_listener (self, upd, con):
        """слушатель для кнопок, что прилетают от мастеров ДЛЯ ВЫБОРА РОЛИ"""
        callback = upd.callback_query.data
        if callback == "dispatcher":
            self.cando.append("sity")
            self.cando.append("masq")
        self.cando_board(upd, con)

    def cando_board (self, upd, con):
        """создает кнопки в зависимости от доступных мастеру функций"""
        keyb = []
        for do in self.cando:
            bt = InlineKeyboardButton(text=do, callback_data=do)
            row = [bt]
            keyb.append(row)
        reply_markup = InlineKeyboardMarkup(keyb)
        self.flag2 = "master_todo"
        con.bot.send_message(chat_id=self.chat_id, text="what you want ", reply_markup=reply_markup)
        return

    def cando_listner (self, upd, con):
        """слуашет, что мостер хочет сделать"""
        def num_gen():
            """генератор случайных чисел. нужен для ключей города"""
            rr = roll.randint(1000, 8999)
            return rr

        callback = upd.callback_query.data

        if callback == "sity":
            self.cur_game.sity_key = num_gen()
            upd.callback_query.message.reply_text("access to sity on {n}".format(n=self.cur_game.sity_key))
        elif callback == "masq":
            """дает инфу о текущем положении маскарада, и дает кнопки для регулировки"""
            upd.callback_query.message.reply_text("mascarade = {n}".format(n=self.cur_game.mascarade))
            keyb=[]
            bt1 = InlineKeyboardButton(text="+", callback_data="+")
            bt2 = InlineKeyboardButton(text="-", callback_data="-")
            row = [bt1, bt2]
            keyb.append(row)
            reply_markup = InlineKeyboardMarkup(keyb)
            self.flag2 = "master_todo"
            con.bot.send_message(chat_id=self.chat_id, text="what you want ", reply_markup=reply_markup)
            return
        elif callback == "+":
            self.cur_game.mascarade += 1
            upd.callback_query.message.reply_text("mascarade = {n}".format(n=self.cur_game.mascarade))
        elif callback == "-":
            self.cur_game.mascarade -= 1
            upd.callback_query.message.reply_text("mascarade = {n}".format(n=self.cur_game.mascarade))

        self.cando_board(upd, con)