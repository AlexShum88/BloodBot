"""файл класу гравця де його методи реєстрації, дій,"""

class Player:
   def __init__(self,chatid, name, clan, blood):
       self.chat_id=chatid
       self.__name: str=name
       self.__blood: int=0
       self.__walking=list()  #список місчь куди ця падла вже ходила
       self.disciplines=[]  #виставляється вибором клану, чи все таки вручну?
       self.__is_ill=False
       self.now_walk=[]

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
       if bl.isnumeric():
           self.__blood=int(bl)

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
           self.__is_ill=il
       return


   def register(self):
       return
   def set_dysciplines(self):
       return
   def eating(self):
       """харчування в любому вигляді"""
       return
   def hunting(self):
       """метод для полювання любого. вибір типу полювання буде через параметр крові та дозвіл від майстра. """
       return

"""додати смерть персонажа"""

