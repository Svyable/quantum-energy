#!/usr/bin/env python3
"""R2 Voc-vs-light-intensity grid and measurement-power study (v3.15).

All power values are planning calculations under explicit Gaussian point-noise
assumptions. They are not measured R2 performance and do not establish a
recombination mechanism.
"""
from __future__ import annotations

import csv
import math
import random
import sys

K_B_EV_PER_K = 8.617333262e-5
T_K = 300.0
PHI_MIN = 0.05
PHI_MAX = 2.0
PRIMARY_N = 17
PRIMARY_WINDOW = 7
SENSITIVITY_WINDOW = 9
LOW_TARGET = 0.1
HIGH_TARGET = 1.0
ALPHA = 0.05
Z_CRIT = 1.959963984540054
SEED = 20260826
MC_REPS = 30000
AREA_CM2 = 0.0961
ONE_SUN_MW_CM2 = 100.0
PLANNING_SECONDS_PER_POINT = 5.0  # dose illustration only, not a thermal model


def solve3(a: list[list[float]], b: list[float]) -> list[float]:
    m = [row[:] + [rhs] for row, rhs in zip(a, b)]
    for col in range(3):
        pivot = max(range(col, 3), key=lambda r: abs(m[r][col]))
        m[col], m[pivot] = m[pivot], m[col]
        if abs(m[col][col]) < 1e-18:
            raise RuntimeError("singular 3x3 system")
        scale = m[col][col]
        for j in range(col, 4):
            m[col][j] /= scale
        for r in range(3):
            if r == col:
                continue
            factor = m[r][col]
            for j in range(col, 4):
                m[r][j] -= factor * m[col][j]
    return [m[i][3] for i in range(3)]


def geom_grid(n: int) -> list[float]:
    ratio = (PHI_MAX / PHI_MIN) ** (1.0 / (n - 1))
    return [PHI_MIN * ratio**i for i in range(n)]


def nearest_index(values: list[float], target: float) -> int:
    return min(range(len(values)), key=lambda i: abs(values[i] - target))


def local_nid_weights(phi: list[float], idx: int, window: int) -> list[float]:
    if window < 3 or window % 2 == 0 or window > len(phi):
        raise ValueError("window must be odd, >=3, <= grid size")
    x = [math.log(v) for v in phi]
    half = window // 2
    lo = max(0, min(idx - half, len(phi) - window))
    hi = lo + window
    u = [x[j] - x[idx] for j in range(lo, hi)]
    sums = [sum(v**k for v in u) for k in range(5)]
    normal = [
        [sums[0], sums[1], sums[2]],
        [sums[1], sums[2], sums[3]],
        [sums[2], sums[3], sums[4]],
    ]
    thermal_v = K_B_EV_PER_K * T_K
    weights = [0.0] * len(phi)
    # A regression coefficient is linear in y. Apply the 3x3 solver to each
    # unit-vector response to obtain independent explicit slope weights.
    for local_col, global_col in enumerate(range(lo, hi)):
        rhs = [u[local_col] ** k for k in range(3)]
        beta = solve3(normal, rhs)
        weights[global_col] = beta[1] / thermal_v
    return weights


def contrast_weights(n: int, window: int) -> tuple[list[float], list[float], int, int]:
    phi = geom_grid(n)
    low = nearest_index(phi, LOW_TARGET)
    high = nearest_index(phi, HIGH_TARGET)
    w_low = local_nid_weights(phi, low, window)
    w_high = local_nid_weights(phi, high, window)
    return phi, [b - a for a, b in zip(w_low, w_high)], low, high


def normal_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def two_sided_power(effect: float, se: float) -> float:
    mu = abs(effect) / se
    return normal_cdf(-Z_CRIT - mu) + 1.0 - normal_cdf(Z_CRIT - mu)


def contrast_se(n: int, window: int, sigma_point_mv: float) -> float:
    _phi, w, _lo, _hi = contrast_weights(n, window)
    return math.sqrt(sum(v*v for v in w)) * sigma_point_mv / 1000.0


