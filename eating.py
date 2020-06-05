import data

def mess(upd, con, cur_game):
    player=cur_game.players[upd.effective_chat.id]
    player.flag1=data.pl_flag1_eat
    upd.callback_query.message.reply_text(data.pl_mess_ent_code)

def eating ( upd, con, cur_game):
    player = cur_game.players[upd.effective_chat.id]
    code = ""
    try:
        code = int(upd.message.text)
    except:
        upd.message.reply_text(data.pl_mess_wrong_code)
    if code in cur_game.blood_base:
        dose =cur_game.blood_base.pop(code)
        player.blood+=int(dose.count)
        player.is_ill= dose.is_ill
        upd.message.reply_text(f"you sacessfuly eat {dose.count} blood point")

    else:
        upd.message.reply_text(data.pl_mess_wrong_code)

    player.flag1 = data.pl_flag1_ready