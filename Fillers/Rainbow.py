from DotStar_Emulator.emulator.send_test_data import App
from math import sin, pi, floor

from utils import scale


class Rainbow(App):

    data_type = "FireWork"

    def __init__(self, args):
        """
        Init for FireWork effect
        :param args:
        """
        super().__init__(args)

        self.strip_length=self.grid_size.x+self.grid_size.y
        self.counter=0

    def fill(self):

        for idx in range(self.strip_length):

            idx2degree=scale(idx+self.counter,0,360,0,self.strip_length)
            r=sin(idx2degree)
            g=sin(idx2degree+pi/2)
            b=sin(idx2degree+pi)

            r=scale(r,0,255,-1,1)
            g=scale(g,0,255,-1,1)
            b=scale(b,0,255,-1,1)

            r=floor(r)
            g=floor(g)
            b=floor(b)

            self.set(idx, 255, r, g, b)

        self.counter+=1
        self.counter%=self.strip_length

    def on_loop(self):
        self.fill()
        self.send()