from models import tl_node
from models import traffic_light


if __name__ == "__main__":
    node = tl_node.TLNode()
    tl1 = traffic_light.TrafficLight(traffic_light.GREEN)
    tl2 = traffic_light.TrafficLight(traffic_light.RED)
    node.traffic_lights = tl1, tl2
    node.run()
