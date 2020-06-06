"""тут будуть методи, для взаємодії саме з ботом, обгортка для методів інших класів. """

"""набір фронтендів для взаємодій. Це єдине місце де код повинен бути завязаний на бота."""
import threading
import telegram
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler,
                          ConversationHandler)
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


import data
import registration_player as rp
from game import Gaming
from sity import Sity
import givingBLD as gb
import eating as eat
cur_game = Gaming()

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)



def mess_dispatcer(upd, con):
    """сюда поступает основной поток текстовых сообщений от пользователя
    и производится выборка что дальше этому пользователю запускать"""
    flag1 = cur_game.players[upd.effective_chat.id].flag1
    print(flag1)
    if flag1 == data.pl_flag1_reg:
        rp.messs_handl(upd, con, cur_game)
    if flag1 == data.pl_flag1_ready:
        game_option(upd, con)
    elif flag1 == data.pl_flag1_eat:
        eat.eating(upd, con, cur_game)

    return


def callback_dispatcher(upd, con):
    """эта шняга активируется когда прилетает саллбек от нажатия кнопки. он адолжна сначала посмотреть на флажок юзера,
    и решить с какой группой соотносить прилетевший каллбек. ну и потом соотнести и вызвать необходимую команду"""
    cq = upd.callback_query.data
    player = cur_game.players[upd.effective_chat.id]
    flag1 = player.flag1
    flag2 = player.flag2

    if flag2 == data.pl_flag2_reg_dis:
        rp.reg_disciplines(upd, con, cur_game)

    elif flag2 == data.pl_flag2_givebld:
        gb.resualt(upd, con, cur_game)

    elif flag2 == data.pl_flag2_sity:
        player.sity.listen_answer(upd, con)
        player.sity = None


    if flag1 == data.pl_flag1_ready and flag2 == data.pl_flag2_ready:
        if cq == data.player_options["give blood"]:
            gb.mess(upd, con, cur_game)
        elif cq == data.player_options["sity"]:
            to_sity(upd, con)
        elif cq == data.player_options["drink blood"]:
            eat.mess(upd, con, cur_game)
        elif cq == data.player_options["player data(for test)"]: #player data
            upd.callback_query.message.reply_text(str(player))
        else:
            upd.callback_query.message.reply_text(data.menu_wrong_callback)
            return

    return

def game_option(upd, con):
    """эта шняга смотрит какие опции возможны для игрока и выдает соотвествующий список кнопок"""
    keyb = []
    for opt, callb in data.player_options.items():
        bt = InlineKeyboardButton(text=opt, callback_data=callb)
        row = [bt]
        keyb.append(row)
    reply_markup = InlineKeyboardMarkup(keyb)
    upd.message.reply_text(data.menu_chouse, reply_markup=reply_markup)
    return

def start_reg(upd, con):
    """игрок стартует отсюда: начало регистрации"""
    if upd.effective_chat.id in cur_game.players:
        mess_dispatcer(upd, con)
    else:
        rp.start_reg(upd, con, cur_game)
        t=threading.Timer(10.0, myfun, [con])
        t.start()


def to_sity(upd, con):
    player=cur_game.players[upd.effective_chat.id]
    player.sity = Sity(player, con, cur_game)
    return

def myfun(con):
    for pl in cur_game.players.values():
        pl.blood-=1
        print (f"current blood is{pl.blood}" )
        con.bot.send_message(chat_id=pl.chat_id, text=f"current blood is{pl.blood}" )




def main():
    updater = Updater(token=data.token, use_context=True, request_kwargs={
        'read_timeout':6,
        'connect_timeout':7 })
    dp = updater.dispatcher
    start_handler = CommandHandler('start', start_reg)
    dp.add_handler(start_handler, group=1)
    dp.add_handler(MessageHandler(Filters.text, mess_dispatcer), group=1)
    dp.add_handler(CallbackQueryHandler(callback_dispatcher), group=1)
    #dp.add_handler(CommandHandler('menu', game_option))

    dp.add_error_handler(error)
    updater.start_polling()





    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

main()