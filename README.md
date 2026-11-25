# DPC-MCEA evaluation metrics

Python implementations of two-dimensional hypervolume (HV), IGD and IGD+ used in the DPC-MCEA study. This release contains the metric functions extracted from the archived analysis script and a synthetic self-check.

Run `python metrics.py` with Python 3.11 or newer. No packages are required.

Pass feasible objective vectors in minimization form. The study's HV reference point is `(1.1, 1.1)`. For IGD and IGD+, supply the same frozen empirical reference front for each compared method. HV is zero for an empty approximation set. IGD and IGD+ return `None` if either set is empty.

The optimizer, comparison implementations, input networks, reference fronts and run records are outside this release. The upstream MONCP materials are maintained by the [original authors](https://github.com/WilfongGuo/MONCP). This release supports metric verification with supplied objective vectors. End-to-end reproduction requires the study inputs and experiment implementation.
