import random
import time


def calculate_semi_random_latency(connection_strength, connection_stability, min_delay=0):
    """returns a latency value depending on the conn. strength and conn. stability
    params:
        - connection_strength (int) : value between [1, 10], where 1 is worst connection, 10 is best
        - connection_stability (int) : determins how much variance there is in samples
        - min_delay (float) : if you want a guarunteed minimum of delay, you should set this to a >= 0 value
    """
    # decrease for lower latency
    numerator = 5

    latency_mean = numerator/connection_strength
    deviation = (1/connection_stability)
    random_latency = max(min_delay, random.normalvariate(latency_mean, deviation))
    return random_latency

def get_unix_time():
    return int(time.time())
