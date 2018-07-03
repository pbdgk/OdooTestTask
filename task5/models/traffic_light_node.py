import threading
from .traffic_light import TrafficLight


ACTIONS = """
    -i <id>-> info
    -m <id> -> manual mode
    -del <id> -> remove Traffic Light from Node
    -add -> add Trafic Light to Node
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

    def restart_tl(self, tl):
        t = threading.Thread(target=tl.start)
        t.start()

    def provision(self):
        print(self._traffic_lights)
        print(ACTIONS)
        while True:
            action = input('-action id:> ')
            if action.startswith('-i'):
                info = self.get_info(action)
                print(info)

            elif action.startswith('-m'):
                self.manual_mode(action)

            elif action.startswith('-del'):
                self.remove_tl(action)

            elif action.startswith('-add'):
                self.add_tl(action)

            else:
                print('Wrong action')
                print(self._traffic_lights)
                print(ACTIONS)

    def add_tl(self, action):
        #  TODO: create func
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
            message = 'deleted'
        else:
           message = 'wrong id'
        print(message)

    def manual_mode(self, action):
        tl = self.get_tl(action)
        if tl is not None:
            tl.auto = False
            tl.manual_switch()
            self.restart_tl(tl)
        else:
            print('error')

    def get_tl(self, action):
        id_ = self.parse_id(action)
        if id_ is not None:
            return self.get_tl_by_id(id_)
        else:
            print('Wrong data ')

    def get_info(self, action):
        tl = self.get_tl(action)
        if tl is not None:
            message = tl.info
        else:
            message = "Wrong id"
        return message

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
