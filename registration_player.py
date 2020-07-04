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
    cont.bot.send_message(chat_id=upd.effective_chat.id, text=data.reg_listen_name)
    cur_game.players[upd.effective_chat.id].flag1 = data.pl_flag1_reg
    change_player_handl(upd, "name", cur_game)
    return


def change_player_handl(upd, new_handl, cur_game):
    cur_game.players[upd.effective_chat.id].flag2 = new_handl


def reg_name(upd, cont, cur_game):
        cur_game.players[upd.effective_chat.id].name = upd.message.text
        cont.bot.send_message(chat_id=upd.effective_chat.id, text=data.reg_listen_blood)
        change_player_handl(upd, "blood", cur_game)
        return


def reg_blood_clan(upd, cont, cur_game):
    if str(upd.message.text).isnumeric():
        bl = int(upd.message.text)
        if bl<10 and bl>0:
            cur_game.players[upd.effective_chat.id].blood = upd.message.text
        else:
            cont.bot.send_message(chat_id=upd.effective_chat.id, text=data.reg_blood_wrong_diapasone)
            return
    else:
        cont.bot.send_message(chat_id=upd.effective_chat.id, text=data.reg_blood_nonum)
        return
    cont.bot.send_message(chat_id=upd.effective_chat.id, text=data.reg_listen_clan)
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
    upd.message.reply_text(data.reg_shoose_clan, reply_markup=reply_markup)
    return

def reg_disciplines(upd, cont, cur_game):
    cq = upd.callback_query.data
    player = cur_game.players[upd.effective_chat.id]
    cur_game.players[upd.effective_chat.id].clan = cq
    for dis in data.clanes[cq]:
        player.disciplines.append(dis)
        player.dis_for_fight[dis]=data.disciplines[dis]
    if "Тауматургия" in player.disciplines:
        taumturg_menu(upd, cont, cur_game)
        player.flag2 = data.pl_flag2_tau
    else:
        end_reg(upd, cont, cur_game)
    return

def taumturg_menu(upd, con, cur_game):
    player = cur_game.players[upd.effective_chat.id]
    keyb=[]
    for dis in data.disciplines.keys():
        if dis in player.disciplines:
            continue

        bt=InlineKeyboardButton(text=f"{dis}", callback_data=dis)
        row=[bt]
        keyb.append(row)
    reply_markup=InlineKeyboardMarkup(keyb)
    con.bot.send_message(chat_id=upd.effective_chat.id, text="for fight get another disciplines property (click to read more)",
                             reply_markup=reply_markup)
    return

def taumaturg_listener(upd, con, cur_game):

    def tf_nemu():
        keyb=[]
        bt_tr=InlineKeyboardButton(text=f"Accept", callback_data="+")
        bt_fls= InlineKeyboardButton(text=f"return", callback_data="-")
        row1=[bt_tr]
        row2=[bt_fls]
        keyb.append(row1)
        keyb.append(row2)
        reply_markup=InlineKeyboardMarkup(keyb)
        return reply_markup

    cq = upd.callback_query.data
    player = cur_game.players[upd.effective_chat.id]
    if cq in data.disciplines.keys():
        con.bot.send_message(chat_id=upd.effective_chat.id, text=f"{cq} \n {data.disciplines[cq]}", reply_markup=tf_nemu())
    elif cq == "+":
        player.dis_for_fight["Тауматургия"] = data.disciplines[upd.callback_query.message.text.split()[0]]
        end_reg(upd, con, cur_game)
    elif cq == "-":
        taumturg_menu(upd, con, cur_game)


def end_reg(upd, con, cur_game):
    player = cur_game.players[upd.effective_chat.id]
    player.disciplines.append(data.no_dis_txt)
    player.dis_for_fight[data.no_dis_txt] = data.no_dis_txt
    print(player.name, player.blood, player.clan)
    con.bot.send_message(chat_id=upd.effective_chat.id, text=data.reg_ready + "\n" + str(player))
    player.flag1 = data.pl_flag1_ready
    player.flag2 = data.pl_flag2_ready
