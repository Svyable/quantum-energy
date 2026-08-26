#!/usr/bin/env python3
"""Benchmark a local Voc-vs-light-intensity ideality estimator on real PM6:Y12 data.

Downloads the exact Zenodo CSV used for Figure S3 + Figure S16a of Wang et al.
(Advanced Materials, 2026; DOI 10.1002/adma.202523681), verifies the
Zenodo-published MD5, extracts the 45% PM6 series, and compares a local
quadratic derivative in ln(light intensity) against the source-provided local
ideality-factor series.

Scientific boundary: agreement with the source-provided local series validates
an estimator on one published material system. It does not make ideality factor
a unique recombination-mechanism identifier in R2.
"""
from __future__ import annotations

import csv
import hashlib
import io
import math
import random
import urllib.request
from dataclasses import dataclass

K_B_EV_PER_K = 8.617333262e-5
TEMPERATURE_K = 300.0
SOURCE_URL = (
    "https://zenodo.org/records/20525023/files/"
    "Figure%20S3%20%2B%20Figure%20S16a.csv?download=1"
)
SOURCE_MD5 = "b430562c7fc5bbc6858553911efb8cc1"
PRIMARY_MIN_SUN = 0.05
PRIMARY_MAX_SUN = 2.0
PRIMARY_WINDOW = 7
SENSITIVITY_WINDOW = 9
NOISE_SIGMA_MV = 0.5  # synthetic planning stress, not source measurement noise
NOISE_REPS = 5000
SEED = 20260826


@dataclass(frozen=True)
class Point:
    phi_suns: float
    voc_v: float
    published_local_nid: float


def fetch_verified_csv() -> bytes:
    with urllib.request.urlopen(SOURCE_URL, timeout=60) as response:
        payload = response.read()
    digest = hashlib.md5(payload).hexdigest()  # upstream integrity field
    if digest != SOURCE_MD5:
        raise RuntimeError(f"source MD5 mismatch: {digest} != {SOURCE_MD5}")
    return payload


def parse_45pct_pm6(payload: bytes) -> list[Point]:
    rows = list(csv.reader(io.StringIO(payload.decode("utf-8-sig"))))
    group_header = rows[1]
    indices = [i for i, value in enumerate(group_header) if value.strip() == "45% PM6"]
    if len(indices) < 2:
        raise RuntimeError(f"could not locate two 45% PM6 groups: {indices}")
    raw_start, reported_start = indices[0], indices[1]
    out: list[Point] = []
    for row in rows[3:]:
        if len(row) <= max(raw_start + 1, reported_start + 1):
            continue
        try:
            phi = float(row[raw_start])
            voc = float(row[raw_start + 1])
            reported_voc = float(row[reported_start])
            nid = float(row[reported_start + 1])
        except (ValueError, IndexError):
            continue
        if phi <= 0 or not all(math.isfinite(v) for v in (voc, nid)):
            continue
        if abs(voc - reported_voc) > 5e-6:
            raise RuntimeError("raw Voc and local-nid Voc columns are misaligned")
        out.append(Point(phi, voc, nid))
    if len(out) < 20:
        raise RuntimeError(f"too few usable 45% PM6 points: {len(out)}")
    return out


def solve3(a: list[list[float]], b: list[float]) -> list[float]:
    """Small independent Gaussian-elimination solver for 3x3 normal equations."""
    m = [row[:] + [rhs] for row, rhs in zip(a, b)]
    for col in range(3):
        pivot = max(range(col, 3), key=lambda r: abs(m[r][col]))
        m[col], m[pivot] = m[pivot], m[col]
        if abs(m[col][col]) < 1e-18:
            raise RuntimeError("singular local polynomial fit")
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


