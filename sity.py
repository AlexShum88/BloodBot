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
        if self.player.clan == "Nosferatu":
            self.for_nos()
        else: self.make_message()
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


    def for_nos (self):
        keyb=[]
        butt = InlineKeyboardButton(text="to sity", callback_data="to sity")
        butt2 = InlineKeyboardButton(text="to canalization", callback_data="to canalization")
        row = [butt, butt2]
        keyb.append(row)
        reply_markup = InlineKeyboardMarkup(keyb)
        self.context.bot.send_message(chat_id=self.player.chat_id, text="where you want to go?",
                              reply_markup=reply_markup)

    def make_message(self):
        """созадет сообщение бота в формате: случай: дисциплины игрока и требуемая на их пременение кровь.
        пока не проверяет предварительно сколько крови у игрока. А надо бы. """

        def make_board():
            keyb=[]
            for dis in self.player.disciplines:
                if self.player.blood >= data.data[self.walk_to]["disciplines"][dis]["blood"]:
                    butt_text = dis + data.pl_sity_butt_need_blood + str(data.data[self.walk_to]["disciplines"][dis]["blood"])
                    butt = InlineKeyboardButton(text=butt_text, callback_data=dis)
                    row=[butt]
                    keyb.append(row)
            reply_markup=InlineKeyboardMarkup(keyb)
            return reply_markup

        self.context.bot.send_message(chat_id=self.player.chat_id, text=data.data[self.walk_to]["open"], reply_markup=make_board())


    def listen_answer(self, upd, con):
        """слушает ответ игрока, получив - уберает слушатель, псоле чего делает проверку на удачность случая.
        проводит изменения параметров игрока. мне не нравится привязка по индексу.
        надо как-то реализовать увеличение маскарада"""

        dis = upd.callback_query.data

        def __sity_do(good=1, bad=2):
            self.player.blood -= data.data[self.walk_to]["disciplines"][dis]["blood"]
            rr = roll.randint(1, 6)
            if rr >= data.rand_dis_fail:
                resualt = data.data[self.walk_to]["disciplines"][dis]["variants"][good]

            else:
                resualt = data.data[self.walk_to]["disciplines"][dis]["variants"][bad]

            self.player.blood += resualt['blood']
            self.cur_game.mascarade += resualt['msq']
            con.bot.send_message(chat_id=self.player.chat_id, text=resualt['text'])
            self.player.walking.append(self.walk_to)
            self.player.flag2 = data.pl_flag2_ready

            if resualt['blood'] > 0:
                """если игроку удалось поккушать, идет проверка на заражен или нет. """
                rr = roll.randint(1, 10)
                if rr >= data.rand_ill_chanse:
                    self.player.is_ill = True

        if upd.callback_query.data == "to sity":
            self.make_message()
            return
        elif upd.callback_query.data == "to canalization":
            pass

        if upd.callback_query.data in self.player.disciplines:
            if upd.callback_query.data == data.no_dis_txt:
                msq = self.cur_game.mascarade
                __sity_do(good=(msq*2-1), bad=(msq*2))
                print("msq = {m} good= {g}, bad ={b}".format(m=msq, g=(msq*2-1), b=(msq*2)))
            else:
                __sity_do()
        else:
            upd.callback_query.message.reply_text("please, answer sity question")