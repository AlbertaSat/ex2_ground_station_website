from satellite_simulator.sat_sim import Satellite, Environment, Simulator, SatelliteComponent
import json
import time

def minimal_example():

    environment = Environment(connection_strength=10, connection_stability=10,
        packet_drop_probability=0.05)
    satellite = Satellite(components=[])

    simulator = Simulator(environment, satellite)
    del environment, satellite

    data = ('PING', [])
    resp = simulator.send_to_sat(data)
    print(resp)


def example_usage():

    environment = Environment(connection_strength=10, connection_stability=10,
        packet_drop_probability=0)

    volt_effect = lambda old_value, time_delta : old_value - (0.01 * time_delta)
    temp_effect = lambda old_value, time_delta : [el + (0.01 * time_delta) for el in old_value]
    wdog_effect = lambda old_value, time_delta : [el - time_delta for el in old_value]

    satellite_components = [
        SatelliteComponent('GPS', 0,
            effects_when_on=[('battery_voltage', volt_effect), ('temps', temp_effect)],
            effects_when_off=[]),
        SatelliteComponent('WATCHDOG_TIMERS', 1,
            effects_when_on=[('watchdogs', wdog_effect)],
            effects_when_off=[])
    ]
    satellite = Satellite(satellite_components)
    satellite._turn_on_channel(1)
    simulator = Simulator(environment, satellite)
    del environment, satellite

    data_sequence = [
        ('GET-HK', []),
        ('TURN-ON', ['0']),
        ('TURN-ON', ['12']),
        ('GET-HK', []),
        ('TURN-OFF', ['0']),
        ('GET-HK', []),
        ('PET-WATCHDOG', ['0', '5400']),
        ('GET-HK', [])
    ]

    for data in data_sequence:
        print('sending data: ', data)
        resp = simulator.send_to_sat(data)
        try:
            # try/except because not all responses are json serializable
            resp = json.loads(resp)
            resp = json.dumps(resp, indent=4)
        except json.decoder.JSONDecodeError as e:
            pass
        print('sat response:', resp)
        time.sleep(2)

    # doing this so I dont have to keep creating it for each example
    return simulator


def flight_schedule_example():
    # TODO: refer to outdated implementation on older commit for reference
    pass


def run_interactively():
    # TODO: refer to outdated implementation on older commit for reference
    pass


def main():
    example_usage()


if __name__=="__main__":
    main()
