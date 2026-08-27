#!/usr/bin/env python3
"""R2 illumination-calibration and sweep-history qualification (v3.16).

All numerical stresses in this file are synthetic/planning calculations. They
quantify how intensity-axis errors and temperature normalization can perturb the
frozen v3.15 local-ideality curvature estimator; they are not measured R2 data.
"""
from __future__ import annotations
import csv, math, sys

K_B_EV_PER_K = 8.617333262e-5
T_K = 300.0
N = 17
PHI_MIN, PHI_MAX = 0.05, 2.0
WINDOW = 7
LOW_TARGET, HIGH_TARGET = 0.1, 1.0
TRUE_CONTRAST = 0.10
CAL_NONLINEARITY_STRESS = 0.005  # ±0.5% log-axis residual envelope, synthetic
COMMON_SCALE_STRESS = 0.02       # +2% common intensity scale, synthetic
LOG_GAIN_STRESS = 0.005          # +0.5% log-axis gain, synthetic
TEMP_ERROR_K = 0.5               # normalization sensitivity only


def solve3(a, b):
    m = [row[:] + [rhs] for row, rhs in zip(a, b)]
    for col in range(3):
        p = max(range(col, 3), key=lambda r: abs(m[r][col]))
        m[col], m[p] = m[p], m[col]
        s = m[col][col]
        if abs(s) < 1e-18:
            raise RuntimeError("singular 3x3 system")
        for j in range(col, 4): m[col][j] /= s
        for r in range(3):
            if r == col: continue
            f = m[r][col]
            for j in range(col, 4): m[r][j] -= f * m[col][j]
    return [m[i][3] for i in range(3)]


def grid():
    r = (PHI_MAX / PHI_MIN) ** (1.0 / (N - 1))
    return [PHI_MIN * r**i for i in range(N)]


def nearest(values, target):
    return min(range(len(values)), key=lambda i: abs(values[i] - target))


def local_nid(x, y, idx, window=WINDOW):
    half = window // 2
    lo = max(0, min(idx - half, len(x) - window)); hi = lo + window
    u = [x[j] - x[idx] for j in range(lo, hi)]
    yy = y[lo:hi]
    sums = [sum(v**k for v in u) for k in range(5)]
    rhs = [sum(val * v**k for val, v in zip(yy, u)) for k in range(3)]
    A = [[sums[0], sums[1], sums[2]],
         [sums[1], sums[2], sums[3]],
         [sums[2], sums[3], sums[4]]]
    return solve3(A, rhs)[1] / (K_B_EV_PER_K * T_K)


def contrast(x_used, voc, phi):
    il, ih = nearest(phi, LOW_TARGET), nearest(phi, HIGH_TARGET)
    return local_nid(x_used, voc, ih) - local_nid(x_used, voc, il)


def main():
    phi = grid(); x = [math.log(v) for v in phi]
    il, ih = nearest(phi, LOW_TARGET), nearest(phi, HIGH_TARGET)
    beta = TRUE_CONTRAST / (x[ih] - x[il])
    voc = [(K_B_EV_PER_K*T_K) * (1.0*xx + 0.5*beta*xx*xx) for xx in x]
    nominal = contrast(x, voc, phi)

    common = [xx + math.log(1.0 + COMMON_SCALE_STRESS) for xx in x]
    common_result = contrast(common, voc, phi)

    gain = [(1.0 + LOG_GAIN_STRESS) * xx for xx in x]
    gain_result = contrast(gain, voc, phi)

    mid = 0.5 * (x[0] + x[-1]); halfspan = 0.5 * (x[-1] - x[0])
    raw_delta = [CAL_NONLINEARITY_STRESS * ((xx-mid)/halfspan)**2 for xx in x]
    anchor_delta = raw_delta[ih]
    curved = [xx + (d-anchor_delta) for xx, d in zip(x, raw_delta)]
    curved_result = contrast(curved, voc, phi)

    # Independent analytic normalization-only temperature sensitivity:
    # n_est/n_true = T_true/T_used for a fixed measured Voc slope.
    temp_rel = T_K / (T_K + TEMP_ERROR_K) - 1.0
    temp_contrast_bias = TRUE_CONTRAST * temp_rel

    rows = [
        ["nominal", "true_contrast", nominal, "synthetic", "dimensionless"],
        ["common_scale_+2pct", "contrast", common_result, "synthetic", "dimensionless"],
        ["common_scale_+2pct", "bias", common_result-nominal, "synthetic", "dimensionless"],
        ["log_axis_gain_+0p5pct", "contrast", gain_result, "synthetic", "dimensionless"],
        ["log_axis_gain_+0p5pct", "bias", gain_result-nominal, "synthetic", "dimensionless"],
        ["quadratic_log_residual_0p5pct", "contrast", curved_result, "synthetic", "dimensionless"],
        ["quadratic_log_residual_0p5pct", "bias", curved_result-nominal, "synthetic", "dimensionless"],
        ["temperature_+0p5K_normalization_only", "relative_n_bias", temp_rel, "analytic", "fraction"],
        ["temperature_+0p5K_normalization_only", "contrast_bias", temp_contrast_bias, "analytic", "dimensionless"],
    ]

    if abs(nominal - TRUE_CONTRAST) > 1e-10:
        raise AssertionError((nominal, TRUE_CONTRAST))
    if abs(common_result - nominal) > 1e-12:
        raise AssertionError("common multiplicative scale must cancel from derivative contrast")
    expected_gain = nominal / (1.0 + LOG_GAIN_STRESS)
    if abs(gain_result - expected_gain) > 1e-10:
        raise AssertionError("log-axis gain analytic cross-check failed")
    if not (-0.007 < curved_result-nominal < -0.006):
        raise AssertionError("quadratic calibration stress drifted")

    print(f"nominal_contrast={nominal:.12f}")
    print(f"common_2pct_bias={common_result-nominal:.12e}")
    print(f"log_gain_0p5pct_bias={gain_result-nominal:.12f}")
    print(f"quadratic_residual_0p5pct_bias={curved_result-nominal:.12f}")
    print(f"temp_plus0p5K_relative_n_bias={temp_rel:.12f}")
    print("PASS")

    if len(sys.argv) > 1:
        with open(sys.argv[1], "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f, lineterminator="\n")
            w.writerow(["case", "metric", "value", "class", "unit"])
            w.writerows(rows)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
