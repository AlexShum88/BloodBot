from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler,
                          ConversationHandler)
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


import data
import player


def messs_handl(upd, con, cur_game):
    print("listen mess")
    comm = cur_game.players[upd.effective_chat.id].flag2
    if comm == "name":
        reg_name(upd, con, cur_game)
    elif comm == "blood":
        reg_blood_clan(upd, con, cur_game)
    elif comm == data.pl_flag2_ready:
        return

    return


def start_reg(upd, cont, cur_game):
    cur_game.regist_pl(upd.effective_chat.id, player.Player(upd.effective_chat.id))
    cont.bot.send_message(chat_id=upd.effective_chat.id, text="Im listen for your name")
    cur_game.players[upd.effective_chat.id].flag1 = data.pl_flag1_reg
    change_player_handl(upd, "name", cur_game)
    return


def change_player_handl(upd, new_handl, cur_game):
    cur_game.players[upd.effective_chat.id].flag2 = new_handl


def reg_name(upd, cont, cur_game):
        cur_game.players[upd.effective_chat.id].name = upd.message.text
        cont.bot.send_message(chat_id=upd.effective_chat.id, text="Im listen for your blood")
        change_player_handl(upd, "blood", cur_game)
        return


def reg_blood_clan(upd, cont, cur_game):
    if str(upd.message.text).isnumeric():
        bl = int(upd.message.text)
        if bl<10 and bl>0:
            cur_game.players[upd.effective_chat.id].blood = upd.message.text
        else:
            cont.bot.send_message(chat_id=upd.effective_chat.id, text="blood must be >0 and <10")
            return
    else:
        cont.bot.send_message(chat_id=upd.effective_chat.id, text="enter num")
        return
    cont.bot.send_message(chat_id=upd.effective_chat.id, text="Im listen for your clan")
    reg_clan(upd, cont)
    cur_game.players[upd.effective_chat.id].flag2=data.pl_flag2_reg_dis
    return

def reg_clan(upd, cont):
    keyb = []
    for clan in data.clanes: #переделать клан на словарь с дисциплинами
        bt = InlineKeyboardButton(text=clan, callback_data=clan)
        row = [bt]
        keyb.append(row)
    reply_markup = InlineKeyboardMarkup(keyb)
    upd.message.reply_text('Please, choose one:', reply_markup=reply_markup)
    return

def reg_disciplines(upd, cont, cur_game):
    cq = upd.callback_query.data
    player = cur_game.players[upd.effective_chat.id]
    cur_game.players[upd.effective_chat.id].clan = cq
    print(player.name, player.blood, player.clan)
    cont.bot.send_message(chat_id=upd.effective_chat.id, text="you registration complete \n"
                            "sent me sign, if you need something")
    player.flag1 = data.pl_flag1_ready
    player.flag2 = data.pl_flag2_ready

    if player.clan == "Malcovian":
        player.disciplines=['Стремительность', 'Затемнение', 'Могущество', data.no_dis_txt]

    return


    #registration players metod end