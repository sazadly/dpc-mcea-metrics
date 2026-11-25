# DPC-MCEA evaluation and reproducibility materials

## Metrics

Run `python metrics.py` with Python 3.11 or newer. No external packages are needed. Pass feasible objective vectors in minimization form. The study's HV reference point is `(1.1, 1.1)`. Use a common frozen reference front when computing IGD and IGD+ across methods. HV is zero when the approximation set is empty. IGD and IGD+ return `None` if either set is empty.

## Reproduce the reported summaries

Run `python reproduce.py` to check file hashes and reproduce the real-network summary. Run `python reproduce.py hv_time.pdf` to regenerate the time curves with matplotlib installed.

- `results/fixed_FE/RUN_METRICS.csv` contains selected columns from 180 runs at 100320 completed source evaluations. The nominal FE limit was 100000.
- `results/fixed_wall/run_endpoints.csv` contains 600 s and 1200 s endpoints for 30 runs. Each budget has five seed pairs per network. Blank IGD+ values represent undefined measurements.
- `results/fixed_wall/HV_time.csv` contains the recorded HV trajectories. Use the endpoint table for comparisons at each deadline.

These tables contain derived optimization metrics and timing records. They support independent summaries and plot generation. Recomputing metrics from original objective vectors requires the original archives and frozen reference fronts.

## Synthetic network generation

In MATLAB, call `cv_graph('er',80,1234)`, `cv_graph('block',160,1234)` or `cv_graph('hub',80,1234)`. This generator supports dimensions 80 and 160, creates closed-neighborhood coverage matrices, and assigns a reproducible 70% prior-node set. The seed in these examples is illustrative.

The upstream network archives and baseline are available from the [MONCP authors](https://github.com/WilfongGuo/MONCP) under the upstream terms. This release does not contain those archives, third-party code, original genotype records, or a standalone optimizer. End-to-end optimizer reproduction requires the original dependencies and additional experiment materials.
