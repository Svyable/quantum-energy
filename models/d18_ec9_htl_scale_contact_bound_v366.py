#!/usr/bin/env python3
"""v3.66 D18/BTP-eC9 HTL scale/contact benchmark. Standard library only."""
from fractions import Fraction
import json
from pathlib import Path

TOL = 1e-12
DATA = Path(__file__).parents[1] / "research/benchmarks/d18-ec9-htl-scale-contact-bound-v3.66.json"


def positive(x, name):
    if x <= 0:
        raise ValueError(f"{name} must be positive")
    return x


def metrics(ped_s, ped_l, beta_s, beta_l):
    for name, x in (("ped_s", ped_s), ("ped_l", ped_l), ("beta_s", beta_s), ("beta_l", beta_l)):
        positive(x, name)
    rp = ped_l / ped_s
    rb = beta_l / beta_s
    return rp, rb, rb-rp, beta_l/ped_l-1


def frac(s):
    return Fraction(str(s))


def main():
    d = json.loads(DATA.read_text())
    i = d["inputs"]
    ps=i["D18_BTP_eC9_PEDOT_small"]["PCE_percent"]
    pl=i["D18_BTP_eC9_PEDOT_large"]["PCE_percent"]
    bs=i["D18_BTP_eC9_betaP_small"]["PCE_percent"]
    bl=i["D18_BTP_eC9_betaP_large"]["PCE_percent"]
    rp,rb,adv,gain=metrics(ps,pl,bs,bl)
    exact=(frac(pl)/frac(ps), frac(bl)/frac(bs), frac(bl)/frac(bs)-frac(pl)/frac(ps), frac(bl)/frac(pl)-1)
    for a,b in zip((rp,rb,adv,gain), exact):
        assert abs(a-float(b)) <= TOL
    exp=d["expected"]
    assert abs(rp-exp["PEDOT_scale_retention"]) <= TOL
    assert abs(rb-exp["betaP_scale_retention"]) <= TOL
    assert abs(adv-exp["retention_advantage_absolute"]) <= TOL
    assert abs(gain-exp["large_area_betaP_relative_PCE_gain"]) <= TOL
    ff=i["D18_BTP_eC9_betaP_large"]["FF_percent"]-i["D18_BTP_eC9_PEDOT_large"]["FF_percent"]
    voc=i["D18_BTP_eC9_betaP_large"]["Voc_V"]-i["D18_BTP_eC9_PEDOT_large"]["Voc_V"]
    jgain=i["D18_BTP_eC9_betaP_large"]["Jsc_mA_cm2"]/i["D18_BTP_eC9_PEDOT_large"]["Jsc_mA_cm2"]-1
    assert abs(ff-exp["large_area_FF_gain_percentage_points"]) <= TOL
    assert abs(voc-exp["large_area_Voc_gain_V"]) <= TOL
    assert abs(jgain-exp["large_area_Jsc_relative_gain"]) <= TOL
    # Limiting case: no scale penalty.
    assert metrics(10,10,10,10) == (1,1,0,0)
    # Negative/control case: a worse alternate HTL must remain worse, not be clamped.
    _,_,adv_bad,gain_bad=metrics(10,8,10,7)
    assert adv_bad < 0 and gain_bad < 0
    # Invalid physical domain fails closed.
    try:
        metrics(10,0,10,10)
        raise AssertionError("non-positive PCE accepted")
    except ValueError:
        pass
    print(f"PEDOT scale retention: {rp:.6f}; beta-P: {rb:.6f}; advantage: {adv*100:.3f} pp")
    print(f"1 cm^2 beta-P relative PCE gain: {gain*100:.3f}%; FF gain: {ff:.2f} pp; Voc gain: {voc*1000:.1f} mV")
    print("PASS: exact arithmetic, fixtures, and fail-closed checks")

if __name__ == "__main__":
    main()
