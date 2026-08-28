#!/usr/bin/env python3
import json, math, pathlib, sys

HERE = pathlib.Path(__file__).resolve().parent
DATA = HERE.parent / 'research' / 'benchmarks' / 'pto2-y1-field-generation-v3.55.json'
TOL = 1e-12


def slope(eta, beta):
    if not (0 < eta <= 1):
        raise ValueError('eta_int must be in (0,1]')
    if beta < 0:
        raise ValueError('beta must be non-negative')
    return (1.0 / eta - 1.0) * beta


def ratio(eta, beta, delta_v):
    return 1.0 + slope(eta, beta) * abs(delta_v)


def independent_ratio(eta, beta, delta_v):
    # Algebraically independent presentation: eta(V)/eta(Voc)
    # = [eta + (1-eta) beta |dV|] / eta.
    return (eta + (1.0 - eta) * beta * abs(delta_v)) / eta


def main():
    d = json.loads(DATA.read_text())
    eta = d['inputs']['eta_int']['value']
    beta = d['inputs']['beta']['value']
    s = slope(eta, beta)
    r = ratio(eta, beta, 0.5)
    ri = independent_ratio(eta, beta, 0.5)
    assert math.isclose(s, d['expected']['slope_per_V'], rel_tol=0, abs_tol=TOL)
    assert math.isclose(r, d['expected']['ratio_at_abs_deltaV_0p5V'], rel_tol=0, abs_tol=TOL)
    assert math.isclose(r, ri, rel_tol=0, abs_tol=TOL)
    assert ratio(eta, beta, 0.0) == 1.0
    assert slope(1.0, beta) == 0.0
    assert ratio(eta, 0.0, 0.5) == 1.0
    assert ratio(eta, beta, -0.5) == r

    elo, ehi = d['reporting_resolution_sensitivity']['eta_int_range']
    blo, bhi = d['reporting_resolution_sensitivity']['beta_V^-1_range']
    vals = [slope(e, b) for e in (elo, ehi) for b in (blo, bhi)]
    lo, hi = min(vals), max(vals)
    exp_lo, exp_hi = d['reporting_resolution_sensitivity']['slope_per_V_range']
    assert math.isclose(lo, exp_lo, rel_tol=0, abs_tol=TOL)
    assert math.isclose(hi, exp_hi, rel_tol=0, abs_tol=TOL)

    print(json.dumps({
        'slope_per_V': s,
        'ratio_at_abs_deltaV_0p5V': r,
        'reporting_resolution_slope_range_per_V': [lo, hi],
        'checks': 'PASS'
    }, indent=2))


if __name__ == '__main__':
    main()
