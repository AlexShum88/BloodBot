"""тут будуть методи, для взаємодії саме з ботом, обгортка для методів інших класів. """

"""набір фронтендів для взаємодій. Це єдине місце де код повинен бути завязаний на бота."""


import telegram
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler,
                          ConversationHandler)
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


import data
import player
from game import Gaming
from sity import Sity
cur_game = Gaming()

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


"""" def start_listen(self, funname):
        self.ms_handl = MessageHandler(Filters.text, funname)
        self.dp.add_handler(self.ms_handl)
        print("start")
        return


    def end_listen(self):
        self.dp.remove_handler(self.ms_handl)
        print("end")
        return"""
#ctart player registration


def start_reg(upd, cont):
    cur_game.regist_pl(upd.effective_chat.id, player.Player(upd.effective_chat.id))
    reg(upd, cont)
    return

def mess_handl(upd, con):
    print("listen mess")
    comm = cur_game.players[upd.effective_chat.id].curr_handl
    print(comm)
    if comm == "name":
        reg_name(upd, con)
    elif comm == "blood":
        reg_blood_clan(upd, con)
    elif comm == "ready":
        game_option(upd, con)
    elif comm == "eating":
        drink_blood(upd,con)
    else:
        reg(upd, con)
    return

def change_player_handl(upd, new_handl):
    cur_game.players[upd.effective_chat.id].curr_handl = new_handl


def reg(upd, cont):
    cont.bot.send_message(chat_id=upd.effective_chat.id, text="Im listen for your name")
    change_player_handl(upd, "name")
    return


def reg_name(upd, cont):
    cur_game.players[upd.effective_chat.id].name = upd.message.text
    cont.bot.send_message(chat_id=upd.effective_chat.id, text="Im listen for your blood")
    change_player_handl(upd, "blood")
    return

def reg_blood_clan(upd, cont):
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
    #change_player_handl(cur_game.players[upd.effective_chat.id], "clan")
    return

def reg_clan(upd, cont):
    keyb = []
    for clan in data.clanes:
        bt = InlineKeyboardButton(text=clan, callback_data=clan)
        row = [bt]
        keyb.append(row)
    reply_markup = InlineKeyboardMarkup(keyb)
    upd.message.reply_text('Please, choose one:', reply_markup=reply_markup)
    cont.dispatcher.add_handler(CallbackQueryHandler(reg_disciplines))
    #print(cont.dispatcher.handlers[0])
    return

def reg_disciplines(upd, cont):
    cq = upd.callback_query.data
    player = cur_game.players[upd.effective_chat.id]
    cur_game.players[upd.effective_chat.id].clan = cq
    print(player.name, player.blood, player.clan)
    cont.bot.send_message(chat_id=upd.effective_chat.id, text="you registration complete \n"
                           "sent me sign, if you need something")
    player.curr_handl = "ready"
    cont.dispatcher.remove_handler(cont.dispatcher.handlers[0][-1])

    """ниже кусок тупо для теста. """
    if player.clan == "Malcovian":
        player.disciplines=['Стремительность', 'Затемнение', 'Могущество', "Без применения дисциплин"]
    #print(cont.dispatcher.handlers[0])
    return

#registration players metod end


def game_option(upd, con): #дивиться, які опції для гравця можливі звіряючись з переліком в даті. видає кнопки
    keyb = []
    for opt, callb in data.player_options.items():
        bt = InlineKeyboardButton(text=opt, callback_data=callb)
        row = [bt]
        keyb.append(row)
    reply_markup = InlineKeyboardMarkup(keyb)
    upd.message.reply_text('Please, choose one:', reply_markup=reply_markup)
    con.dispatcher.add_handler(CallbackQueryHandler(option_dispatcher))
    return

def option_dispatcher(upd, con):  #шняга, що читає калбек та вирішує який метод далі включити для плеєра
    cq = upd.callback_query.data
    con.dispatcher.remove_handler(con.dispatcher.handlers[0][-1])
    player = cur_game.players[upd.effective_chat.id]
    if cq == "bld":
        player.curr_handl="eating"
        con.bot.send_message(chat_id=upd.effective_chat.id, text="how many blood you get?")
    elif cq == "sity":
        to_sity(upd, con)
        return
    elif cq == "cast":
        return
    elif cq == "fight":
        return
    elif cq == "code":
        return

    return

def drink_blood(upd, con):
    """по ходу питаться они должны через коды. коды создаются и регистрируются в игре. и после использования стираются. сразу."""

    return

def to_sity(upd, con):
    player=cur_game.players[upd.effective_chat.id]
    sit = Sity(player, context=con)
    return

def main():
    updater = Updater(token=data.token, use_context=True, request_kwargs={
        'read_timeout':6,
        'connect_timeout':7 })
    dp = updater.dispatcher
    start_handler = CommandHandler('start', start_reg)
    dp.add_handler(start_handler)
    ms_handler = MessageHandler(Filters.text, mess_handl)
    dp.add_handler(ms_handler)

    dp.add_error_handler(error)
    updater.start_polling()




    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

main()