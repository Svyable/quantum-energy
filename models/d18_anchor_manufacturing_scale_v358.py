#!/usr/bin/env python3
"""v3.58 D18/PY-IT/eC9 anchor manufacturing-scale evidence audit.

Standard-library only. This script does not model scale-up performance. It checks the
arithmetic evidence boundary between the published 0.041 cm^2 illuminated device area
and this repository's existing 1 cm^2 / 10 cm^2 scale-transfer engineering stages.
"""
from fractions import Fraction
import json
from pathlib import Path

TOL = 1e-12
ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "research" / "benchmarks" / "d18-anchor-manufacturing-scale-v3.58.json"


def close(a: float, b: float, tol: float = TOL) -> bool:
    return abs(a - b) <= tol


def classify(illuminated_area_cm2: float, first_scale_cm2: float) -> str:
    if illuminated_area_cm2 <= 0 or first_scale_cm2 <= 0:
        raise ValueError("areas must be positive")
    return "LAB_SCALE_ONLY" if illuminated_area_cm2 < first_scale_cm2 else "SCALE_STAGE_REACHED"


def main() -> None:
    data = json.loads(INPUT.read_text())
    source = data["source"]["methods_facts"]
    targets = data["project_reference_areas"]
    expected = data["expected"]

    illum = float(source["illuminated_area_cm2"])
    contact = float(source["contact_area_cm2"])
    a1 = float(targets["first_scale_transfer_cm2"])
    a10 = float(targets["later_scale_transfer_cm2"])

    factor1 = a1 / illum
    factor10 = a10 / illum
    excess = (contact - illum) / contact

    # Independent exact-rational check from the published decimal strings.
    illum_q = Fraction(str(source["illuminated_area_cm2"]))
    contact_q = Fraction(str(source["contact_area_cm2"]))
    factor1_q = Fraction(str(targets["first_scale_transfer_cm2"])) / illum_q
    factor10_q = Fraction(str(targets["later_scale_transfer_cm2"])) / illum_q
    excess_q = (contact_q - illum_q) / contact_q

    checks = [
        close(factor1, float(factor1_q)),
        close(factor10, float(factor10_q)),
        close(excess, float(excess_q)),
        close(factor1, expected["factor_to_1cm2"]),
        close(factor10, expected["factor_to_10cm2"]),
        close(excess, expected["contact_to_illuminated_area_excess_fraction"]),
        classify(illum, a1) == expected["classification"],
        # Limiting/control case: exactly 1 cm^2 reaches the first project scale stage.
        classify(a1, a1) == "SCALE_STAGE_REACHED",
    ]

    # Negative/adversarial case: invalid zero area must fail rather than create an infinity.
    try:
        classify(0.0, a1)
        checks.append(False)
    except ValueError:
        checks.append(True)

    result = {
        "factor_to_1cm2": factor1,
        "factor_to_10cm2": factor10,
        "contact_to_illuminated_area_excess_fraction": excess,
        "classification": classify(illum, a1),
        "checks": "PASS" if all(checks) else "FAIL",
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    if result["checks"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
