
import random as roll

class Blood:
    def __init__(self, base, bl_count, is_ill, pl_from):
        self.name = self.num_gen(base)
        self.count = bl_count
        self.is_ill = is_ill
        self.pl_from = pl_from
        self.add_to_base(base)


    def num_gen(self, base:dict):
        rr = roll.randint(1000, 8999)
        if rr not in base:
            return rr
        else:
            self.num_gen(base)

    def add_to_base(self,base):
        base[self.name]= self

    def __str__(self):
        st = "{n} {c} {ill} {player}".format(n=self.name, c=self.count, ill=self.is_ill, player=self.pl_from.name)
        return