def mc_power(n: int, window: int, sigma_point_mv: float, effect: float, reps: int = MC_REPS) -> tuple[float, float]:
    phi, w, _lo, _hi = contrast_weights(n, window)
    # A linear n_id trend integrates to a quadratic Voc(ln phi); the local
    # quadratic estimator therefore recovers the injected contrast exactly
    # in the noiseless limiting case.
    x = [math.log(v) for v in phi]
    x_low = math.log(phi[nearest_index(phi, LOW_TARGET)])
    x_high = math.log(phi[nearest_index(phi, HIGH_TARGET)])
    beta = effect / (x_high - x_low)  # dn_id/dln(phi)
    n0 = 1.0
    voc = [K_B_EV_PER_K*T_K*(n0*xx + 0.5*beta*xx*xx) for xx in x]
    true_contrast = sum(ww*yy for ww, yy in zip(w, voc))
    if abs(true_contrast - effect) > 1e-10:
        raise AssertionError((true_contrast, effect))
    se = contrast_se(n, window, sigma_point_mv)
    rng = random.Random(SEED + 100*n + window + int(100*sigma_point_mv) + int(1000*effect))
    hits = 0
    null_hits = 0
    for _ in range(reps):
        noise = [rng.gauss(0.0, sigma_point_mv/1000.0) for _ in phi]
        est = effect + sum(ww*ee for ww, ee in zip(w, noise))
        if abs(est / se) > Z_CRIT:
            hits += 1
        noise0 = [rng.gauss(0.0, sigma_point_mv/1000.0) for _ in phi]
        est0 = sum(ww*ee for ww, ee in zip(w, noise0))
        if abs(est0 / se) > Z_CRIT:
            null_hits += 1
    return hits/reps, null_hits/reps


def main() -> int:
    rows: list[list[object]] = []
    for n in (13, 15, 17, 19):
        phi = geom_grid(n)
        ratio = phi[1]/phi[0]
        se = contrast_se(n, PRIMARY_WINDOW, 0.5)
        power = two_sided_power(0.10, se)
        incident_mj = (
            ONE_SUN_MW_CM2 * AREA_CM2 * sum(phi) * PLANNING_SECONDS_PER_POINT
        )
        rows.append(["grid", n, "ratio", ratio, "planning", "dimensionless"])
        rows.append(["grid", n, "local7_support_factor", ratio**6, "planning", "x intensity"])
        rows.append(["grid", n, "se_delta_n_sigma0p5mV", se, "synthetic", "dimensionless"])
        rows.append(["grid", n, "power_effect0p10_sigma0p5mV", power, "synthetic", "probability"])
        rows.append(["grid", n, "incident_energy_5s_each_mJ", incident_mj, "planning", "mJ"])

    for sigma in (0.25, 0.5, 1.0, 2.0):
        for window in (PRIMARY_WINDOW, SENSITIVITY_WINDOW):
            se = contrast_se(PRIMARY_N, window, sigma)
            for effect in (0.05, 0.10, 0.15):
                rows.append([
                    "point_noise_power", sigma, f"window{window}_effect{effect:.2f}",
                    two_sided_power(effect, se), "synthetic", "probability"
                ])

    se_meas = contrast_se(PRIMARY_N, PRIMARY_WINDOW, 0.5)
    for sigma_between in (0.0, 0.025, 0.05, 0.075, 0.10):
        for n_substrates in (5, 7, 9, 12):
            se_mean = math.sqrt(sigma_between**2 + se_meas**2) / math.sqrt(float(n_substrates))
            for effect in (0.05, 0.10, 0.15):
                rows.append([
                    "substrate_sensitivity",
                    f"sd{sigma_between:.3f}_n{n_substrates}",
                    f"effect{effect:.2f}",
                    two_sided_power(effect, se_mean),
                    "synthetic",
                    "probability",
                ])

    analytic = two_sided_power(0.10, contrast_se(17, 7, 0.5))
    mc, null_fp = mc_power(17, 7, 0.5, 0.10)
    if abs(analytic - mc) > 0.015:
        raise AssertionError(f"analytic/MC power mismatch: {analytic} vs {mc}")
    if not (0.035 <= null_fp <= 0.065):
        raise AssertionError(f"null false-positive rate out of range: {null_fp}")
    if analytic < 0.95:
        raise AssertionError(f"17-point nominal power below gate: {analytic}")

    phi = geom_grid(PRIMARY_N)
    i_low, i_high = nearest_index(phi, LOW_TARGET), nearest_index(phi, HIGH_TARGET)
    max_incident_mw = ONE_SUN_MW_CM2 * AREA_CM2 * max(phi)
    sweep_incident_mj = ONE_SUN_MW_CM2 * AREA_CM2 * sum(phi) * PLANNING_SECONDS_PER_POINT

    print(f"primary_points={PRIMARY_N}")
    print(f"grid_ratio={phi[1]/phi[0]:.9f}")
    print(f"low_anchor={phi[i_low]:.9f} high_anchor={phi[i_high]:.9f}")
    print(f"local7_support_factor={(phi[1]/phi[0])**6:.9f}")
    print(f"nominal_sigma_point_mV=0.5")
    print(f"analytic_power_effect0p10={analytic:.9f}")
    print(f"mc_power_effect0p10={mc:.9f}")
    print(f"mc_null_false_positive={null_fp:.9f}")
    print(f"max_incident_power_mW={max_incident_mw:.6f}")
    print(f"illustrative_5s_each_incident_energy_mJ={sweep_incident_mj:.6f}")
    print("PASS")

    if len(sys.argv) > 1:
        with open(sys.argv[1], "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["section", "condition", "metric", "value", "class", "unit"])
            writer.writerows(rows)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
