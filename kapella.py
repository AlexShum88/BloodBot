
import logging
import threading
import time
import data

def kapella_def_sys(cur_game, bot):
    """эта штука раз по таймеру проверяет какие у нас есть игроки. Есди игрок не в городе (а значит он в капелле)
    она его ебает на 1 крови"""
    while True:
        time.sleep(data.capella_timer)
        for pl in cur_game.players.values():
            if pl.flag2 == data.pl_flag2_sity:
                continue
            pl.blood-=1
            print(f"current blood is{pl.blood}")
            bot.send_message(chat_id=pl.chat_id, text=f"current blood is{pl.blood}")