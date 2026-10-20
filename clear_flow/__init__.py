"""Clear Flow: reinforcement-learning environments for traffic-signal optimization."""

from clear_flow.environment.env import (
    ObservationFunction,
    SumoEnvironment,
    TrafficSignal,
    env,
    parallel_env,
)
from clear_flow.environment.resco_envs import (
    arterial4x4,
    cologne1,
    cologne3,
    cologne8,
    grid4x4,
    ingolstadt1,
    ingolstadt7,
    ingolstadt21,
)


__version__ = "0.1.0"
__upstream_version__ = "1.4.5"

# Register Clear Flow-specific reward functions on package import.
from clear_flow.rewards import clear_flow_mixed_traffic
