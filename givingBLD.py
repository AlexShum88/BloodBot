from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler,
                          ConversationHandler)
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


import data
import player
from blood import Blood

class Give:
    def __init__(self, pl:player, base, con):
        self.plr = pl
        self.dp = con.dispatcher
        self.base = base


    def handl_remover(self):
        for handl in self.dp.handlers[0]:
            self.dp.remove_handler(handl)


    def bld_var(self):
        keyb=[]
        for bld in range(self.plr.blood):
            bt=InlineKeyboardButton(text=bld, callback_data=bld)
            row=[bt]
            keyb.append(row)
        bt=InlineKeyboardButton(text="drop of blood", callback_data=0)
        row=[bt]
        keyb.append(row)
        reply_markup=InlineKeyboardMarkup(keyb)
        return reply_markup

    def mess(self, upd, con):
        self.handl_remover()
        self.dp.add_handler(CallbackQueryHandler(self.resualt))
        upd.callback_query.message.reply_text("how many blood you want to give?", reply_markup=self.bld_var())

    def resualt(self,upd, con):
        cq = upd.callback_query.data
        bld =Blood(self.base, cq, self.plr.is_ill, self.plr)
        upd.callback_query.message.reply_text(text="you give {n} blood point. \n"
                                    "its code {c}".format(n=cq, c=bld.name))
        self.handl_remover()