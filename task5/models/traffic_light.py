import datetime
import time
import itertools


GREEN = 'green'
YELLOW = 'yellow'
RED = 'red'
BLINKING_YELLOW = 'blinking yellow'

YELLOW_TIME = 3
GREEN_TIME = 10
RED_TIME = 10


MANUAL_HINT = """
    0: Green,
    1: Yellow,
    2: Red,
    -x: exit, and return to auto mode
    """

MANUAL = {
    "0": GREEN,
    "1": YELLOW,
    "2": RED,
}


class BaseTrafficLight:
    next_id = itertools.count(1)

    def __init__(self, color):
        self.id = next(TrafficLight.next_id)
        self.color = color

        self.auto = True
        self.time = None
        self.time_to_switch  = None

        self.start_night_time = 1
        self.end_night_time = 5

    @property
    def info(self):
        info = {
            'color': self.color,
            'auto': self.auto,
            'time_to_switch': self.time_to_switch
        }
        return info

    def start(self):
        while self.auto:
            if self.is_night_time():
                self.night_mode()
            else:
                for light, time_ in self._lights_cycle():
                    self.light(light, time_)

    def light(self, color, time_):
        self.color = color
        self.time_to_switch = time_
        while self.time_to_switch and self.auto:
            time.sleep(1)
            self.time_to_switch -= 1

    def _lights_cycle(self):
        if self.color == GREEN:
            lights = (GREEN, GREEN_TIME), (YELLOW, YELLOW_TIME), (RED, RED_TIME)
        else:
            lights = (RED, RED_TIME), (YELLOW, YELLOW_TIME), (GREEN, GREEN_TIME)
        for light, color in lights:
            yield light, color

    def is_night_time(self):
        hour = datetime.datetime.now().hour
        return self.start_night_time <= hour < self.end_night_time

    def night_mode(self):
        self.mode = NIGHT_MODE
        while self.is_night_time() and self.auto:
            self.color = YELLOW
            self.time_to_switch = None
            time.sleep(.5)

    def __repr__(self):
        return 'Traffic light %s' % self.id


class TrafficLight(BaseTrafficLight):

    def manual_switch():
        print(MANUAL_HINT)
        while not self.auto:
            action = input('option:? ')
            color = MANUAL.get(action.split(), None)
            if color is not None:
                self.color = color
            else:
                print('Wrong action. Do nothing')
                print(MANUAL_HINT)

class TLSmall(TrafficLight):
    pass
