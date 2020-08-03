import inspect
import logging
import threading
import time

from rgb import RGB
from utils.color import scale_brightness

pattern_logger = logging.getLogger("pattern_logger")

# the rate is passed as a value>=1 second which is too slow
RATE_DIVISOR = 200


class Default(threading.Thread):
    """
    The default class for patterns
    """

    def __init__(self, handler, rate, pixels, color=RGB()):
        """

        :param handler: The handler for the led strip, either a DotStar_Emulator.emulator.send_test_data.App or a rpi.pi_handler.PiHandler
        :param rate:(float) the rate for the pixel update
        :param pixels: (int) the number of pixels
        :param color: (default RGB), the initial color for the leds
        """

        # init the thread and the handler
        threading.Thread.__init__(self, name="PatternThread")

        rate /= RATE_DIVISOR

        self.handler = handler
        self.rate = rate
        self.stop = False

        self.strip_length = pixels
        self.color = color
        self.alpha=255
        # boolan value to randomize color
        self.randomize_color = False

        # string for patter name
        self.pattern_name = None

        # dictionary storing the modifiers to be implemented in the web app
        self.modifiers = dict()

        # init and set the pixels to the default color
        self.pixels = {idx: dict(color=self.color) for idx in range(self.strip_length + 1)}

    def set_pixels(self):
        for idx in range(self.strip_length):
            self.color_set(idx, self.pixels[idx]['color'])
        self.handler.send()

    def color_all(self, color):
        for idx in range(self.strip_length):
            self.pixels[idx]['color'] = color

    def color_set(self, index, rgb):

        if isinstance(rgb, RGB):
            r = rgb.r
            g = rgb.b
            b = rgb.b
            a = rgb.a
        elif isinstance(rgb, tuple) or isinstance(rgb, list):
            assert len(rgb) == 4, "The length of the color should be 4"
            r, g, b, a = rgb

        else:
            raise ValueError(f"Class {rgb.__class__} not recognized")

        # scale rgb based on passed alpha
        r,g,b=[scale_brightness(elem,a) for elem in (r,g,b)]

        self.handler.set(index=index, r=r, g=g, b=b, a=self.alpha)

    def fill(self):

        raise NotImplementedError

    def on_loop(self):
        self.fill()
        self.set_pixels()
        time.sleep(self.rate)

    def update_args(self, **kwargs):
        variables = [i for i in dir(self) if not inspect.ismethod(i)]

        changed = False
        for k in kwargs.keys():
            if k in variables:
                setattr(self, k, kwargs[k])
                changed = True

        if not changed:
            for k in kwargs.keys():
                pattern_logger.warn(f"No such attribute named '{k}' for class {self.__str__()}")

        return changed

    def close(self):
        self.stop = True
        pattern_logger.info(f"Pattern {self.pattern_name} stopped")

    def run(self):
        # init handler and set pixels
        self.set_pixels()

        pattern_logger.info(f"Started pattern: {self.pattern_name} with rate: {self.rate}")
        try:
            while not self.stop:
                self.on_loop()
        except KeyboardInterrupt:
            pattern_logger.info("Pattern has been interrupted")
            self.close()

    def bound_attrs(self):
        """
        override this function if the fill method to bound attributes to a limited range
        :return:
        """
        raise NotImplementedError()

    def set_rate(self, rate):
        rate /= RATE_DIVISOR
        self.rate = rate
