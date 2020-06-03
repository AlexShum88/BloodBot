from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler,
                          ConversationHandler)
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


import data
import player


class Regist_pl:
    def __init__(self, game, upd, con):
        self.cur_game = game
        self.dp = con.dispatcher
        self.handl_remover()




    def start_reg(self, upd, cont):
        self.cur_game.regist_pl(upd.effective_chat.id, player.Player(upd.effective_chat.id))
        ms_handler=MessageHandler(Filters.text, self.messs_handl)
        self.dp.add_handler(ms_handler)
        self.reg(upd, cont)
        return

    def messs_handl(self, upd, con):
        print("listen mess")
        comm = self.cur_game.players[upd.effective_chat.id].curr_handl
        print(comm)
        if comm == "name":
            self.reg_name(upd, con)
        elif comm == "blood":
            self.reg_blood_clan(upd, con)
        elif comm == "ready":
            return
        else:
            self.reg(upd, con)
        return

    def change_player_handl(self, upd, new_handl):
        self.cur_game.players[upd.effective_chat.id].curr_handl = new_handl


    def reg(self, upd, cont):
        cont.bot.send_message(chat_id=upd.effective_chat.id, text="Im listen for your name")
        self.change_player_handl(upd, "name")
        return


    def reg_name(self, upd, cont):
        self.cur_game.players[upd.effective_chat.id].name = upd.message.text
        cont.bot.send_message(chat_id=upd.effective_chat.id, text="Im listen for your blood")
        self.change_player_handl(upd, "blood")
        return

    def reg_blood_clan(self, upd, cont):
        if str(upd.message.text).isnumeric():
            bl = int(upd.message.text)
            if bl<10 and bl>0:
                self.cur_game.players[upd.effective_chat.id].blood = upd.message.text
            else:
                cont.bot.send_message(chat_id=upd.effective_chat.id, text="blood must be >0 and <10")
                return
        else:
            cont.bot.send_message(chat_id=upd.effective_chat.id, text="enter num")
            return
        cont.bot.send_message(chat_id=upd.effective_chat.id, text="Im listen for your clan")
        self.reg_clan(upd, cont)
        #change_player_handl(cur_game.players[upd.effective_chat.id], "clan")
        return

    def reg_clan(self, upd, cont):
        keyb = []
        for clan in data.clanes: #переделать клан на словарь с дисциплинами
            bt = InlineKeyboardButton(text=clan, callback_data=clan)
            row = [bt]
            keyb.append(row)
        reply_markup = InlineKeyboardMarkup(keyb)
        upd.message.reply_text('Please, choose one:', reply_markup=reply_markup)
        cont.dispatcher.add_handler(CallbackQueryHandler(self.reg_disciplines))
        #print(cont.dispatcher.handlers[0])
        return

    def reg_disciplines(self, upd, cont):
        cq = upd.callback_query.data
        player = self.cur_game.players[upd.effective_chat.id]
        self.cur_game.players[upd.effective_chat.id].clan = cq
        print(player.name, player.blood, player.clan)
        cont.bot.send_message(chat_id=upd.effective_chat.id, text="you registration complete \n"
                               "sent me sign, if you need something")
        player.curr_handl = "ready"
        cont.dispatcher.remove_handler(cont.dispatcher.handlers[0][-1])
        if player.clan == "Malcovian":
            player.disciplines=['Стремительность', 'Затемнение', 'Могущество']
        self.handl_remover()
        #print(cont.dispatcher.handlers[0])
        return

    def handl_remover(self):
        for handl in self.dp.handlers[0]:
            self.dp.remove_handler(handl)
    #registration players metod end