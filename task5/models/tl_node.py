import threading

ACTIONS = """
    -i <id>-> info
    -m <id> -> manual mode
    -del <TrafficLight> -> remove Traffic Light to System
    -add <TrafficLight> -> add Trafic Light to System
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
            else:
                print('Wrong action')
                print(ACTIONS)

    def get_info(self, action):
        id_ = self.parse_id(action)
        if id_ is not None:
            tl = self.get_tl_by_id(id_)
            if tl is not None:
                return tl.info
            else:
                print('Wrong id')
        else:
            print('Wrong data ')

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
