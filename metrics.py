"""Biobjective minimization metrics used in the DPC-MCEA study."""

import math
from statistics import mean


def hv(points, ref=(1.1,1.1)):
    y=ref[1]
    area=0.0
    for a,b in sorted(set(map(tuple,points))):
        if a<=ref[0] and b<y:
            area+=(ref[0]-a)*(y-b)
            y=b
    return area

def igd(points, reference, plus=False):
    if not points or not reference:
        return None
    return mean(min(math.sqrt(sum((max(0,a-b) if plus else a-b)**2
                             for a,b in zip(p,r))) for p in points)
                for r in reference)

if __name__ == "__main__":
    assert math.isclose(hv([(0.2, 0.8), (0.3, 0.7)]), 0.35)
    assert hv([]) == 0
    assert igd([], [(0, 0)], plus=True) is None
    assert igd([(0, 0)], [(0.5, 0.5)], plus=True) == 0
    assert math.isclose(igd([(0, 0)], [(0.5, 0.5)]), math.sqrt(0.5))
    print("PASS: HV, IGD and IGD+ checks")