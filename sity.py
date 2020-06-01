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
    def __init__(self, player, bot):
        self.player = player
        self.bot = bot
        self.can_walk_to = []
        self.open_scene= ""
        self.dis_for_case = []
        self.check_cases()
        self.form_var(case=self.get_one_case())
        self.make_message()


    def check_cases(self):
        for key in data.data.keys():
            if key in self.player.now_walk:
                continue
            else:
                self.can_walk_to.append(key)

    def get_one_case(self):
        go_to = 0
        try:
            go_to=roll.choice(self.can_walk_to)
        except IndexError:
            print("no more variants to go")
        return go_to

    def form_var (self, case):
        dis = self.player.disciplines
        walk = data.data[case]
        self.open_scene = case
        self.dis_for_case = []
        for key in walk:
            if key in dis:
                self.dis_for_case.append(key)

        self.dis_for_case.append(walk['Без применения дисциплин']) # add no DIS case

    def make_message(self):
        def make_board():
            keyb=[]
            for dis in self.dis_for_case:
                butt_text = dis.key + " need blood " + dis[dis.key][0]
                butt = InlineKeyboardButton(text=butt_text, callback_data=dis.key)
                row=[butt]
                keyb.append(row)
                reply_markup=InlineKeyboardMarkup(keyb)
                return reply_markup
        self.bot.bot.send_message(chat_id=self.player.chat_id, text=self.open_scene, reply_markup=make_board())