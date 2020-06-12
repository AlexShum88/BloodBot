import player
import threading
import time
import data

bot:object = 0


def start(pat):
    print("start desease")
    bot.send_message(chat_id=pat.chat_id, text="ill comming")
    vir=threading.Thread(target=desease, args=[pat], daemon=True)
    vir.start()


def desease(pat):
    time.sleep(5)
    bot.send_message(chat_id=pat.chat_id, text=data.desease1)
    time.sleep(6)
    bot.send_message(chat_id=pat.chat_id, text=data.desease2)
    pat.blood = 0
    time.sleep(12)
    bot.send_message(chat_id=pat.chat_id, text=data.desease3)
