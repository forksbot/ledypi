from copy import deepcopy
from random import randint

from DotStar_Emulator.emulator.send_test_data import App

from RGB import RGB
from utils import bound_sub, bound_add


class RandomFading(App):
    data_type = "RandomFading"

    def __init__(self, args, random_points=20, delay_start=4, delay_end=20):
        """
        Init for snow effect
        :param args:
        """

        # assert delays are in range
        assert 0 <= delay_start <= 20
        assert 0 <= delay_end <= 20

        super().__init__(args)
        self.random_points = random_points
        self.delay_start = delay_start
        self.delay_end = delay_end
        self.strip_length = self.grid_size.x + self.grid_size.y - 1

        # assert there are no more points than leds
        assert random_points < self.strip_length
        self.centers = {randint(0, self.strip_length - 1): self.empty_center() for _ in range(random_points)}

    def empty_center(self):
        """
        Return an empty center point as a dict with fields
        :return:
        """

        default_dict = dict(color=RGB(random=True), alpha=0, delay=randint(0, 10), increasing=True)

        # if there is no start in delay then alpha is maximum
        if not self.delay_start:
            default_dict['alpha'] = 255

        return default_dict

    def set(self, index, rgb, **kwargs):
        """
        use set with RGB class
        :param index: index of led to set
        :param rgb: RGB class color
        :param kwargs: ...
        :return:
        """

        super().set(index, rgb.c, rgb.r, rgb.b, rgb.b)

    def fill(self):

        # copy original dict
        center_copy = deepcopy(self.centers)

        # for every center in the list
        for c, attr in center_copy.items():

            # get attributes
            color = attr["color"]
            alpha = attr['alpha']
            delay = attr['delay']
            increasing = attr['increasing']
            done = False

            # if point has to wait more then wait
            if delay > 0:
                self.centers[c]['delay'] -= 1
                continue

            # if increasing and there is still room for increasing do it
            if 0 <= alpha < 255 and increasing:
                alpha = bound_add(alpha, self.delay_start, maximum=255)
            # if not increasing and still in good range, decrease
            elif 0 < alpha <= 255 and not increasing:
                alpha = bound_sub(alpha, self.delay_end, minimum=0)
            # if zero and decreasing we're done
            elif alpha == 0 and not increasing:
                done = True
            # if 255 and increasing then start decreasing
            elif alpha == 255 and increasing:
                increasing = False

            # update and set color
            color.update_single(c=alpha)
            self.set(c, color)

            # update for original dict too
            self.centers[c]['alpha'] = alpha
            self.centers[c]['increasing'] = increasing

            # if is done
            if done:
                # pop center
                self.centers.pop(c)
                # get a new one
                new_c = randint(0, self.strip_length - 1)
                while new_c in self.centers.keys():
                    new_c = randint(0, self.strip_length - 1)
                # add it to list
                self.centers[new_c] = self.empty_center()

    def on_loop(self):
        self.fill()
        self.send()
