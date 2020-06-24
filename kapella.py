"""тут логіка капелли, А саме система забору крові за перебування у капеллі"""

"""звертатись до пакунку гравців та знімати з кожного з них поінт крові, коли до того прийде час. ймовірно для цього 
потрібно освоїти паралельні потоки """
import logging
import threading
import time
import data

def kapella_def_sys(cur_game, bot):
    while True:
        time.sleep(120)
        for pl in cur_game.players.values():
            if pl.flag2 == data.pl_flag2_sity:
                continue
            pl.blood-=1
            print(f"current blood is{pl.blood}")
            bot.send_message(chat_id=pl.chat_id, text=f"current blood is{pl.blood}")