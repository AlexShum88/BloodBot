""" зберігання поточної бази гравців, їх екземплярів, станів гри
лічильник маскараду, лічильник кількості  невикористаної крові в полі, набір кодів крові
(повинно відсікати при використанні), статус капели.
метод генерації кодів, методи регестрації гравців, їх знищення"""
import player
import random as roll

class Gaming:
    players= {}
    masters={}
    num_base = []

    def regist_pl(self, id:int, play:player.Player):
        self.players[id]=play
        return

    def start_game(self):
        return

    def reg_num(self, uneed:int):
        """штука для генерации кодов. например для крови."""
        for num in range(uneed):
            rr = roll.randint(1000, 9999)
            if rr not in self.num_base:
                self.num_base.append(rr)

