"""файл класу гравця де його методи реєстрації, дій,"""
import sity
import virus


class Player:
    def __init__(self,chatid):
        self.chat_id=chatid
        self.__name: str="undefined"
        self.__blood: int=0
        self.clan = "undefined"
        self.__walking=list()  #список місчь куди ця падла вже ходила
        self.disciplines=[]  #виставляється вибором клану, чи все таки вручну?
        self.__is_ill=False
        self.now_walk=[]
        self.flag1 ="start" #its pl status: ono registration, on game, on torpor, dead?....
        self.flag2 = "start" #its for change callback listener
        self.sity: sity.Sity
        self.status = "normal"
        self.hp = 5
        self.bloodlines = 0
        self.fight = ""



    @property
    def walking(self):
       return self.__walking

    @walking.setter
    def walking(self, wa):
       self.__walking.append(wa)

    @property
    def blood(self):
       return self.__blood

    @blood.setter
    def blood(self, bl):
       if type(bl)==int or bl.isnumeric():
           self.__blood=int(bl)
           if self.__blood<0:
               self.__blood=0

    @property
    def name(self):
       return self.__name

    @name.setter
    def name(self, nm):
       self.__name=nm

    @property
    def is_ill(self):
       return self.__is_ill

    @is_ill.setter
    def is_ill(self, il):
       if type(il) == bool:
           if not self.__is_ill and il:
               virus.start(self)

           self.__is_ill=il
       return


    def __str__(self):
        s= f"Name {self.__name} \n" \
           f"blood {self.__blood} \n" \
           f"ill {self.__is_ill}\n" \
           f"flag1 {self.flag1}, flag2 {self.flag2}"
        return s

    def set_dysciplines(self):
       pass