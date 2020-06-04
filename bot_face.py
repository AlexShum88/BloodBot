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
    if flag1 == "reg":
        rp.messs_handl(upd, con, cur_game)
    if flag1 == "ready":
        game_option(upd, con)
    elif flag1 == "eat":
        eat.eating(upd, con, cur_game)

    return


def callback_dispatcher(upd, con):
    """эта шняга активируется когда прилетает саллбек от нажатия кнопки. он адолжна сначала посмотреть на флажок юзера,
    и решить с какой группой соотносить прилетевший каллбек. ну и потом соотнести и вызвать необходимую команду"""
    cq = upd.callback_query.data
    player = cur_game.players[upd.effective_chat.id]
    flag1 = player.flag1
    flag2 = player.flag2

    if flag2 == "blcl":
        rp.reg_disciplines(upd, con, cur_game)

    elif flag2 == "givebld":
        gb.resualt(upd, con, cur_game)

    elif flag2 == "sity":
        player.sity.listen_answer(upd, con)
        player.sity = None


    if flag1 == "ready" and flag2 == "ready":
        if cq == "give_bld":
            gb.mess(upd, con, cur_game)
        elif cq == "sity":
            to_sity(upd, con)
            return
        elif cq == "cast":
            return
        elif cq == "fight":
            return
        elif cq == "code":
            return
        elif cq == "bld":
            player.flag1="eat"
            eat.mess(upd, con)
        elif cq == "pldt": #player data
            upd.callback_query.message.reply_text(str(player))
        else:
            upd.callback_query.message.reply_text("please, answer for another qestion")
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
    upd.message.reply_text('Please, choose one:', reply_markup=reply_markup)
    return

def start_reg(upd, con):
    """игрок стартует отсюда: начало регистрации"""
    if upd.effective_chat.id in cur_game.players:
        mess_dispatcer(upd, con)
    else:
        rp.start_reg(upd, con, cur_game)


def drink_blood(upd, con):
    """по ходу питаться они должны через коды. коды создаются и регистрируются в игре. и после использования стираются. сразу."""

    return

def to_sity(upd, con):
    player=cur_game.players[upd.effective_chat.id]
    player.sity = Sity(player, con)
    player.flag2 = "sity"
    return



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