"""Read-only reproduction of main real-network tables and HV plot."""
from collections import defaultdict
import csv
import hashlib
import json
import math
from pathlib import Path
from statistics import mean
import sys

BASE=Path(__file__).resolve().parent
CASES=('BRCA_37','LUSC_16','LUAD_68')
def read(name):
    with (BASE/name).open(encoding='utf-8-sig',newline='') as f:
        return list(csv.DictReader(f))

from metrics import hv, igd

def verify():
    pin=json.loads((BASE/'SHA256.json').read_text(encoding='utf-8'))
    for name, digest in pin.items():
        with (BASE/name).open('rb') as f:
            assert hashlib.file_digest(f,'sha256').hexdigest()==digest, name
    assert hv([(0.2,0.8),(0.3,0.7)]) == hv([(0.3,0.7),(0.2,0.8),(0.4,0.9)])
    assert hv([])==0 and igd([],[(0,0)],plus=True) is None
    assert igd([(0,0)],[(.5,.5)],plus=True)==0
    assert math.isclose(igd([(0,0)],[(.5,.5)]),math.sqrt(.5))
    fixed=read('results/fixed_FE/RUN_METRICS.csv')
    wall=read('results/fixed_wall/run_endpoints.csv')
    assert len(fixed)==180 and len(wall)==60
    assert all(int(float(x['actual_source_FE']))==100320 for x in fixed)
    assert all(x['status']=='valid' and x['cap_reached'].lower() in {'0','false'} for x in wall)
    print('Network | HV gain FE % | IGD reduction % | IGD+ reduction % | time ratio | 1200s HV (D/O) | timely FE (D/O)')
    for g in CASES:
        a,b=[[mean(float(r[m]) for r in fixed if r['graph_id']==g and r['variant']==arm)
              for m in ('HV','IGD','IGD_plus','macro_plus_deferred_seconds')]
             for arm in ('DPC','O_CORR')]
        p=[(a[0]/b[0]-1)*100,(1-a[1]/b[1])*100,(1-a[2]/b[2])*100,a[3]/b[3]]
        q=[[mean(float(r[m]) for r in wall if r['graph']==g and r['arm']==arm and r['budget']=='1200')
            for m in ('HV','timely_FE','feasible_main')] for arm in ('DPC','O_CORR')]
        assert q[0][2]==300 and q[1][2]==0
        print(f'{g} | {p[0]:.2f} | {p[1]:.3f} | {p[2]:.3f} | {p[3]:.3f} | {q[0][0]:.6f}/{q[1][0]:.0f} | {q[0][1]:.0f}/{q[1][1]:.0f}')
    print('PASS: checksums, job counts, budgets and numerical summary.')

def plot(path):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    trajectories=defaultdict(list)
    for r in read('results/fixed_wall/HV_time.csv'):
        trajectories[r['graph'],r['arm'],r['seed']].append((float(r['seconds']),float(r['HV'])))
    fig, axes=plt.subplots(1,3,figsize=(11,3.5),sharey=True)
    for g,ax in zip(CASES,axes):
        seen=set()
        for (case,arm,seed),xy in trajectories.items():
            if case!=g:
                continue
            x,y=zip(*sorted(xy))
            ax.step(x,y,where='post',color={'DPC':'#2166AC','O_CORR':'#B2182B'}[arm],
                    alpha=.65,label=arm if arm not in seen else None)
            seen.add(arm)
        for budget in (600,1200):
            ax.axvline(budget,ls=':',color='.45',lw=.7)
        ax.set(xlabel='Elapsed wall time (s)', title=g, xlim=(0,1220))
    axes[0].set_ylabel('Feasible-set hypervolume')
    handles,labels=axes[0].get_legend_handles_labels()
    fig.legend(handles,labels,loc='upper center',frameon=False,ncol=2)
    fig.tight_layout(rect=(0,0,1,.88))
    fig.savefig(path)

if __name__=='__main__':
    verify()
    if len(sys.argv)>1:
        plot(sys.argv[1])
