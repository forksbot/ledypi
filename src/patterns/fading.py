from copy import deepcopy
from random import randint

from patterns.default import Default
from rgb import RGB
from utils import bound_sub, bound_add


class Fading(Default):
    data_type = "Fading"

    def __init__(self, **kwargs):

        super().__init__(**kwargs)


        self.point_number = 29
        self.rate_start = 40
        self.rate_end = 4

        # assert there are no more points than leds
        self.centers = {randint(0, self.strip_length - 1): self.empty_center() for _ in range(self.point_number)}

    def empty_center(self):
        """
        Return an empty center point as a dict with fields
        :return:
        """


        if self.randomize_color:
            default_dict = dict(color=RGB(random=True), alpha=0, delay=randint(0, 100), increasing=True)
        else:
            default_dict = dict(color=RGB(rgb=self.color), alpha=0, delay=randint(0, 100), increasing=True)

        # if there is no start in delay then alpha is maximum
        if not self.rate_start:
            default_dict['alpha'] = 255

        return default_dict


    def fill(self):

        # copy original dict
        center_copy = deepcopy(self.centers)
        
        # bound the rnadom point to the maximum 
        self.point_number = min(self.point_number, self.strip_length)

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
                alpha = bound_add(alpha, self.rate_start, maximum=255)
            # if not increasing and still in good range, decrease
            elif 0 < alpha <= 255 and not increasing:
                alpha = bound_sub(alpha, self.rate_end, minimum=0)
            # if zero and decreasing we're done
            elif alpha == 0 and not increasing:
                done = True
            # if 255 and increasing then start decreasing
            elif alpha == 255 and increasing:
                increasing = False

            # update and set color
            color.update_single(c=alpha)
            self.pixels[c]['color']=color

            # update for original dict too
            self.centers[c]['alpha'] = alpha
            self.centers[c]['increasing'] = increasing

            # if is done
            if done:
                # pop center
                self.centers.pop(c)

                # if centers are less than supposed, add other
                if len(self.centers) < self.point_number:
                    # get a new one
                    new_c = randint(0, self.strip_length - 1)
                    while new_c in self.centers.keys():
                        new_c = randint(0, self.strip_length - 1)
                    # add it to list
                    self.centers[new_c] = self.empty_center()
