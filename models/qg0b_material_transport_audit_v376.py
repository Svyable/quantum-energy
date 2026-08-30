#!/usr/bin/env python3
"""QG0b v3.76: audit published material transport values and reproduction readiness.

This script deliberately does NOT reproduce the material-specific BSE/DFT/phonon
calculation. It independently checks arithmetic and the SSH bond-swap spectral
identity, then fails closed if asked to claim full material reproduction while
required numerical inputs remain unavailable.
"""

from __future__ import annotations

import argparse
import csv
import math
from fractions import Fraction
from pathlib import Path

PUBLISHED = {
    "polypentacene_topological_D_cm2_s": "1.76",
    "polypentacene_trivial_D_cm2_s": "0.61",
    "polyheptacene_topological_D_cm2_s": "0.44",
    "polyheptacene_trivial_D_cm2_s": "0.103",
}

T1_EV = 0.33
T2_EV = 0.52

MISSING_FOR_EXACT_REPRODUCTION = (
    "plot numeric datasets",
    "first-principles calculation input files",
    "momentum-resolved exciton-energy/group-velocity/scattering-rate data or a full independent recomputation",
    "complete material-specific transport-run inputs for the polyheptacene calculation",
)

REPRODUCTION_LEVEL = "AGGREGATE_VALUES_AND_CONTROL_LOGIC_VERIFIED"
MATERIAL_STATUS = "BLOCKED_PENDING_NUMERIC_DATA_OR_FULL_INDEPENDENT_RECOMPUTATION"
PHYSICAL_STATUS = "NONE_EXTERNAL_COMPUTATIONAL_EVIDENCE_ONLY"


def exact_ratio(numerator: str, denominator: str) -> Fraction:
    return Fraction(numerator) / Fraction(denominator)


def ssh_positive_energy(k: float, t1: float, t2: float) -> float:
    """Positive SSH band energy for two real nearest-neighbour hoppings."""
    return math.sqrt(t1 * t1 + t2 * t2 + 2.0 * t1 * t2 * math.cos(k))


def swap_spectral_error(t1: float = T1_EV, t2: float = T2_EV, points: int = 4097) -> float:
    if points < 3:
        raise ValueError("points must be >= 3")
    max_error = 0.0
    for index in range(points):
        k = -math.pi + (2.0 * math.pi * index / (points - 1))
        normal = ssh_positive_energy(k, t1, t2)
        swapped = ssh_positive_energy(k, t2, t1)
        max_error = max(max_error, abs(normal - swapped))
    return max_error


def audit() -> dict[str, str | float]:
    pent_ratio = exact_ratio(
        PUBLISHED["polypentacene_topological_D_cm2_s"],
        PUBLISHED["polypentacene_trivial_D_cm2_s"],
    )
    hept_ratio = exact_ratio(
        PUBLISHED["polyheptacene_topological_D_cm2_s"],
        PUBLISHED["polyheptacene_trivial_D_cm2_s"],
    )
    return {
        **{key: float(value) for key, value in PUBLISHED.items()},
        "polypentacene_exact_ratio": float(pent_ratio),
        "polyheptacene_exact_ratio": float(hept_ratio),
        "polypentacene_t1_eV": T1_EV,
        "polypentacene_t2_eV": T2_EV,
        "ssh_swap_max_abs_spectral_diff": swap_spectral_error(),
        "reproduction_level": REPRODUCTION_LEVEL,
        "material_transport_reproduction": MATERIAL_STATUS,
        "physical_project_result": PHYSICAL_STATUS,
    }


def read_expected(path: Path) -> dict[str, str]:
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if not rows or set(rows[0]) != {"metric", "value"}:
        raise ValueError("expected fixture must have metric,value columns")
    result: dict[str, str] = {}
    for row in rows:
        metric = row["metric"]
        if metric in result:
            raise ValueError(f"duplicate expected metric: {metric}")
        result[metric] = row["value"]
    return result


def check_expected(path: Path) -> None:
    actual = audit()
    expected = read_expected(path)
    if set(actual) != set(expected):
        missing = sorted(set(actual) - set(expected))
        extra = sorted(set(expected) - set(actual))
        raise AssertionError(f"fixture key mismatch: missing={missing}, extra={extra}")
    for key, observed in actual.items():
        target = expected[key]
        if isinstance(observed, float):
            target_float = float(target)
            tolerance = 1e-15 if key != "ssh_swap_max_abs_spectral_diff" else 1e-14
            if not math.isclose(observed, target_float, rel_tol=1e-14, abs_tol=tolerance):
                raise AssertionError(f"{key}: observed {observed!r}, expected {target_float!r}")
        elif observed != target:
            raise AssertionError(f"{key}: observed {observed!r}, expected {target!r}")


def reject_false_reproduction_claim() -> None:
    if MISSING_FOR_EXACT_REPRODUCTION:
        joined = "; ".join(MISSING_FOR_EXACT_REPRODUCTION)
        raise RuntimeError(
            "FULL_MATERIAL_REPRODUCTION_CLAIM_REJECTED: unresolved inputs remain: " + joined
        )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check-expected",
        action="store_true",
        help="compare the independent arithmetic/control audit against the frozen CSV",
    )
    parser.add_argument(
        "--claim-reproduced",
        action="store_true",
        help="negative-control option: must fail while exact material inputs are unresolved",
    )
    args = parser.parse_args()

    if args.claim_reproduced:
        try:
            reject_false_reproduction_claim()
        except RuntimeError as exc:
            print(str(exc))
            return 2
        return 0

    if args.check_expected:
        fixture = Path(__file__).with_name("qg0b_material_transport_expected_v376.csv")
        check_expected(fixture)

    result = audit()
    print("QG0b material transport audit v3.76: PASS")
    print(f"polypentacene_ratio={result['polypentacene_exact_ratio']:.15f}")
    print(f"polyheptacene_ratio={result['polyheptacene_exact_ratio']:.15f}")
    print(f"ssh_swap_max_abs_spectral_diff={result['ssh_swap_max_abs_spectral_diff']:.3e}")
    print(f"reproduction_level={REPRODUCTION_LEVEL}")
    print(f"material_transport_reproduction={MATERIAL_STATUS}")
    print(f"physical_project_result={PHYSICAL_STATUS}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
