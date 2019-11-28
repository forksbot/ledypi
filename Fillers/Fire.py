from math import ceil
from random import randint

from Fillers.Default import Default
from RGB import RGB
from utils import bound_sub


class Fire(Default):
    data_type = "Fire"

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        self.cooling = 2
        self.sparking = 50
        self.alpha = 255
        self.cooldown_list = [0 for _ in range(self.strip_length)]

    def bound_attrs(self):
        self.sparking = min(self.sparking, 255)

    def fill(self):

        self.bound_attrs()

        # cooling_down
        for idx in range(self.strip_length):
            cooldown = randint(0, ceil(((self.cooldown_list[idx] * 10) / self.strip_length)) + self.cooling)
            self.cooldown_list[idx] = bound_sub(self.cooldown_list[idx], cooldown, minimum=0)

        for idx in range(self.strip_length - 1, 2, -1):
            self.cooldown_list[idx] = (self.cooldown_list[idx - 1] + self.cooldown_list[idx - 2] + self.cooldown_list[idx - 2]) / 3

        if randint(0, 255) < self.sparking:
            y = randint(0, 7)
            self.cooldown_list[y] = self.cooldown_list[y] + randint(160, 255)

        for idx in range(self.strip_length):
            self.pixels[idx]['color'] = heat_to_rgb(self.cooldown_list[idx])


def heat_to_rgb(temperature):
    t192 = round((temperature / 255.0) * 191)
    heatramp = t192 & 0x3F
    heatramp <<= 2

    if t192 > 0x80:
        return RGB(r=255, g=255, b=heatramp, c=255)
    elif t192 > 0x40:
        return RGB(r=255, g=heatramp, b=0, c=255)
    else:
        return RGB(r=heatramp, g=0, b=0, c=255)