def local_quadratic_nid(points: list[Point], window: int, voc_override: list[float] | None = None) -> list[float]:
    if window < 3 or window % 2 == 0 or window > len(points):
        raise ValueError("window must be odd, >=3, and <= number of points")
    x = [math.log(p.phi_suns) for p in points]
    y = voc_override if voc_override is not None else [p.voc_v for p in points]
    thermal_v = K_B_EV_PER_K * TEMPERATURE_K
    result: list[float] = []
    half = window // 2
    for i in range(len(points)):
        lo = max(0, min(i - half, len(points) - window))
        hi = lo + window
        u = [x[j] - x[i] for j in range(lo, hi)]
        yy = y[lo:hi]
        sums = [sum(v ** k for v in u) for k in range(5)]
        rhs = [sum(val * (v ** k) for val, v in zip(yy, u)) for k in range(3)]
        normal = [
            [sums[0], sums[1], sums[2]],
            [sums[1], sums[2], sums[3]],
            [sums[2], sums[3], sums[4]],
        ]
        _a0, b1, _c2 = solve3(normal, rhs)
        result.append(b1 / thermal_v)
    return result


def metrics(points: list[Point], pred: list[float]) -> dict[str, float]:
    chosen = [i for i, p in enumerate(points) if PRIMARY_MIN_SUN <= p.phi_suns <= PRIMARY_MAX_SUN]
    err = [pred[i] - points[i].published_local_nid for i in chosen]
    mae = sum(abs(v) for v in err) / len(err)
    rmse = math.sqrt(sum(v * v for v in err) / len(err))
    max_abs = max(abs(v) for v in err)
    src = [points[i].published_local_nid for i in chosen]
    est = [pred[i] for i in chosen]
    sm, em = sum(src) / len(src), sum(est) / len(est)
    num = sum((a-sm)*(b-em) for a,b in zip(src,est))
    den = math.sqrt(sum((a-sm)**2 for a in src) * sum((b-em)**2 for b in est))
    return {"n_points": float(len(chosen)), "mae": mae, "rmse": rmse, "max_abs": max_abs, "pearson_r": num/den}


def noise_stress(points: list[Point], window: int) -> tuple[float, float]:
    rng = random.Random(SEED + window)
    maes: list[float] = []
    for _ in range(NOISE_REPS):
        noisy = [p.voc_v + rng.gauss(0.0, NOISE_SIGMA_MV / 1000.0) for p in points]
        pred = local_quadratic_nid(points, window, noisy)
        maes.append(metrics(points, pred)["mae"])
    maes.sort()
    median = maes[len(maes)//2]
    p95 = maes[math.ceil(0.95 * len(maes)) - 1]
    return median, p95


def main() -> int:
    points = parse_45pct_pm6(fetch_verified_csv())
    primary = metrics(points, local_quadratic_nid(points, PRIMARY_WINDOW))
    smooth = metrics(points, local_quadratic_nid(points, SENSITIVITY_WINDOW))
    med7, p957 = noise_stress(points, PRIMARY_WINDOW)
    med9, p959 = noise_stress(points, SENSITIVITY_WINDOW)

    # Frozen acceptance values are deliberately broad enough for CSV decimal precision,
    # but narrow enough to detect algorithm drift.
    if int(primary["n_points"]) != 16:
        raise AssertionError(f"unexpected primary point count: {primary['n_points']}")
    if not (primary["mae"] < 0.006 and primary["rmse"] < 0.010 and primary["pearson_r"] > 0.995):
        raise AssertionError(f"7-point benchmark failed: {primary}")
    if not (smooth["mae"] < 0.010 and smooth["rmse"] < 0.012):
        raise AssertionError(f"9-point sensitivity benchmark failed: {smooth}")
    if not (p957 < 0.035 and p959 < 0.030):
        raise AssertionError(f"0.5 mV synthetic noise stress failed: p95 7={p957}, 9={p959}")

    print(f"verified_source_md5={SOURCE_MD5}")
    print(f"usable_points={len(points)} primary_points={int(primary['n_points'])}")
    print(f"local7_mae={primary['mae']:.9f} local7_rmse={primary['rmse']:.9f} r={primary['pearson_r']:.9f}")
    print(f"local9_mae={smooth['mae']:.9f} local9_rmse={smooth['rmse']:.9f}")
    print(f"noise_0p5mV_local7_median_mae={med7:.9f} p95={p957:.9f}")
    print(f"noise_0p5mV_local9_median_mae={med9:.9f} p95={p959:.9f}")
    print("PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
