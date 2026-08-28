#!/usr/bin/env python3
"""AT-04 EQE_EL -> DeltaV_nr uncertainty-budget verifier.

All numerical inputs in the bundled JSON fixture are synthetic planning assumptions
except k_B/q and the repository's internal 10 mV planning gate. This script does
not evaluate measured R2 performance.
"""
from __future__ import annotations
import json
import math
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "machine" / "at04-eqeel-uncertainty-budget-v3.44.json"


def delta_v_nr(T_K: float, eqe_el: float, kbq: float) -> float:
    if T_K <= 0 or not (0 < eqe_el <= 1):
        raise ValueError("Require T>0 K and 0<EQE_EL<=1")
    return -(kbq * T_K) * math.log(eqe_el)


def analytic_components(T: float, uT: float, eqe: float, rel_u_eqe: float, kbq: float):
    # First-order propagation. dV/dEQE = -(kT/q)/EQE; dV/dT = -(k/q)ln(EQE).
    u_eqe_V = abs(kbq * T / eqe) * (eqe * rel_u_eqe)
    u_T_V = abs(-kbq * math.log(eqe)) * uT
    return u_eqe_V, u_T_V


def finite_difference_derivatives(T: float, eqe: float, kbq: float):
    # Independent numerical derivative route; step sizes are deterministic and small.
    hT = 1e-4 * T
    he = 1e-6 * eqe
    dVdT = (delta_v_nr(T + hT, eqe, kbq) - delta_v_nr(T - hT, eqe, kbq)) / (2 * hT)
    dVde = (delta_v_nr(T, eqe + he, kbq) - delta_v_nr(T, eqe - he, kbq)) / (2 * he)
    return dVdT, dVde


def rss_with_pair_correlation(components_mV: dict[str, float], rho: float) -> float:
    var = sum(v * v for v in components_mV.values())
    var += 2.0 * rho * components_mV["radiometric_scale"] * components_mV["background_subtraction"]
    if var < 0:
        raise ValueError("Nonphysical negative variance")
    return math.sqrt(var)


def main() -> int:
    c = json.loads(CONTRACT.read_text())
    kbq = c["governing_model"]["k_B_over_q_V_per_K"]["value"]
    f = c["planning_fixture"]
    T = f["T_K"]["value"]
    uT = f["T_K"]["u_1sigma"]
    eqe = f["EQE_EL"]["value"]
    rel = f["EQE_EL"]["relative_u_1sigma"]

    dv = delta_v_nr(T, eqe, kbq)
    if not (dv > 0):
        raise AssertionError("For 0<EQE<1, DeltaV_nr must be positive")
    if delta_v_nr(T, 1.0, kbq) != 0.0:
        raise AssertionError("EQE_EL=1 limiting case must give zero loss")

    ueqe, utemp = analytic_components(T, uT, eqe, rel, kbq)
    dT_fd, de_fd = finite_difference_derivatives(T, eqe, kbq)
    dT_exact = -kbq * math.log(eqe)
    de_exact = -(kbq * T) / eqe
    if not math.isclose(dT_fd, dT_exact, rel_tol=1e-9, abs_tol=1e-12):
        raise AssertionError("Finite-difference T derivative disagrees with analytic derivative")
    if not math.isclose(de_fd, de_exact, rel_tol=2e-10, abs_tol=1e-6):
        raise AssertionError("Finite-difference EQE derivative disagrees with analytic derivative")

    comps = {
        "eqe_relative": ueqe * 1000.0,
        "temperature": utemp * 1000.0,
    }
    for item in f["additional_equivalent_mV_components"]:
        comps[item["name"]] = item["u_1sigma_mV"]

    sensitivity = {}
    for rho in c["correlation_sensitivity"]["radiometric_background_rho"]:
        sensitivity[str(rho)] = rss_with_pair_correlation(comps, rho)

    gate = c["acceptance"]["combined_standard_uncertainty_mV_max"]
    decision_stable = all(v <= gate for v in sensitivity.values())
    dominant = max(comps.items(), key=lambda kv: kv[1])

    out = {
        "classification": "synthetic_planning_result",
        "DeltaV_nr_mV": dv * 1000.0,
        "components_1sigma_mV": comps,
        "combined_mV_by_rho": sensitivity,
        "planning_gate_mV": gate,
        "decision_stable_over_declared_rho_sensitivity": decision_stable,
        "largest_component": {"name": dominant[0], "u_1sigma_mV": dominant[1]},
        "independence_note": "uncertainty components are not experimental replicates",
    }
    print(json.dumps(out, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
