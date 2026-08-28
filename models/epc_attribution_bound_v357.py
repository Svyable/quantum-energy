from fractions import Fraction
import json

SYSTEMS = {
    "PA_D18_PYIT": {"total_mev": 55, "epc_only_mev": 35},
    "SMA_D18_eC9": {"total_mev": 38, "epc_only_mev": 20},
}
TOL = 1e-12


def analyze(total_mev, epc_only_mev):
    total = total_mev
    epc = epc_only_mev
    if total <= 0 or epc < 0:
        raise ValueError("require total>0 and epc>=0")
    fraction = epc / total
    exact = float(Fraction(epc, total))
    if abs(fraction - exact) > TOL:
        raise AssertionError("fraction cross-check failed")
    gap = total - epc
    return {
        "epc_fraction_of_reported_total": fraction,
        "epc_percent_of_reported_total": 100.0 * fraction,
        "gap_mev": gap,
        "equal_opposite_perturbation_to_close_gap_mev": gap / 2.0,
        "epc_alone_nominally_accounts_for_all": epc >= total,
    }


def main():
    out = {name: analyze(**vals) for name, vals in SYSTEMS.items()}
    assert out["PA_D18_PYIT"]["epc_fraction_of_reported_total"] < 1.0
    assert out["SMA_D18_eC9"]["epc_fraction_of_reported_total"] < 1.0

    # Limiting case: EPC-only equals the reported total.
    limit = analyze(total_mev=40, epc_only_mev=40)
    assert abs(limit["epc_fraction_of_reported_total"] - 1.0) <= TOL
    assert limit["gap_mev"] == 0

    # Negative/control: an EPC-only number larger than total is a warning that
    # the quantities are not a simple additive decomposition.
    control = analyze(total_mev=40, epc_only_mev=45)
    assert control["epc_alone_nominally_accounts_for_all"] is True

    print(json.dumps({"results": out, "checks": "PASS"}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
