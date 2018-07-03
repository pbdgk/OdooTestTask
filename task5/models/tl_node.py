import threading
from .traffic_light import TrafficLight


ACTIONS = """
    -i <id>-> info
    -m <id> -> manual mode
    -del <id> -> remove Traffic Light from Node
    -add <start color> -> add Trafic Light to Node
    """



class TLNode:

    def __init__(self):
        self._traffic_lights = {}

    @property
    def traffic_lights(self):
        return self._traffic_lights

    @traffic_lights.setter
    def traffic_lights(self, tls):
        if isinstance(tls, (tuple, list)):
            for tl in tls:
                self._traffic_lights[tl.id] = tl
        elif isinstance(tl, TrafficLight):
            self._traffic_lights[tl.id] = tl
        else:
            raise ValueError("Wrong instance of traffic light")

    def run(self):
        for tl in self._traffic_lights.values():
            t = threading.Thread(target=tl.start)
            t.start()

        self.provision()

    def provision(self):
        print(self._traffic_lights)
        print(ACTIONS)
        while True:
            action = input('-action id:> ')
            if action.startswith('-i'):
                info = self.get_info(action)
                print(info)

            elif action.startswith('-m'):
                self.create_manual_mode(action)

            elif action.startswith('-del'):
                self.remove_tl(action)

            elif action.startswith('-add'):
                self.add_tl(action)

            else:
                print('Wrong action')
                print(self._traffic_lights)
                print(ACTIONS)

    def add_tl(self, action):
        #  TODO: crearte func
        start_color = input('input start color')
        tl = TrafficLight(start_color)
        self._traffic_lights[tl.id] = tl
        t = threading.Thread(target=tl.start)
        t.start()
        print("TL started:> %s" % tl)

    def remove_tl(self, action):
        tl = self.get_tl(action)
        if tl is not None:
            tl.auto = False  # terminates expression for running Thread.
            del self._traffic_lights[tl.id]
            res = 'deleted'
        else:
            res = 'wrong id'
        print(res)

    def create_manual_mode(self, action):
        tl = self.get_tl(action)
        tl.mode = False
        tl.manual_switch()

    def get_tl(self, action):
        id_ = self.parse_id(action)
        if id_ is not None:
            return self.get_tl_by_id(id_)
        else:
            print('Wrong data ')

    def get_info(self, action):
        tl = self.get_tl(action)
        if tl is not None:
            res = tl.info
        else:
            res = "Wrong id"
        return res

    def parse_id(self, action):
        try:
            id_str = action.split()[-1]
            id_ = int(id_str)
            return id_
        except (IndexError, ValueError):
            return None

    def get_tl_by_id(self, id_):
        try:
            return self._traffic_lights[id_]
        except KeyError:
            return None
