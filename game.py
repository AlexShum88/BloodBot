""" зберігання поточної бази гравців, їх екземплярів, станів гри
лічильник маскараду, лічильник кількості  невикористаної крові в полі, набір кодів крові
(повинно відсікати при використанні), статус капели."""
import player


class Gaming:
    players= {}
    masters= {}
    blood_base = {}
    mascarade = 0
    sity_key: int = 1234
    def regist_pl(self, id:int, play:player.Player):
        self.players[id]=play
        return
    def start_game(self):
        return

