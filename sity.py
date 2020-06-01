"""методи міста. Його логіка"""

"""сюди зввертається метод гравця полювання. тут проходить перевірка куди персонаж вже ходив, та створюється 
індивідуальний набір доступних прогулянок. проходить рандомний вибір прогулянки, та вибираються доступні гравцеві 
дії. """
import telegram
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler,
                          ConversationHandler)
import data
import player

import random as roll


class Sity:
    def __init__(self, player, context):
        self.player = player
        self.context = context
        self.can_walk_to = []
        self.walk_to = {}
        self.open_scene= ""
        self.dis_for_case = []
        self.check_cases()
        self.get_one_case()
        self.form_var()
        self.make_message()


    def check_cases(self):
        for key in data.data.keys():
            if key in self.player.now_walk:
                continue
            else:
                self.can_walk_to.append(key)

    def get_one_case(self):
        go_to = ""
        try:
            go_to=roll.choice(self.can_walk_to)
        except IndexError:
            print("no more variants to go")
        self.walk_to= go_to

    def form_var (self):
        dis = self.player.disciplines
        walk = data.data[self.walk_to]
        self.open_scene = self.walk_to
        """"for key in walk:
            if key in dis:
                self.dis_for_case.append(key)"""


    def make_message(self):
        def make_board():
            keyb=[]
            for dis in self.player.disciplines:
                butt_text = dis + " need blood " + str(data.data[self.walk_to][dis][0])
                butt = InlineKeyboardButton(text=butt_text, callback_data=dis)
                row=[butt]
                keyb.append(row)
            reply_markup=InlineKeyboardMarkup(keyb)
            return reply_markup
        self.context.bot.send_message(chat_id=self.player.chat_id, text=self.open_scene, reply_markup=make_board())
        self.context.dispatcher.add_handler(CallbackQueryHandler(self.listen_answer))

    def listen_answer(self, upd, con):
        cq = upd.callback_query.data
        con.dispatcher.remove_handler(con.dispatcher.handlers[0][-1])
        rr = roll.randint(1, 6)
        if rr>=4:
            text = data.data[self.walk_to][cq][1][0]
        else:
            text = data.data[self.walk_to][cq][2][0]

        self.context.bot.send_message(chat_id=self.player.chat_id, text=text)

