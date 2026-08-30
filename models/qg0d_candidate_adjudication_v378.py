#!/usr/bin/env python3
"""QG0d-prep candidate adjudication and transport-reach arithmetic v3.78.

External printed diffusion values are treated as literature inputs, not project
measurements. Cross-study PBE/GW labels do not establish a same-structure
method-consensus calculation.
"""

from __future__ import annotations

import argparse
import csv
import math
import sys
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path


@dataclass(frozen=True)
class Candidate:
    name: str
    n_rings: int
    pbe_label: str
    gw_label: str
    same_structure_adjudicated: bool
    d_top_cm2_s: Fraction
    d_triv_cm2_s: Fraction


N5 = Candidate(
    name="polypentacene",
    n_rings=5,
    pbe_label="TOPOLOGICAL",
    gw_label="TRIVIAL",
    same_structure_adjudicated=False,
    d_top_cm2_s=Fraction(176, 100),
    d_triv_cm2_s=Fraction(61, 100),
)

N7 = Candidate(
    name="polyheptacene",
    n_rings=7,
    pbe_label="TOPOLOGICAL",
    gw_label="TOPOLOGICAL",
    same_structure_adjudicated=False,
    d_top_cm2_s=Fraction(44, 100),
    d_triv_cm2_s=Fraction(103, 1000),
)

CANDIDATES = (N5, N7)


def cross_study_status(c: Candidate) -> str:
    if c.pbe_label != c.gw_label:
        return "CROSS_STUDY_METHOD_CONFLICT"
    if c.pbe_label == "TOPOLOGICAL":
        return "CROSS_STUDY_LABEL_AGREEMENT_TOPOLOGICAL"
    return "CROSS_STUDY_LABEL_AGREEMENT_TRIVIAL"


def same_structure_status(c: Candidate) -> str:
    if not c.same_structure_adjudicated:
        return "NOT_ADJUDICATED_SAME_STRUCTURE"
    if c.pbe_label != c.gw_label:
        return "SAME_STRUCTURE_METHOD_CONFLICT"
    return f"SAME_STRUCTURE_METHOD_CONSENSUS_{c.pbe_label}"


def diffusion_ratio(c: Candidate) -> Fraction:
    return c.d_top_cm2_s / c.d_triv_cm2_s


def reach_gain(c: Candidate) -> float:
    """Diffusion-length gain if lifetime is unchanged within a candidate pair."""
    return math.sqrt(float(diffusion_ratio(c)))


def equal_lifetime_reach_ratio(candidate: Candidate, reference: Candidate) -> float:
    """L_D,candidate/L_D,reference for equal lifetime, using L_D proportional sqrt(D*tau)."""
    return math.sqrt(float(candidate.d_top_cm2_s / reference.d_top_cm2_s))


def lifetime_ratio_for_equal_reach(candidate: Candidate, reference: Candidate) -> Fraction:
    """tau_candidate/tau_reference needed for equal D*tau and equal diffusion length."""
    return reference.d_top_cm2_s / candidate.d_top_cm2_s


def choose_primary() -> str:
    """Hard-gate selection: cross-study topological agreement is required before transport ranking."""
    eligible = [c for c in CANDIDATES if cross_study_status(c) == "CROSS_STUDY_LABEL_AGREEMENT_TOPOLOGICAL"]
    if len(eligible) != 1:
        return "NO_UNIQUE_CROSS_STUDY_TOPOLOGY_CANDIDATE"
    return eligible[0].name


