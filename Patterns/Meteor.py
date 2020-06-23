from random import randint

from Patterns.Default import Default
from RGB import RGB


class Meteor(Default):
    data_type = "Meteor"

    def __init__(self, **kwargs):

        super().__init__(**kwargs)
        self.size=10
        self.trail_decay=64
        self.random_decay=True
        self.step=0


    def bound_attrs(self):
        self.size=min(self.size,self.strip_length)

    def fill(self):

        for jdx in range(self.strip_length):
            if not self.random_decay or randint(0,10) > 5:
                self.pixels[jdx]['color'].fade(self.trail_decay)

        for jdx in range( 0, self.size):
            if self.step-jdx< self.strip_length and self.step-jdx>=0:
                self.pixels[self.step-jdx]['color']=self.color.copy()

        self.step+=1
        self.step%=self.strip_length


