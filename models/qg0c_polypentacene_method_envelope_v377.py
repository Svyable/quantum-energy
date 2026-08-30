#!/usr/bin/env python3
"""QG0c polypentacene method-dependence and control-envelope audit v3.77."""

import argparse
import csv
import math
import sys
from pathlib import Path

T1_EV = 0.33
T2_EV = 0.52
A_ANGSTROM = 6.89
STRAIN_CROSSOVER_LOW = 0.05
STRAIN_CROSSOVER_HIGH = 0.10

EXPECTED = {
    "ordering_margin_fraction": 0.22352941176470587,
    "xi2_lower_bound_A2": 11.868025,
    "xi_lower_bound_A": 3.445,
    "log_hopping_ratio": 0.4547361571149471,
    "Cdiff_min": 4.547361571149471,
    "Cdiff_max": 9.094723142298942,
}


def ssh_energy(k: float, t1: float, t2: float) -> float:
    return math.sqrt(t1 * t1 + t2 * t2 + 2.0 * t1 * t2 * math.cos(k))


def classify(t1: float, t2: float) -> str:
    if math.isclose(t1, t2, rel_tol=0.0, abs_tol=1e-15):
        return "GAP_CLOSING_BOUNDARY"
    return "TOPOLOGICAL_SSH" if t2 > t1 else "TRIVIAL_SSH"


def relative_ordering_radius(t1: float, t2: float) -> float:
    """Largest symmetric fractional perturbation r preserving t2(1-r)>t1(1+r)."""
    return (t2 - t1) / (t2 + t1)


def strain_sensitivity_difference_bracket(t1: float, t2: float, gamma_lo: float, gamma_hi: float):
    """For a crossover gamma_c in [lo,hi], C2-C1=ln(t2/t1)/gamma_c."""
    lr = math.log(t2 / t1)
    return lr / gamma_hi, lr / gamma_lo


def verify_swap_spectrum(t1: float, t2: float, n: int = 2001) -> float:
    max_diff = 0.0
    for i in range(n):
        k = -math.pi + (2.0 * math.pi * i / (n - 1))
        diff = abs(ssh_energy(k, t1, t2) - ssh_energy(k, t2, t1))
        max_diff = max(max_diff, diff)
    return max_diff


def write_expected(path: Path):
    rows = [
        ("t1_eV", T1_EV),
        ("t2_eV", T2_EV),
        ("a_angstrom", A_ANGSTROM),
        ("ssh_classification", classify(T1_EV, T2_EV)),
        ("ordering_margin_fraction", relative_ordering_radius(T1_EV, T2_EV)),
        ("xi2_lower_bound_A2", A_ANGSTROM**2 / 4.0),
        ("xi_lower_bound_A", A_ANGSTROM / 2.0),
        ("log_hopping_ratio", math.log(T2_EV / T1_EV)),
    ]
    cmin, cmax = strain_sensitivity_difference_bracket(
        T1_EV, T2_EV, STRAIN_CROSSOVER_LOW, STRAIN_CROSSOVER_HIGH
    )
    rows.extend([
        ("Cdiff_min", cmin),
        ("Cdiff_max", cmax),
        ("material_topology_claim", "METHOD_DEPENDENT_NOT_ROBUST"),
        ("physical_result", "NONE_EXTERNAL_COMPUTATIONAL_EVIDENCE_ONLY"),
    ])
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["metric", "value"])
        writer.writerows(rows)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check-expected", action="store_true")
    ap.add_argument("--write-expected", type=Path)
    ap.add_argument("--assert-robust-material-topology", action="store_true")
    args = ap.parse_args()

    cls = classify(T1_EV, T2_EV)
    margin = relative_ordering_radius(T1_EV, T2_EV)
    xi2 = A_ANGSTROM**2 / 4.0
    xi = A_ANGSTROM / 2.0
    lr = math.log(T2_EV / T1_EV)
    cmin, cmax = strain_sensitivity_difference_bracket(
        T1_EV, T2_EV, STRAIN_CROSSOVER_LOW, STRAIN_CROSSOVER_HIGH
    )
    spectrum_error = verify_swap_spectrum(T1_EV, T2_EV)

    if args.assert_robust_material_topology:
        print("FAIL: robust material-topology claim blocked by DFT/GW method disagreement.", file=sys.stderr)
        return 2

    if args.write_expected:
        write_expected(args.write_expected)

    if args.check_expected:
        checks = [
            (cls == "TOPOLOGICAL_SSH", "public SSH anchor must classify t2>t1"),
            (abs(margin - EXPECTED["ordering_margin_fraction"]) < 1e-14, "ordering margin"),
            (abs(xi2 - EXPECTED["xi2_lower_bound_A2"]) < 1e-12, "xi2 bound"),
            (abs(xi - EXPECTED["xi_lower_bound_A"]) < 1e-12, "xi bound"),
            (abs(lr - EXPECTED["log_hopping_ratio"]) < 1e-14, "log hopping ratio"),
            (abs(cmin - EXPECTED["Cdiff_min"]) < 1e-13, "Cdiff min"),
            (abs(cmax - EXPECTED["Cdiff_max"]) < 1e-13, "Cdiff max"),
            (spectrum_error < 1e-14, "bond-swap spectrum identity"),
        ]
        failed = [name for ok, name in checks if not ok]
        if failed:
            print("QG0c v3.77: FAIL: " + ", ".join(failed), file=sys.stderr)
            return 1

    print("QG0c polypentacene control-envelope v3.77: PASS")
    print(f"ssh_classification={cls}")
    print(f"ordering_margin_fraction={margin:.12f}")
    print(f"xi_lower_bound_A={xi:.12f}")
    print(f"C2_minus_C1_bracket={cmin:.12f},{cmax:.12f}")
    print(f"swap_spectrum_max_abs_error_eV={spectrum_error:.3e}")
    print("material_topology_claim=METHOD_DEPENDENT_NOT_ROBUST")
    print("physical_result=NONE_EXTERNAL_COMPUTATIONAL_EVIDENCE_ONLY")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