def rows():
    n5_ratio = diffusion_ratio(N5)
    n7_ratio = diffusion_ratio(N7)
    tau_ratio = lifetime_ratio_for_equal_reach(N7, N5)
    return [
        ("n5_cross_study_status", cross_study_status(N5)),
        ("n7_cross_study_status", cross_study_status(N7)),
        ("n5_same_structure_status", same_structure_status(N5)),
        ("n7_same_structure_status", same_structure_status(N7)),
        ("n5_topological_diffusion_cm2_s_printed", f"{float(N5.d_top_cm2_s):.3f}"),
        ("n7_topological_diffusion_cm2_s_printed", f"{float(N7.d_top_cm2_s):.3f}"),
        ("n5_topological_trivial_ratio_exact", f"{n5_ratio.numerator}/{n5_ratio.denominator}"),
        ("n7_topological_trivial_ratio_exact", f"{n7_ratio.numerator}/{n7_ratio.denominator}"),
        ("n5_reach_gain_equal_lifetime", f"{reach_gain(N5):.12f}"),
        ("n7_reach_gain_equal_lifetime", f"{reach_gain(N7):.12f}"),
        ("n7_vs_n5_reach_equal_lifetime", f"{equal_lifetime_reach_ratio(N7, N5):.12f}"),
        ("tau7_over_tau5_for_equal_topological_reach_exact", f"{tau_ratio.numerator}/{tau_ratio.denominator}"),
        ("qg0d_primary_candidate", choose_primary()),
        ("qg0d_method_sensitivity_control", N5.name),
        ("same_structure_method_consensus_claim", "BLOCKED_PENDING_IDENTICAL_STRUCTURE_PBE_GW_ADJUDICATION"),
        ("physical_result", "NONE_EXTERNAL_COMPUTATIONAL_EVIDENCE_ONLY"),
    ]


def write_expected(path: Path) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(["metric", "value"])
        writer.writerows(rows())


def run_checks() -> list[str]:
    failures: list[str] = []
    if diffusion_ratio(N5) != Fraction(176, 61):
        failures.append("N5 exact diffusion ratio")
    if diffusion_ratio(N7) != Fraction(440, 103):
        failures.append("N7 exact diffusion ratio")
    if lifetime_ratio_for_equal_reach(N7, N5) != Fraction(4, 1):
        failures.append("N7 lifetime compensation")
    if abs(equal_lifetime_reach_ratio(N7, N5) - 0.5) > 1e-15:
        failures.append("N7/N5 equal-lifetime reach")
    if cross_study_status(N5) != "CROSS_STUDY_METHOD_CONFLICT":
        failures.append("N5 method conflict")
    if cross_study_status(N7) != "CROSS_STUDY_LABEL_AGREEMENT_TOPOLOGICAL":
        failures.append("N7 cross-study label agreement")
    if same_structure_status(N7) != "NOT_ADJUDICATED_SAME_STRUCTURE":
        failures.append("same-structure fail-closed")
    if choose_primary() != "polyheptacene":
        failures.append("hard-gate candidate selection")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-expected", action="store_true")
    parser.add_argument("--write-expected", type=Path)
    parser.add_argument("--assert-same-structure-consensus", action="store_true")
    parser.add_argument("--assert-n5-robust-topology", action="store_true")
    args = parser.parse_args()

    if args.assert_same_structure_consensus:
        print("FAIL: same-structure PBE/GW adjudication has not been performed for the frozen literature fixture.", file=sys.stderr)
        return 2
    if args.assert_n5_robust_topology:
        print("FAIL: N=5 has a cross-study PBE/GW topology conflict.", file=sys.stderr)
        return 3

    if args.write_expected:
        write_expected(args.write_expected)

    if args.check_expected:
        failures = run_checks()
        if failures:
            print("QG0d-prep v3.78: FAIL: " + ", ".join(failures), file=sys.stderr)
            return 1

    print("QG0d-prep candidate adjudication v3.78: PASS")
    print(f"N5_status={cross_study_status(N5)}")
    print(f"N7_status={cross_study_status(N7)}")
    print(f"N5_diffusion_ratio={float(diffusion_ratio(N5)):.12f}")
    print(f"N7_diffusion_ratio={float(diffusion_ratio(N7)):.12f}")
    print(f"N5_reach_gain={reach_gain(N5):.12f}")
    print(f"N7_reach_gain={reach_gain(N7):.12f}")
    print(f"N7_vs_N5_equal_lifetime_reach={equal_lifetime_reach_ratio(N7, N5):.12f}")
    print(f"tau7_over_tau5_for_equal_reach={float(lifetime_ratio_for_equal_reach(N7, N5)):.12f}")
    print(f"qg0d_primary_candidate={choose_primary()}")
    print("same_structure_method_consensus_claim=BLOCKED_PENDING_IDENTICAL_STRUCTURE_PBE_GW_ADJUDICATION")
    print("physical_result=NONE_EXTERNAL_COMPUTATIONAL_EVIDENCE_ONLY")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
