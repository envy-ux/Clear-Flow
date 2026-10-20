"""Train a tabular Q-learning baseline on Clear Flow's synthetic India scenario.

The scenario and vehicle parameters are for simulation development only, not field-calibrated.
"""

import argparse
import os
import sys
from datetime import datetime
from pathlib import Path


if "SUMO_HOME" not in os.environ:
    raise SystemExit("Please set SUMO_HOME to your SUMO installation directory.")
sumo_tools = str(Path(os.environ["SUMO_HOME"]) / "tools")
if sumo_tools not in sys.path:
    sys.path.append(sumo_tools)

from clear_flow import SumoEnvironment
from clear_flow.agents import QLAgent
from clear_flow.exploration import EpsilonGreedy


def parse_args():
    parser = argparse.ArgumentParser(description="Clear Flow mixed-traffic Q-learning baseline")
    parser.add_argument("--seconds", type=int, default=1800, help="Simulation seconds per episode")
    parser.add_argument("--runs", type=int, default=1, help="Number of independent training runs")
    parser.add_argument("--alpha", type=float, default=0.1, help="Q-learning learning rate")
    parser.add_argument("--gamma", type=float, default=0.99, help="Discount factor")
    parser.add_argument("--epsilon", type=float, default=0.1, help="Initial exploration probability")
    parser.add_argument("--min-epsilon", type=float, default=0.01, help="Minimum exploration probability")
    parser.add_argument("--decay", type=float, default=0.995, help="Exploration decay per decision")
    parser.add_argument("--seed", type=int, default=42, help="Base simulation seed")
    parser.add_argument("--gui", action="store_true", help="Show SUMO-GUI")
    parser.add_argument("--sublane", action="store_true", help="Enable SUMO sublane resolution (experimental)")
    return parser.parse_args()


def main():
    args = parse_args()
    output_dir = Path("outputs/india-mixed-traffic")
    output_dir.mkdir(parents=True, exist_ok=True)
    net_file = "clear_flow/nets/single-intersection/single-intersection.net.xml"
    route_file = "clear_flow/nets/india_mixed_traffic/india_mixed_traffic.rou.xml"

    for run in range(args.runs):
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        out_csv = str(output_dir / f"qlearning-{stamp}-run{run + 1}")
        extra_cmd = "--lateral-resolution 0.2" if args.sublane else None
        env = SumoEnvironment(
            net_file=net_file,
            route_file=route_file,
            out_csv_name=out_csv,
            use_gui=args.gui,
            num_seconds=args.seconds,
            reward_fn="clear_flow_mixed_traffic",
            min_green=5,
            max_green=50,
            sumo_seed=args.seed + run,
            additional_sumo_cmd=extra_cmd,
        )
        try:
            initial_states = env.reset()
            agents = {
                ts: QLAgent(
                    starting_state=env.encode(initial_states[ts], ts),
                    state_space=env.observation_space,
                    action_space=env.action_space,
                    alpha=args.alpha,
                    gamma=args.gamma,
                    exploration_strategy=EpsilonGreedy(
                        initial_epsilon=args.epsilon,
                        min_epsilon=args.min_epsilon,
                        decay=args.decay,
                    ),
                )
                for ts in env.ts_ids
            }
            done = {"__all__": False}
            while not done["__all__"]:
                actions = {ts: agents[ts].act() for ts in agents}
                next_states, rewards, done, _ = env.step(actions)
                for ts, agent in agents.items():
                    agent.learn(
                        next_state=env.encode(next_states[ts], ts),
                        reward=rewards[ts],
                    )
            env.save_csv(out_csv, run + 1)
            print(f"Run {run + 1}/{args.runs} complete. Metrics prefix: {out_csv}")
        finally:
            env.close()


if __name__ == "__main__":
    main()
