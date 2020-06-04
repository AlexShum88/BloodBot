from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler,
                          ConversationHandler)
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


import data
import player
from blood import Blood


def bld_var(upd, cur_game):
    keyb=[]
    for bld in range(cur_game.players[upd.effective_chat.id].blood+1):
        if bld == 0:
            bt=InlineKeyboardButton(text="drop of blood", callback_data=0)
        else:
            bt=InlineKeyboardButton(text=bld, callback_data=bld)
        row=[bt]
        keyb.append(row)
    reply_markup=InlineKeyboardMarkup(keyb)
    return reply_markup

def mess(upd, con, cur_game):
    upd.callback_query.message.reply_text("how many blood you want to give?", reply_markup=bld_var(upd, cur_game))
    cur_game.players[upd.effective_chat.id].flag2="givebld"

def resualt(upd, con, cur_game):
    cq = upd.callback_query.data
    pl = cur_game.players[upd.effective_chat.id]
    if type(cq)==int or cq.isnumeric():
        pl.blood-=int(cq)
    else:
        upd.callback_query.message.reply_text(text="wrong callback")
        return
    bld =Blood(cur_game.blood_base, cq, pl.is_ill, pl)
    upd.callback_query.message.edit_reply_markup(reply_markup="")
    upd.callback_query.message.reply_text(text="you give {n} blood point. \n"
                                "its code {c}".format(n=cq, c=bld.name))
    cur_game.players[upd.effective_chat.id].flag2 ="ready"
