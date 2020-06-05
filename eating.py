import data

def mess(upd, con, cur_game):
    player=cur_game.players[upd.effective_chat.id]
    player.flag1=data.pl_flag1_eat
    upd.callback_query.message.reply_text("enter code")

def eating ( upd, con, cur_game):
    player = cur_game.players[upd.effective_chat.id]
    code = int(upd.message.text)
    if code in cur_game.blood_base:
        dose =cur_game.blood_base.pop(code)
        player.blood+=int(dose.count)
        player.is_ill= dose.is_ill
        upd.message.reply_text(f"you sacsessfuly eat {dose.count} blood point")

    else:
        upd.message.reply_text("this is wrong code")

    player.flag1 = data.pl_flag1_ready