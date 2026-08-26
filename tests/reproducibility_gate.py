#!/usr/bin/env python3
"""Publication-gate regression tests for quantitative quantum-energy work.

This file intentionally exercises two independent layers:
1) the published EQE_EL -> DeltaVnr benchmark (standard-library arithmetic), and
2) the v3.7 raw-spectrum numerical self-tests (NumPy/SciPy path).

Passing this test means those committed calculations are reproducible in the
specified software environment. It is not experimental validation of R2, EPC,
or any physical mechanism.
"""
from __future__ import annotations

import csv
import importlib.util
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
K_B_SI = 1.380649e-23
Q_SI = 1.602176634e-19


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def check_delta_vnr_benchmark() -> None:
    mod = load_module("delta_vnr_benchmark", ROOT / "models" / "delta_vnr_literature_benchmark.py")
    rows = mod.run_benchmark()
    mod.validate(rows)

    # Independent constants/unit path: use exact SI J/K and C rather than the
    # eV/K constant used by the primary implementation.
    for p, row in zip(mod.POINTS, rows, strict=True):
        independent_v = -(K_B_SI * mod.T_BENCHMARK_K / Q_SI) * math.log(p.eqe_el_fraction)
        primary_v = float(row["calculated_delta_vnr_300k_v"])
        if not math.isclose(independent_v, primary_v, rel_tol=0.0, abs_tol=2e-15):
            raise AssertionError(
                f"independent SI cross-check failed for {p.device}: "
                f"{independent_v:.16g} vs {primary_v:.16g} V"
            )

    # Frozen machine-readable output must still correspond to the executable
    # benchmark. This catches silent CSV drift or hand edits.
    csv_path = ROOT / "models" / "delta_vnr_literature_benchmark_v3_8.csv"
    with csv_path.open(newline="", encoding="utf-8") as f:
        frozen = list(csv.DictReader(f))
    if len(frozen) != len(rows):
        raise AssertionError("frozen benchmark CSV row count changed")

    numeric_keys = (
        "eqe_el_fraction",
        "reported_delta_vnr_v",
        "calculated_delta_vnr_300k_v",
        "error_mv",
        "implied_temperature_k",
        "percent_bug_error_mv",
    )
    for expected, actual in zip(rows, frozen, strict=True):
        if expected["device"] != actual["device"]:
            raise AssertionError("frozen benchmark device ordering/identity changed")
        for key in numeric_keys:
            if not math.isclose(float(expected[key]), float(actual[key]), rel_tol=1e-12, abs_tol=1e-12):
                raise AssertionError(f"frozen CSV drift for {expected['device']} {key}")


def check_raw_spectrum_harness() -> None:
    mod = load_module("raw_spectrum_harness", ROOT / "models" / "r2_raw_spectrum_harness.py")
    passed, checks = mod.self_tests(mod.Config())
    if not passed:
        raise AssertionError(f"raw-spectrum self-tests failed: {checks}")

    # Publication-level numerical invariants. These duplicate the decision in
    # explicit assertions so a future refactor cannot weaken self_tests() alone.
    if checks["photon_integral_relative_error"] >= 2e-6:
        raise AssertionError("photon-number conservation gate failed")
    for key in (
        "integral_convergence_ratio_2nm_to_1nm",
        "integral_convergence_ratio_1nm_to_0p5nm",
    ):
        if not 3.5 < checks[key] < 4.5:
            raise AssertionError(f"expected second-order trapezoid convergence not observed: {key}")
    if abs(checks["noiseless_curvefit_sigma_error_meV"]) >= 1e-6:
        raise AssertionError("nonlinear-fit noiseless linewidth regression failed")
    if abs(checks["noiseless_fwhm_sigma_error_meV"]) >= 0.01:
        raise AssertionError("independent FWHM linewidth regression failed")
    if abs(checks["wrong_no_jacobian_center_shift_meV"]) <= 5.0:
        raise AssertionError("deliberate missing-Jacobian failure control is no longer discriminating")


def main() -> None:
    check_delta_vnr_benchmark()
    check_raw_spectrum_harness()
    print("PUBLICATION_REPRODUCIBILITY_GATE=PASS")


if __name__ == "__main__":
    main()
