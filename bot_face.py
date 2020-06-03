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
from registration_player import Regist_pl
from game import Gaming
from sity import Sity
from givingBLD import Give
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
def start_reg(upd, con):
    rp = Regist_pl(cur_game, upd, con)
    rp.start_reg(upd, con)
    handl_setup(con)



def mess_handl(upd, con):
    print("listen mess")
    comm=cur_game.players[upd.effective_chat.id].curr_handl
    print(comm)

    if comm == "ready":
        game_option(upd, con)
    return


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
    if cq == "give_bld":
        vgb= Give(player,cur_game.blood_base, con)
        vgb.mess(upd, con)
        handl_setup (con)
        for bl, sw in cur_game.blood_base.items():
            print(bl, sw)
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
    sit = Sity(player, bot=con.bot)
    return

def handl_setup (con):
    con.dispatcher.add_handler(MessageHandler(Filters.text, mess_handl))


def main():
    updater = Updater(token=data.token, use_context=True, request_kwargs={
        'read_timeout':6,
        'connect_timeout':7 })
    dp = updater.dispatcher
    start_handler = CommandHandler('start', start_reg)
    dp.add_handler(start_handler, group=0)
    dp.add_error_handler(error)
    updater.start_polling()




    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

main()