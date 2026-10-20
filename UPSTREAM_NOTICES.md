# Upstream and third-party notices

## Clear Flow base framework

Clear Flow v0.1.0 is a modified derivative of **SUMO-RL**, originally published at <https://github.com/LucasAlegre/sumo-rl>. The inherited code is distributed under the MIT License. The original `LICENSE` file and copyright notice are preserved in this repository:

> Copyright (c) 2018 Lucas Alegre

The Clear Flow adaptation changes the project/package branding, moves the Python package namespace to `clear_flow`, updates project documentation and packaging, and adds an illustrative mixed-vehicle scenario plus a Q-learning demo. It should not be read as a claim that the inherited simulator or baseline algorithms were originally authored for Clear Flow. The upstream bibliographic entry is preserved in [`UPSTREAM_CITATION.bib`](UPSTREAM_CITATION.bib).

## Other components and datasets

- **SUMO** is a separate traffic simulator; it must be installed separately and retains its own license and terms.
- **RESCO benchmark assets** are distributed with separate license files and/or license documents under `clear_flow/nets/RESCO/`. These terms may differ from the MIT license for the inherited framework. In particular, check the included Creative Commons notices before copying or modifying benchmark assets or using them commercially.
- Python dependencies (Gymnasium, PettingZoo, NumPy, pandas, TraCI, and others) retain their own licenses.

The MIT license covers the Clear Flow code and inherited code distributed under MIT; it does not override third-party license terms that accompany bundled benchmark networks, maps, or datasets. Review the nearby license files before redistributing or using those assets, especially for commercial purposes.

Keep this notice, the `LICENSE`, and the relevant dataset/license files when redistributing this project.
