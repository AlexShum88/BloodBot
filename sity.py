"""методи міста. Його логіка"""

"""сюди зввертається метод гравця полювання. тут проходить перевірка куди персонаж вже ходив, та створюється 
індивідуальний набір доступних прогулянок. проходить рандомний вибір прогулянки, та вибираються доступні гравцеві 
дії. """
import telegram
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler,
                          ConversationHandler)
import data


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
        self.make_message()


    def check_cases(self):
        """формирует пул доступных случаев"""
        for key in data.data.keys():
            if key in self.player.now_walk:
                continue
            else:
                self.can_walk_to.append(key)

    def get_one_case(self):
        """выбирает один случай из доступных"""
        go_to = ""
        try:
            go_to=roll.choice(self.can_walk_to)
        except IndexError:
            print("no more variants to go")
        self.walk_to = go_to


    def make_message(self):
        """созадет сообщение бота в формате: случай: дисциплины игрока и требуемая на их пременение кровь.
        пока не проверяет предварительно сколько крови у игрока. А надо бы. """

        def make_board():
            keyb=[]
            for dis in self.player.disciplines:
                butt_text = dis + " need blood " + str(data.data[self.walk_to][dis][0])
                butt = InlineKeyboardButton(text=butt_text, callback_data=dis)
                row=[butt]
                keyb.append(row)
            reply_markup=InlineKeyboardMarkup(keyb)
            return reply_markup

        self.context.bot.send_message(chat_id=self.player.chat_id, text=self.walk_to, reply_markup=make_board())
        self.context.dispatcher.add_handler(CallbackQueryHandler(self.listen_answer))

    def listen_answer(self, upd, con):
        """слушает ответ игрока, получив - уберает слушатель, псоле чего делает проверку на удачность случая.
        проводит изменения параметров игрока. мне не нравится привязка по индексу.
        надо как-то реализовать увеличение маскарада"""
        dis = upd.callback_query.data
        con.dispatcher.remove_handler(con.dispatcher.handlers[0][-1])
        self.player.blood -= data.data[self.walk_to][dis][0]

        rr = roll.randint(1, 6)
        if rr>=4:
            resualt = data.data[self.walk_to][dis][1]
        else:
            resualt = data.data[self.walk_to][dis][2]

        self.player.blood -= resualt[-1]
        self.context.bot.send_message(chat_id=self.player.chat_id, text=resualt[0])

        if resualt[-1]>0:
            """если игроку удалось поккушать, идет проверка на заражен или нет. при 1 - да. 
            можно выставить один из параметров в рандомизаторе на динамический"""
            rr = roll.randint(1, 10)
            if rr ==1:
                self.player.is_ill=True

