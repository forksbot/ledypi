
from Fillers.Default import Default
from RGB import RGB


class Snow(Default):
    data_type = "Snow"

    def __init__(self, rate, trail=5):
        """
        Init for snow effect
        :param args: for App
        :param trail_length: length of snow trail
        """
        super().__init__(rate)

        self.trail = trail
        self.min_space = 3  # min space between trail end and trail start
        self.counter = 0

    def fill(self):

        # get the number of trails the strip can have
        num_of_trail = self.strip_length // (self.trail + self.min_space)
        # make them even
        if num_of_trail % 2 != 0:
            num_of_trail -= 1

        intensity = 255
        loss = intensity // self.trail  # loss of intensity for trail

        for jdx in reversed(range(num_of_trail)):
            for idx in range(jdx + self.counter, self.strip_length + jdx + self.counter, num_of_trail):
                self.pixels[idx % self.strip_length]['color']=RGB(r=255,g=255,b=255,c=intensity)

            if not intensity - loss < 0:
                intensity -= loss
            else:
                intensity = 0

        self.update_counter()
        self.set_pixels()

    def update_counter(self):
        self.counter += 1
        self.counter %= self.strip_length
