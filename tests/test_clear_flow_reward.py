"""Unit tests for the Clear Flow mixed-traffic reward."""

from types import SimpleNamespace

from clear_flow.rewards import clear_flow_mixed_traffic


class FakeTrafficSignal:
    def __init__(self):
        self.lanes = ["north_in", "west_in"]
        self.waiting = {"bus_1": 120.0, "car_1": 60.0, "bike_1": 30.0}
        self.types = {"bus_1": "bus", "car_1": "car", "bike_1": "two_wheeler"}
        self.queues = [0.7, 0.4]
        self.downstream = [0.3, 0.2]
        self.sumo = SimpleNamespace(
            lane=SimpleNamespace(
                getLastStepVehicleIDs=lambda lane: {"north_in": ["bus_1", "bike_1"], "west_in": ["car_1"]}[lane]
            ),
            vehicle=SimpleNamespace(
                getTypeID=lambda vehicle_id: self.types[vehicle_id],
                getAccumulatedWaitingTime=lambda vehicle_id: self.waiting[vehicle_id],
            ),
        )

    def get_lanes_queue(self):
        return self.queues

    def get_out_lanes_density(self):
        return self.downstream


def test_reward_is_neutral_on_first_observation():
    signal = FakeTrafficSignal()
    assert clear_flow_mixed_traffic(signal) == 0.0


def test_reward_improves_when_waiting_and_queues_fall():
    signal = FakeTrafficSignal()
    clear_flow_mixed_traffic(signal)
    signal.waiting = {"bus_1": 20.0, "car_1": 15.0, "bike_1": 10.0}
    signal.queues = [0.2, 0.1]
    signal.downstream = [0.1, 0.1]
    assert clear_flow_mixed_traffic(signal) > 0.0


def test_reward_penalizes_a_congestion_regression():
    signal = FakeTrafficSignal()
    clear_flow_mixed_traffic(signal)
    signal.waiting = {"bus_1": 250.0, "car_1": 200.0, "bike_1": 180.0}
    signal.queues = [0.95, 0.85]
    signal.downstream = [0.9, 0.8]
    assert clear_flow_mixed_traffic(signal) < 0.0
