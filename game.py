""" зберігання поточної бази гравців, їх екземплярів, станів гри
лічильник маскараду, лічильник кількості  невикористаної крові в полі, набір кодів крові
(повинно відсікати при використанні), статус капели.
метод генерації кодів, методи регестрації гравців, їх знищення"""
import player


class Gamer:
    players= {}
    masters={}

    def regist_pl(self, id:int, play:player.Player):
        self.players[id]=play
        return
    def start_game(self):
        return

