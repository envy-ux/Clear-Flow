# Contributing to Clear Flow

Thanks for considering a contribution. Clear Flow is an early-stage research and engineering project for reinforcement-learning traffic-signal control in heterogeneous traffic.

## Before opening a change

1. Search the issue tracker for related work, or open an issue to discuss a substantial design change.
2. Keep changes focused and explain the motivation, assumptions, and expected impact.
3. Preserve notices and license files for inherited code, benchmark networks, and datasets. Some bundled benchmark assets have terms different from the root MIT license; see `UPSTREAM_NOTICES.md` and the notices beside those assets.
4. Do not include API keys, personal data, private traffic-camera footage, or sensitive infrastructure data.

## Development setup

Install a supported Python version and SUMO separately, then set `SUMO_HOME` so it points to your SUMO installation. From the repository root:

```bash
python -m venv .venv
python -m pip install --upgrade pip
python -m pip install -e .[testing]
```

On Windows PowerShell, activate the environment with:

```powershell
.\.venv\Scripts\Activate.ps1
```

## Tests

Set `SUMO_HOME` before importing Clear Flow, then run:

```bash
python -m pytest tests/
```

The integration tests start SUMO simulations and therefore need the SUMO executable and tools installed. When changing RL rewards or policies, include repeatable scenarios and report the seeds and metrics used. Prefer comparisons against a fixed-time baseline and report trade-offs across vehicle classes, not just a single aggregate score.

## Pull requests

- Explain what changed and why.
- Link related issues when applicable.
- Add tests and update documentation where behavior changes.
- Identify any new assumptions, limitations, data sources, and license constraints.
- Do not claim real-world traffic improvements from synthetic simulation alone.
