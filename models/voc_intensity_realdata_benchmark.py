#!/usr/bin/env python3
"""External real-data benchmark for Voc-vs-light-intensity ideality extraction.

Downloads the exact Zenodo CSV used for Figure S3 + Figure S16a of:
Wang et al., "Rethinking Charge Transport and Recombination in Donor-Diluted
Organic Solar Cells", Advanced Materials (2026), DOI 10.1002/adma.202523681.

No upstream data are vendored. The downloaded bytes are verified against the
Zenodo-published MD5 before parsing.

Scientific claim boundary: this validates extraction arithmetic on a public
PM6:Y12 dataset. It does not establish that ideality factor uniquely identifies
an interface-recombination mechanism in R2.
"""
from __future__ import annotations

import csv
import hashlib
import io
import math
import sys
import urllib.request
from dataclasses import dataclass
from pathlib import Path

K_B_EV_PER_K = 8.617333262e-5
TEMPERATURE_K = 300.0
SOURCE_URL = (
    "https://zenodo.org/records/20525023/files/"
    "Figure%20S3%20%2B%20Figure%20S16a.csv?download=1"
)
SOURCE_MD5 = "b430562c7fc5bbc6858553911efb8cc1"
EXPECTED_PATH = Path(__file__).with_name("voc_intensity_realdata_expected_v3_13.csv")
WINDOWS = ((0.03, 2.0), (0.05, 0.5), (0.1, 1.0), (0.2, 1.0), (0.1, 2.0), (0.5, 2.0))


@dataclass(frozen=True)
class Point:
    phi_suns: float
    voc_v: float
    published_local_nid: float


def fetch_verified_csv() -> bytes:
    with urllib.request.urlopen(SOURCE_URL, timeout=60) as response:
        payload = response.read()
    digest = hashlib.md5(payload).hexdigest()  # upstream publishes MD5; integrity check only
    if digest != SOURCE_MD5:
        raise RuntimeError(f"source MD5 mismatch: {digest} != {SOURCE_MD5}")
    return payload


def parse_45pct_pm6(payload: bytes) -> list[Point]:
    text = payload.decode("utf-8-sig")
    rows = list(csv.reader(io.StringIO(text)))
    if len(rows) < 4:
        raise RuntimeError("unexpected source CSV structure")

    group_header = rows[1]
    indices = [i for i, value in enumerate(group_header) if value.strip() == "45% PM6"]
    if len(indices) < 2:
        raise RuntimeError(f"could not locate two 45% PM6 column groups: {indices}")
    raw_start, reported_start = indices[0], indices[1]

    points: list[Point] = []
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
        if not (phi > 0 and math.isfinite(voc) and math.isfinite(nid)):
            continue
        if abs(voc - reported_voc) > 5e-6:
            raise RuntimeError("raw Voc and reported-nid Voc columns are misaligned")
        points.append(Point(phi, voc, nid))

    if len(points) < 15:
        raise RuntimeError(f"too few usable 45% PM6 points: {len(points)}")
    return points


def closed_form_fit(points: list[Point], lo: float, hi: float) -> dict[str, float]:
    subset = [p for p in points if lo <= p.phi_suns <= hi]
    if len(subset) < 3:
        raise RuntimeError(f"too few points in window {lo}..{hi}")
    x = [math.log(p.phi_suns) for p in subset]
    y = [p.voc_v for p in subset]
    xm = sum(x) / len(x)
    ym = sum(y) / len(y)
    sxx = sum((v - xm) ** 2 for v in x)
    sxy = sum((vx - xm) * (vy - ym) for vx, vy in zip(x, y))
    slope = sxy / sxx
    intercept = ym - slope * xm
    residuals = [vy - (intercept + slope * vx) for vx, vy in zip(x, y)]
    rss = sum(r * r for r in residuals)
    dof = len(subset) - 2
    se_slope = math.sqrt((rss / dof) / sxx)
    thermal_v = K_B_EV_PER_K * TEMPERATURE_K
    n_fit = slope / thermal_v
    n_se = se_slope / thermal_v
    rmse = math.sqrt(rss / len(subset))
    mean_published = sum(p.published_local_nid for p in subset) / len(subset)
    return {
        "phi_min_suns": lo,
        "phi_max_suns": hi,
        "n_points": float(len(subset)),
        "slope_V_per_ln_sun": slope,
        "n_fit": n_fit,
        "n_fit_se": n_se,
        "voc_rmse_V": rmse,
        "mean_published_local_nid": mean_published,
        "fit_minus_mean_local": n_fit - mean_published,
    }


def endpoint_slope_check(points: list[Point], lo: float, hi: float) -> float:
    subset = [p for p in points if lo <= p.phi_suns <= hi]
    a, b = subset[0], subset[-1]
    return (b.voc_v - a.voc_v) / math.log(b.phi_suns / a.phi_suns)


def read_expected() -> list[dict[str, str]]:
    with EXPECTED_PATH.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def main() -> int:
    payload = fetch_verified_csv()
    points = parse_45pct_pm6(payload)
    expected = read_expected()
    if len(expected) != len(WINDOWS):
        raise RuntimeError("expected-output row count does not match frozen windows")

    results = [closed_form_fit(points, *window) for window in WINDOWS]
    for got, exp in zip(results, expected):
        for key in (
            "slope_V_per_ln_sun",
            "n_fit",
            "n_fit_se",
            "voc_rmse_V",
            "mean_published_local_nid",
            "fit_minus_mean_local",
        ):
            target = float(exp[key])
            if not math.isclose(got[key], target, rel_tol=2e-10, abs_tol=2e-12):
                raise AssertionError(f"{key}: {got[key]} != expected {target}")

    # Independent check: endpoint slope must be physically consistent with the OLS slope.
    # It is intentionally not expected to be identical because the real data are curved.
    nominal = results[2]  # 0.1..1 sun
    endpoint_slope = endpoint_slope_check(points, 0.1, 1.0)
    endpoint_n = endpoint_slope / (K_B_EV_PER_K * TEMPERATURE_K)
    if abs(endpoint_n - nominal["n_fit"]) > 0.08:
        raise AssertionError("independent endpoint-slope check disagrees by >0.08 in ideality")

    print(f"verified_source_md5={SOURCE_MD5}")
    print(f"usable_45pct_points={len(points)}")
    print(f"nominal_0p1_1sun_n={nominal['n_fit']:.9f}")
    print(f"nominal_0p1_1sun_se={nominal['n_fit_se']:.9f}")
    print(f"endpoint_0p1_1sun_n={endpoint_n:.9f}")
    print("PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
