"""Clear Flow reward functions for heterogeneous-traffic signal control.

The reward below is a research baseline, not a validated traffic-engineering policy.
It combines class-weighted waiting, normalized incoming queues and downstream occupancy.
"""
from __future__ import annotations

from typing import Any

from clear_flow.environment.traffic_signal import TrafficSignal


# Illustrative priorities: buses receive extra weight because they can carry many
# passengers; other classes remain represented so the policy is not car-only.
VEHICLE_WAIT_WEIGHTS = {
    "two_wheeler": 1.0,
    "auto_rickshaw": 1.15,
    "car": 1.0,
    "bus": 1.5,
    "truck": 1.15,
}


def _wait_weight(vehicle_type: str) -> float:
    """Return a reward weight for a scenario vehicle type."""
    for prefix, weight in VEHICLE_WAIT_WEIGHTS.items():
        if vehicle_type.startswith(prefix):
            return weight
    return 1.0


def clear_flow_mixed_traffic(signal: Any) -> float:
    """Reward improvements in class-weighted delay, queues, and downstream clearance.

    The returned value is the reduction in a local congestion cost since the
    previous decision. Queue values and downstream densities are normalized by
    the inherited simulator interface. Accumulated waiting is capped to reduce
    sensitivity to extreme outliers. Weights are editable experiment parameters,
    not official priorities or calibrated parameters.
    """
    weighted_wait = 0.0
    total_weight = 0.0

    for lane_id in signal.lanes:
        for vehicle_id in signal.sumo.lane.getLastStepVehicleIDs(lane_id):
            vehicle_type = signal.sumo.vehicle.getTypeID(vehicle_id)
            weight = _wait_weight(vehicle_type)
            wait_seconds = min(
                float(signal.sumo.vehicle.getAccumulatedWaitingTime(vehicle_id)),
                300.0,
            )
            weighted_wait += weight * (wait_seconds / 60.0)
            total_weight += weight

    class_weighted_delay = weighted_wait / total_weight if total_weight else 0.0

    incoming_queue = signal.get_lanes_queue()
    mean_queue = sum(incoming_queue) / len(incoming_queue) if incoming_queue else 0.0
    worst_queue = max(incoming_queue, default=0.0)

    downstream_density = signal.get_out_lanes_density()
    downstream_blockage = max(downstream_density, default=0.0)

    # Costs are deliberately transparent so experiments can tune/ablate terms.
    cost = (
        class_weighted_delay
        + 1.8 * mean_queue
        + 2.5 * (worst_queue**2)
        + 1.5 * (downstream_blockage**2)
    )

    previous_cost = getattr(signal, "_clear_flow_previous_cost", cost)
    signal._clear_flow_previous_cost = cost
    return float(previous_cost - cost)


# Register the custom reward with the inherited environment's string-based API.
TrafficSignal.register_reward_fn(clear_flow_mixed_traffic)
