class Banana:
    food_group="fruit"
    colors=["green","green-yellow","yellow","brown spotted","black"]

    __ripe_colors=['yellow',"brown spotted"]

    def __str__(self):
        return f"{self.color} {self.__class__.__name__}"

    def __init__(self,color="green"):
        if not self.check_color(color):
            raise ValueError(f"Ia {self.__class__.__name__} cannot be {color}!")
        self.color=color

    def _is_ripe(self):
        return self.color in self.__ripe_colors

    def can_eat(self,must_be_ripe=False):
        if must_be_ripe and not self._is_ripe():
            return False
        return True

    def peel(self):
       self.peel=False

    def set_color(self,color):
        if color in self.colors:
           self.color=color
        else:
            raise ValueError(f"Ia banana cannot be {color}!")

    @classmethod
    def check_color(cls,color):
        return color in cls.colors

    @classmethod
    def make_greenie(cls):
        banana=cls()
        banana.set_color("green")
        return banana

    @staticmethod
    def estimate_calories(num_bananas):
      return num_bananas * 105


class RedBanana(Banana):

    colors=['green','orange','brown','red','black']
    botanical_name= "red dacca"

    def peel(self):
        super().peel()
        print("It looks like a regular banana inside!")

    def set_color(self,color):
        if color not in self.colors:
            raise ValueError(f"A Red Banana cannot be {color}!")

my_banana=Banana()
my_banana.set_color("green")
my_banana.peel()
print(my_banana)
