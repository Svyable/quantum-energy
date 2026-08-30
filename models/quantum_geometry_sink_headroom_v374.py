#!/usr/bin/env python3
"""Quantum-geometry sink-headroom model v3.74.

Dimensionless first-passage model only. This script does not calculate a
material's topology or quantum metric and does not assign a 4x gain to any
project material.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import random
from io import StringIO
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONTRACT = ROOT / "machine" / "quantum-geometry-sink-headroom-v3.74.json"
DEFAULT_EXPECTED = Path(__file__).with_name("quantum_geometry_sink_headroom_expected_v374.csv")


def capture_probability(x: float, gain: float = 1.0) -> float:
    """P(hit absorbing sink before exponential loss) for dimensionless x."""
    if x < 0:
        raise ValueError("x must be >= 0")
    if gain <= 0:
        raise ValueError("gain must be > 0")
    return math.exp(-x / math.sqrt(gain))


def capture_gain(x: float, gain: float) -> float:
    return capture_probability(x, gain) / capture_probability(x, 1.0)


def break_even_rho(intrinsic_gain: float) -> float:
    if intrinsic_gain <= 0:
        raise ValueError("intrinsic gain must be > 0")
    return 1.0 / intrinsic_gain


def analytic_rows(contract: dict) -> list[dict[str, float]]:
    fixture = contract["synthetic_fixture"]
    out = []
    for x in fixture["x_grid"]:
        p0 = capture_probability(x, 1.0)
        for g in fixture["intrinsic_gain_grid"]:
            p = capture_probability(x, g)
            out.append({
                "x": float(x),
                "G_intrinsic": float(g),
                "P_reference": p0,
                "P_candidate": p,
                "capture_gain": p / p0,
                "rho_break_even": break_even_rho(float(g)),
            })
    return out


def csv_text(rows: list[dict[str, float]]) -> str:
    buf = StringIO()
    fields = ["x", "G_intrinsic", "P_reference", "P_candidate", "capture_gain", "rho_break_even"]
    w = csv.DictWriter(buf, fieldnames=fields, lineterminator="\n")
    w.writeheader()
    for r in rows:
        w.writerow({
            "x": f"{r['x']:.6f}",
            "G_intrinsic": f"{r['G_intrinsic']:.6f}",
            "P_reference": f"{r['P_reference']:.15g}",
            "P_candidate": f"{r['P_candidate']:.15g}",
            "capture_gain": f"{r['capture_gain']:.15g}",
            "rho_break_even": f"{r['rho_break_even']:.15g}",
        })
    return buf.getvalue()


def monte_carlo_capture(x: float, gain: float, draws: int, seed: int) -> float:
    """Independent Brownian first-passage vs exponential-loss simulation.

    Normalize D0=tau=1 and L=x. Candidate D=gain. For 1D Brownian motion
    with variance 2Dt, the exact first-passage time to a boundary a distance
    L away is L^2/(2 D Z^2), Z~N(0,1).
    """
    if x == 0:
        return 1.0
    rng = random.Random(seed)
    hits = 0
    D = gain
    tau = 1.0
    for _ in range(draws):
        z = rng.gauss(0.0, 1.0)
        # z==0 has probability zero; protect the finite PRNG representation.
        while z == 0.0:
            z = rng.gauss(0.0, 1.0)
        t_hit = x * x / (2.0 * D * z * z)
        t_loss = rng.expovariate(1.0 / tau)
        if t_hit < t_loss:
            hits += 1
    return hits / draws


def internal_checks(contract: dict) -> None:
    # Limiting cases.
    assert abs(capture_probability(0.0, 1.0) - 1.0) < 1e-15
    assert abs(capture_probability(2.0, 1.0) - math.exp(-2.0)) < 1e-15

    # Algebraically independent gain identity.
    x, g = 2.0, 4.0
    direct = capture_gain(x, g)
    reduced = math.exp(x * (1.0 - 1.0 / math.sqrt(g)))
    assert abs(direct - reduced) < 1e-15

    # Break-even environment penalty: G*rho=1 must return baseline capture.
    rho = break_even_rho(g)
    assert abs(capture_probability(x, g * rho) - capture_probability(x, 1.0)) < 1e-15

    # Monotonicity in D and sink distance.
    assert capture_probability(2.0, 4.0) > capture_probability(2.0, 2.0) > capture_probability(2.0, 1.0)
    assert capture_probability(1.0, 2.0) > capture_probability(2.0, 2.0)

    # Frozen headline case.
    h = contract["synthetic_fixture"]["headline_case"]
    assert abs(capture_probability(h["x"], 1.0) - h["P_reference"]) < 1e-15
    assert abs(capture_probability(h["x"], h["G_intrinsic"]) - h["P_candidate"]) < 1e-15
    assert abs(capture_gain(h["x"], h["G_intrinsic"]) - h["capture_gain"]) < 1e-15
    assert abs(break_even_rho(h["G_intrinsic"]) - h["rho_break_even"]) < 1e-15


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--contract", type=Path, default=DEFAULT_CONTRACT)
    p.add_argument("--expected", type=Path, default=DEFAULT_EXPECTED)
    p.add_argument("--write-expected", action="store_true")
    p.add_argument("--check-expected", action="store_true")
    p.add_argument("--skip-mc", action="store_true")
    ns = p.parse_args()

    contract = json.loads(ns.contract.read_text(encoding="utf-8"))
    internal_checks(contract)
    generated = csv_text(analytic_rows(contract))

    if ns.write_expected:
        ns.expected.write_text(generated, encoding="utf-8", newline="\n")
    if ns.check_expected:
        frozen = ns.expected.read_text(encoding="utf-8").replace("\r\n", "\n")
        if frozen != generated:
            raise AssertionError("generated table differs from frozen expected CSV")

    h = contract["synthetic_fixture"]["headline_case"]
    print("quantum-geometry sink headroom v3.74: PASS")
    print(f"headline_reference_capture={h['P_reference']:.12f}")
    print(f"headline_candidate_capture={h['P_candidate']:.12f}")
    print(f"headline_capture_gain={h['capture_gain']:.12f}")
    print(f"headline_break_even_rho={h['rho_break_even']:.12f}")

    if not ns.skip_mc:
        v = contract["independent_verification"]
        mc_ref = monte_carlo_capture(h["x"], 1.0, v["mc_draws"], v["mc_seed"])
        mc_candidate = monte_carlo_capture(h["x"], h["G_intrinsic"], v["mc_draws"], v["mc_seed"] + 1)
        tol = v["mc_absolute_tolerance"]
        if abs(mc_ref - h["P_reference"]) > tol:
            raise AssertionError(("MC reference", mc_ref, h["P_reference"]))
        if abs(mc_candidate - h["P_candidate"]) > tol:
            raise AssertionError(("MC candidate", mc_candidate, h["P_candidate"]))
        print(f"mc_reference_capture={mc_ref:.6f}")
        print(f"mc_candidate_capture={mc_candidate:.6f}")
        print(f"mc_tolerance={tol:.6f}")

    print("physical_status=NO_PROJECT_TOPOLOGICAL_EXCITON_EVIDENCE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
