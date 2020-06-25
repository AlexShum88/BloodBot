"""город. и канализация. и голод тоже тут будет"""

import telegram
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler,
                          ConversationHandler)
import data

import random as roll




class Sity:
    def __init__(self, player, con, cur_game):
        self.context = con
        self.cur_game = cur_game
        self.player = player
        self.can_walk_to = []
        self.walk_to = ""
        self.open_scene= ""
        self.dis_for_case = []
        if self.player.clan == "Nosferatu":
            self.for_nos()
        else: self.make_message()
        self.player.flag2=data.pl_flag2_sity


    def check_cases(self, base = data.data):
        """формирует пул доступных случаев. база оприделяет то есть город или подгород"""
        for key in base.keys():
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
        """штука для оссобенных. создает кнопки на выбор в город или в подгород"""
        keyb=[]
        butt = InlineKeyboardButton(text="to sity", callback_data="to sity")
        butt2 = InlineKeyboardButton(text="to canalization", callback_data="to canalization")
        row = [butt, butt2]
        keyb.append(row)
        reply_markup = InlineKeyboardMarkup(keyb)
        self.context.bot.send_message(chat_id=self.player.chat_id, text="where you want to go?",
                              reply_markup=reply_markup)

    def make_message(self, text=data.data):
        """созадет сообщение бота в формате: случай: дисциплины игрока и требуемая на их пременение кровь.
        """
        self.check_cases(base=text)
        self.get_one_case()
        def make_board():
            keyb=[]
            for dis in self.player.disciplines:
                if self.player.blood >= text[self.walk_to]["disciplines"][dis]["blood"]:
                    butt_text = dis + data.pl_sity_butt_need_blood + str(text[self.walk_to]["disciplines"][dis]["blood"])
                    butt = InlineKeyboardButton(text=butt_text, callback_data=dis)
                    row=[butt]
                    keyb.append(row)
            reply_markup=InlineKeyboardMarkup(keyb)
            return reply_markup

        self.context.bot.send_message(chat_id=self.player.chat_id, text=text[self.walk_to]["open"], reply_markup=make_board())


    def listen_answer(self, upd, con):
        """слушает ответ игрока, получив - уберает слушатель, псоле чего делает проверку на удачность случая.
        проводит изменения параметров игрока. """

        dis = upd.callback_query.data

        def __sity_do(good=1, bad=2, base=data.data):
            """процесс определения результата города для игрока"""
            self.player.blood -= base[self.walk_to]["disciplines"][dis]["blood"]
            rr = roll.randint(1, 6)
            if rr >= data.rand_dis_fail:
                resualt = base[self.walk_to]["disciplines"][dis]["variants"][good]

            else:
                resualt = base[self.walk_to]["disciplines"][dis]["variants"][bad]

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
        """ниже реакции на слушатель кнопок для носферату"""
        if upd.callback_query.data == "to sity":
            self.make_message()
            return
        elif upd.callback_query.data == "to canalization":
            self.make_message(text=data.canal_data)
            return

        if upd.callback_query.data in self.player.disciplines:
            """это реакция на нажатие кнопки дисциплины.
            если имя этого случая заканчивается на К - это канализация. соответственно читать надо из канализации"""
            base = data.data
            if str(self.walk_to)[-1] == "k":
                base = data.canal_data
            if upd.callback_query.data == data.no_dis_txt:
                """если выбрана без дисциплины, то надо смотреть на уровень маскарада для определения какую пару брать
                НО если таких пар нет(как бывает в канализации, то просто брать по умолчанию"""
                msq = self.cur_game.mascarade
                try:
                    __sity_do(good=(msq*2-1), bad=(msq*2), base=base)
                except: __sity_do(base=base)

            else:
                __sity_do(base=base)
        else:
            upd.callback_query.message.reply_text("please, answer sity question")