#!/usr/bin/env python3
"""Independent arithmetic packet for v3.54 external FF-loss benchmark.

Standard library only. This script does not reproduce Zhang et al.'s full device
model. It verifies the decision-driving scalar comparison recorded in the
machine-readable input contract.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "models" / "inputs" / "d18_field_generation_external_benchmark_v354.json"


def load() -> dict:
    return json.loads(INPUT.read_text(encoding="utf-8"))


def direct(ff_measured: float, ff_transport: float, h: float) -> dict[str, float]:
    if not (0.0 < ff_measured <= 1.0 and 0.0 < ff_transport <= 1.0):
        raise ValueError("FF values must be dimensionless fractions in (0, 1].")
    if h < 0 or ff_transport <= h or ff_measured <= h:
        raise ValueError("Invalid reporting-resolution half-width.")
    r = ff_measured / ff_transport
    return {
        "ff_retention": r,
        "absolute_ff_deficit": ff_transport - ff_measured,
        "relative_ff_deficit": 1.0 - r,
        "rounding_retention_min": (ff_measured - h) / (ff_transport + h),
        "rounding_retention_max": (ff_measured + h) / (ff_transport - h),
        "rounding_deficit_min": (ff_transport - h) - (ff_measured + h),
        "rounding_deficit_max": (ff_transport + h) - (ff_measured - h),
    }


def independent_log_ratio(ff_measured: float, ff_transport: float) -> float:
    """Numerically distinct cross-check of FF_measured / FF_transport."""
    return math.exp(math.log(ff_measured) - math.log(ff_transport))


def assert_close(a: float, b: float, tol: float, label: str) -> None:
    if not math.isclose(a, b, rel_tol=tol, abs_tol=tol):
        raise AssertionError(f"{label}: {a!r} != {b!r} within {tol}")


def self_test() -> dict[str, float]:
    d = load()
    ffm = float(d["inputs"]["ff_measured"]["value"])
    fft = float(d["inputs"]["ff_transport_reconstructed"]["value"])
    h = float(d["inputs"]["ff_measured"]["reporting_resolution_half_width"])
    tol = float(d["numerical_tolerance"])

    out = direct(ffm, fft, h)
    expected = d["expected_outputs"]
    for key, val in out.items():
        assert_close(val, float(expected[key]), tol, key)

    # Independent arithmetic path: ratio through log space.
    assert_close(out["ff_retention"], independent_log_ratio(ffm, fft), tol, "log-ratio cross-check")

    # Dimensional/normalization checks: FF and all three headline metrics are dimensionless.
    assert 0.0 < out["ff_retention"] < 1.0
    assert 0.0 < out["absolute_ff_deficit"] < 1.0
    assert 0.0 < out["relative_ff_deficit"] < 1.0

    # Limiting case: equal measured and reconstructed FF gives no deficit.
    eq = direct(0.58, 0.58, h)
    assert_close(eq["ff_retention"], 1.0, tol, "equal-FF retention")
    assert_close(eq["absolute_ff_deficit"], 0.0, tol, "equal-FF absolute deficit")
    assert_close(eq["relative_ff_deficit"], 0.0, tol, "equal-FF relative deficit")

    # Negative/control case: measured FF greater than reference must produce negative deficit.
    neg = direct(0.60, 0.58, h)
    if not neg["absolute_ff_deficit"] < 0.0:
        raise AssertionError("negative/control case failed")

    # Reporting-resolution sensitivity must not reverse the qualitative decision.
    if not out["rounding_retention_max"] < 0.5:
        raise AssertionError("two-decimal rounding interval unexpectedly permits >=50% retention")
    if not out["rounding_deficit_min"] > 0.0:
        raise AssertionError("two-decimal rounding interval unexpectedly permits zero deficit")

    return out


def main() -> None:
    out = self_test()
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
