from fractions import Fraction

TOL = 1e-12


def ratio(test_h: float, ref_h: float) -> float:
    if test_h <= 0 or ref_h <= 0:
        raise ValueError("T80 values must be positive")
    return test_h / ref_h


def main() -> None:
    thermal = ratio(2500.0, 1200.0)
    light = ratio(710.0, 550.0)
    thermal_gain = thermal - 1.0
    light_gain = light - 1.0
    ratio_of_ratios = thermal / light

    # Independent exact-rational recomputation.
    thermal_exact = Fraction(2500, 1200)
    light_exact = Fraction(710, 550)
    ratio_of_ratios_exact = thermal_exact / light_exact

    assert abs(thermal - float(thermal_exact)) <= TOL
    assert abs(light - float(light_exact)) <= TOL
    assert abs(ratio_of_ratios - float(ratio_of_ratios_exact)) <= TOL

    # Limiting case: identical T80 gives ratio 1 and zero relative gain.
    assert ratio(1000.0, 1000.0) == 1.0

    # Negative/adversarial case: a shorter ternary lifetime must remain <1.
    assert ratio(800.0, 1000.0) < 1.0

    # Fail closed on invalid domains.
    for bad_test, bad_ref in [(0.0, 1000.0), (-1.0, 1000.0), (1000.0, 0.0)]:
        try:
            ratio(bad_test, bad_ref)
        except ValueError:
            pass
        else:
            raise AssertionError("invalid T80 domain did not fail closed")

    # Decision-relevant stress-mode sensitivity: the relative advantage is not equal.
    assert thermal > light

    print(f"thermal_ratio={thermal:.12f}")
    print(f"thermal_relative_gain={thermal_gain:.12f}")
    print(f"light_ratio={light:.12f}")
    print(f"light_relative_gain={light_gain:.12f}")
    print(f"ratio_of_ratios={ratio_of_ratios:.12f}")
    print("decision=STRESS_MODE_SPECIFIC_DURABILITY_REQUIRED")
    print("checks=PASS")


if __name__ == "__main__":
    main()
