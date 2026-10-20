"""SUMO Environment for Traffic Signal Control."""

from gymnasium.envs.registration import register


register(
    id="clear-flow-v0",
    entry_point="clear_flow.environment.env:SumoEnvironment",
    kwargs={"single_agent": True},
)
