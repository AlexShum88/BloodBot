"""тут хранятся базы игроков и мастеров. а так же параметры маскарада, коды крови и города. так же будут, анаверное,
коды доступа в лабораторию. этот файл надо бы сериализировать, либо делать из него ДБ, во избежание. """
import player


class Gaming:
    players= {}
    masters= {}
    blood_base = {}
    mascarade = 1
    sity_key: int = 1234
    gorgul = { }
    lab_keys = []

    def regist_pl(self, id:int, play:player.Player):
        self.players[id]=play
        return
    def start_game(self):
        return

