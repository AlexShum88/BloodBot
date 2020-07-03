import player
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler,
                          ConversationHandler)
import data
import random as roll

class Fight:
    def __init__(self, player):
        self.player = player
        self.dis = ""
        self.bld = ""
        self.colour = ""
        self.player.flag2 = data.pl_flag2_fight

    def listener(self, upd, con):
        cq = upd.callback_query.data
        if cq in self.player.disciplines:
            self.dis = cq
            if self.dis == data.no_dis_txt:
                self.make_colourboard(upd, con)
            else:
                self.make_bloodboard(upd, con)
        elif "*" == cq[0]:
            self.bld = cq[-1]
            self.player.blood -= int(cq[-1])
            self.make_colourboard(upd, con)
        elif cq in data.colour:
            self.colour = cq
            self.resualt(upd, con)
        else:
            self.make_disboard(upd, con)


    def make_disboard(self, upd, con):
        keyb = []
        for dis in self.player.disciplines:
            bt = InlineKeyboardButton(text=dis, callback_data=dis)
            row = [bt]
            keyb.append(row)
        reply_markup = InlineKeyboardMarkup(keyb)
        con.bot.send_message(chat_id=self.player.chat_id, text="please, choose disciplines for fight", reply_markup=reply_markup)
        return


    def make_bloodboard(self, upd, con):
        keyb = []
        for blood in range(1, 4):
            if blood <= self.player.blood:
                bt = InlineKeyboardButton(text=f"blood rate {blood}", callback_data=f"*{blood}")
                row = [bt]
                keyb.append(row)
        reply_markup = InlineKeyboardMarkup(keyb)
        con.bot.send_message(chat_id=self.player.chat_id, text="choose blood for fight", reply_markup=reply_markup)
        return


    def make_colourboard(self, upd, con):
        keyb = []
        for colour in data.colour:
            bt = InlineKeyboardButton(text=f"{colour}", callback_data=colour)
            row = [bt]
            keyb.append(row)
        reply_markup = InlineKeyboardMarkup(keyb)
        con.bot.send_message(chat_id=self.player.chat_id, text="make colour rate", reply_markup=reply_markup)
        return


    def resualt(self, upd, con):
        con.bot.send_message(chat_id=self.player.chat_id, text=f"{self.dis}, of blood {self.bld} \n {self.colour}")
        self.player.flag2 = data.pl_flag2_ready
        self.player.fight = ""
        return



class Fight2 (Fight):
    def __init__(self, player):
        super().__init__(player)

    def listener(self, upd, con):
        cq = upd.callback_query.data
        if cq in self.player.disciplines:
            self.dis = cq
            self.make_bloodboard(upd, con)
        elif "*" == cq[0]:
            self.bld = cq[-1]
            self.player.blood -= int(cq[-1])
            self.ft_roll(upd, con)
        else:
            self.make_disboard(upd, con)

    def ft_roll (self, upd, con):
        rr = roll.randint(1, 10)
        res = rr + int(self.bld)
        con.bot.send_message(chat_id=self.player.chat_id, text=f"{self.dis} \n{self.player.dis_for_fight[self.dis]} \n"
                                                               f"resualt is {res}")
        self.player.flag2 = data.pl_flag2_ready
        self.player.fight = ""
        return