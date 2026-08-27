#!/usr/bin/env python3
"""R2 v3.36 shipping-control planning and validation.

Standard-library only. All numerical variability inputs in the planning section are
synthetic engineering assumptions; they are not measured R2 performance.
"""

from __future__ import annotations

import csv
import json
import math
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "technical/data/r2_shipping_control_protocol_v3_36.json"
RAW_TEMPLATE = ROOT / "technical/data/r2_shipping_control_raw_template_v3_36.csv"


def normal_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def normal_two_sided_power(delta_mV: float, sigma_mV: float, n_per_arm: int, alpha: float = 0.05) -> float:
    """Normal-approximation power for equal-n two-arm difference in mean changes."""
    if sigma_mV <= 0 or n_per_arm < 2 or not (0 < alpha < 1):
        raise ValueError("invalid power inputs")
    # z_0.975 frozen explicitly because statistics.NormalDist is an independent
    # cross-check in self_test(), not the primary path.
    zcrit = 1.959963984540054
    se = sigma_mV * math.sqrt(2.0 / n_per_arm)
    noncentral = abs(delta_mV) / se
    return 1.0 - normal_cdf(zcrit - noncentral) + normal_cdf(-zcrit - noncentral)


def min_n_for_power(delta_mV: float, sigma_mV: float, target_power: float, alpha: float = 0.05, n_max: int = 200) -> int:
    for n in range(2, n_max + 1):
        if normal_two_sided_power(delta_mV, sigma_mV, n, alpha) >= target_power:
            return n
    raise ValueError("target power not reached within n_max")


def shipping_effect(travel_changes: list[float], home_changes: list[float]) -> tuple[float, float]:
    if len(travel_changes) < 2 or len(home_changes) < 2:
        raise ValueError("at least two independent substrates per arm are required to estimate SE")
    estimate = statistics.mean(travel_changes) - statistics.mean(home_changes)
    se = math.sqrt(statistics.variance(travel_changes) / len(travel_changes) + statistics.variance(home_changes) / len(home_changes))
    return estimate, se


def validate_protocol() -> None:
    data = json.loads(PROTOCOL.read_text())
    assert data["schema_version"] == "3.36"
    assert data["design"]["experimental_unit"] == "independent R2 substrate"
    assert data["design"]["arms"] == ["TRAVEL", "HOME"]
    assert data["design"]["minimum_independent_substrates_per_arm_nominal"] == 6
    assert data["synthetic_power_plan"]["planning_effect_class"].startswith("synthetic")
    assert data["synthetic_power_plan"]["sigma_change_class"].startswith("synthetic")
    assert data["qc_and_exclusions"]["freeze_before_unblinding"] is True
    assert "large unfavorable PRE-to-POST change" in data["qc_and_exclusions"]["not_allowed_as_exclusion"]
    assert data["provenance"]["external_sources"] == []


def validate_raw_template() -> None:
    with RAW_TEMPLATE.open(newline="") as f:
        rows = list(csv.DictReader(f))
    required = {
        "lot_id", "substrate_id", "arm", "session_phase", "measurement_timestamp_iso8601",
        "facility_id", "configuration_id", "analysis_commit", "temperature_K",
        "injection_condition", "delta_vnr_mV", "qc_status", "exclusion_code",
        "carrier_id", "package_integrity_status", "storage_or_shipping_deviation",
    }
    assert required.issubset(rows[0].keys())
    assert {(r["arm"], r["session_phase"]) for r in rows} == {
        ("TRAVEL", "PRE"), ("TRAVEL", "POST"), ("HOME", "PRE"), ("HOME", "POST")
    }


def self_test() -> None:
    validate_protocol()
    validate_raw_template()

    # Frozen nominal planning value.
    nominal = normal_two_sided_power(5.0, 3.0, 6, 0.05)
    assert abs(nominal - 0.8229821534848882) < 1e-12

    # Sensitivity table.
    expected = {2.0: 3, 3.0: 6, 4.0: 11, 5.0: 16}
    got = {sigma: min_n_for_power(5.0, sigma, 0.80) for sigma in expected}
    assert got == expected

    # Useful negative result: three per arm is underpowered at nominal sigma.
    p3 = normal_two_sided_power(5.0, 3.0, 3, 0.05)
    assert abs(p3 - 0.5324208639051091) < 1e-12

    # Independent implementation cross-check using NormalDist for z critical and CDF.
    nd = statistics.NormalDist()
    zcrit_ind = nd.inv_cdf(0.975)
    se = 3.0 * math.sqrt(2.0 / 6.0)
    nc = 5.0 / se
    independent = 1.0 - nd.cdf(zcrit_ind - nc) + nd.cdf(-zcrit_ind - nc)
    assert abs(independent - nominal) < 1e-12

    # Limiting cases for estimator and sign convention.
    est, se0 = shipping_effect([2.0, 2.0, 2.0], [2.0, 2.0, 2.0])
    assert est == 0.0 and se0 == 0.0
    est5, _ = shipping_effect([5.0, 5.0, 5.0], [0.0, 0.0, 0.0])
    assert est5 == 5.0
    swapped, _ = shipping_effect([0.0, 0.0, 0.0], [5.0, 5.0, 5.0])
    assert swapped == -5.0

    print("v3.36 PASS")
    print(f"nominal_power_n6={nominal:.12f}")
    print(f"nominal_power_n3={p3:.12f}")
    print("min_n_by_sigma=" + json.dumps(got, sort_keys=True))


if __name__ == "__main__":
    try:
        self_test()
    except Exception as exc:
        print(f"v3.36 FAIL: {exc}", file=sys.stderr)
        raise
