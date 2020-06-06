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

"""а вот запускать его из плеера может быть хорошей идеей. тогда мжоно будет по плееру добраться к обработчику"""
class Sity:
    def __init__(self, player, con, cur_game):
        self.context = con
        self.cur_game = cur_game
        self.player = player
        self.can_walk_to = []
        self.walk_to = {}
        self.open_scene= ""
        self.dis_for_case = []
        self.check_cases()
        self.get_one_case()
        self.make_message()
        self.player.flag2=data.pl_flag2_sity


    def check_cases(self):
        """формирует пул доступных случаев"""
        for key in data.data.keys():
            if key in self.player.walking:
                continue
            else:
                self.can_walk_to.append(key)

    def get_one_case(self):
        """выбирает один случай из доступных"""
        try:
            go_to = roll.choice(self.can_walk_to)
        except IndexError:
            go_to = data.pl_sity_no_more_walk
        self.walk_to = go_to


    def make_message(self):
        """созадет сообщение бота в формате: случай: дисциплины игрока и требуемая на их пременение кровь.
        пока не проверяет предварительно сколько крови у игрока. А надо бы. """

        def make_board():
            keyb=[]
            for dis in self.player.disciplines:
                if self.player.blood >= int(data.data[self.walk_to][dis][0]):
                    butt_text = dis + data.pl_sity_butt_need_blood + str(data.data[self.walk_to][dis][0])
                    butt = InlineKeyboardButton(text=butt_text, callback_data=dis)
                    row=[butt]
                    keyb.append(row)
            reply_markup=InlineKeyboardMarkup(keyb)
            return reply_markup

        self.context.bot.send_message(chat_id=self.player.chat_id, text=self.walk_to, reply_markup=make_board())


    def listen_answer(self, upd, con):
        """слушает ответ игрока, получив - уберает слушатель, псоле чего делает проверку на удачность случая.
        проводит изменения параметров игрока. мне не нравится привязка по индексу.
        надо как-то реализовать увеличение маскарада"""
        dis = upd.callback_query.data
        self.player.blood -= data.data[self.walk_to][dis][0]

        rr = roll.randint(1, 6)
        if rr >= data.rand_dis_fail:
            resualt = data.data[self.walk_to][dis][1]
        else:
            resualt = data.data[self.walk_to][dis][2]

        self.player.blood += resualt[-1]
        self.cur_game.mascarade += resualt[-2]
        con.bot.send_message(chat_id=self.player.chat_id, text=resualt[0])
        self.player.walking.append(self.walk_to)
        self.player.flag2 = data.pl_flag2_ready

        if resualt[-1] > 0:
            """если игроку удалось поккушать, идет проверка на заражен или нет. """
            rr = roll.randint(1, 10)
            if rr >= data.rand_ill_chanse:
                self.player.is_ill=True

