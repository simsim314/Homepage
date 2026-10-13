#!/usr/bin/env python3
"""Conservative sampled collision check for separator registration patterns.

Each Life/blue width L is 120 raster units. Search all 120x120 translations
for horizontal and vertical orange bodies. This is NOT a continuous-angle or
manufacturing-tolerance proof. It does not check final B/W connector geometry.

To cover all binary values conservatively, retain only the common material
of 0/+ data studs, and enlarge every input recess to the UNION of both shapes.
If even this more permissive model collides, every actual data assignment does.
"""
from pathlib import Path
import json
import numpy as np

P=120
Y,X=np.mgrid[0:P,0:P]+.5


def delta(cx,cy):
    return (X-cx+P/2)%P-P/2,(Y-cy+P/2)%P-P/2


def shape(cx,cy,kind,radius=5.2,width=1.8):
    x,y=delta(cx,cy)
    if kind=='0':return (x*x+y*y<=radius**2)&(x*x+y*y>=3.4**2)
    if kind=='X':x,y=(x+y)/2**.5,(x-y)/2**.5
    return ((abs(x)<width/2)&(abs(y)<radius))|((abs(y)<width/2)&(abs(x)<radius))


def blockers(name):
    result=np.zeros((P,P),bool)
    for cy in (12,36,60,84,108):
        for cx in (12,36,60,84,108):
            if cx!=60 and cy!=60:continue
            if name=='one_big_X':result|=shape(cx,cy,'X',9,2)
            elif name=='four_small_Xs':
                for dx in (-6,6):
                    for dy in (-6,6):result|=shape(cx+dx,cy+dy,'X',4,1.5)
            elif name=='four_rotated_Ls':
                u,v=delta(cx,cy)
                # Rotate both a corner location and its L profile together.
                for _ in range(4):
                    a,b=u+6,v+6
                    result|=((abs(a+2.5)<.75)&(abs(b)<3.25))|((abs(b+2.5)<.75)&(abs(a)<3.25))
                    u,v=-v,u
    assert np.array_equal(result,np.rot90(result)),name
    return result


def main():
    mandatory=np.zeros((P,P),bool)
    for cy in (12,36,84,108):
        for cx in (12,36,84,108):mandatory|=shape(cx,cy,'0')&shape(cx,cy,'+')
    forbidden=(X<96)&(Y<24)
    for cx in (12,36,60,84):forbidden&=~(shape(cx,12,'0')|shape(cx,12,'+'))
    reports={}
    for name in ('empty','one_big_X','four_small_Xs','four_rotated_Ls'):
        occupied=mandatory|blockers(name)
        reports[name]={}
        for orientation,mask in (('horizontal',forbidden),('vertical',forbidden.T)):
            corr=np.fft.ifft2(np.fft.fft2(occupied)*np.conj(np.fft.fft2(mask))).real
            yy,xx=np.where(corr<.5)
            candidates=set(zip(xx.tolist(),yy.tolist()))
            expected={(72,y) for y in (0,24,72,96)}
            if orientation=='vertical':expected={(y,x) for x,y in expected}
            assert expected<=candidates
            reports[name][orientation]={'surviving_translations':len(candidates),
                 'intended_translations':len(expected),'extra_candidates':len(candidates-expected)}
            if name!='empty':assert candidates==expected,(name,orientation)
    report={'period_samples':P,'translation_step_over_L':1/P,
        'tested_axis_directions':['horizontal','vertical'],
        'patterns':reports,
        'big_X_half_arm_length_over_L':9/P,'big_X_bar_width_over_L':2/P,
        'scope':'Conservative raster test across all binary values. Axis-aligned translations only. No arbitrary-angle, tolerance, or final C/BW alignment proof.'}
    out=Path(__file__).parent/'blue-schematics'/'separator-pattern-check.json'
    out.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__=='__main__':main()
