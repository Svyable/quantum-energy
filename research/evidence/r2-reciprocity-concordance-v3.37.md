# Evidence record — R2 reciprocity concordance v3.37

Date: 2026-08-27

## Established/internal evidence

`technical/current-specification.md` on `main` already specifies an R2/AT-04 planning acceptance criterion of direct `EQE_EL` versus reciprocity-derived `Delta V_nr` agreement within 20 mV. The same file records `Delta V_nr = -(k_B T/q) ln(EQE_EL)` as the direct voltage-loss relation and requires injection control because weak-EL NFA systems can be carrier-density dependent.

`research/CALCULATION_VERIFICATION.md` requires correlated/systematic uncertainty to be separated from independent random terms, two calculation paths where practical, preserved statistical hierarchy, and visible negative results.

No new external empirical source, vendor capability, or measured R2 value is introduced in v3.37.

## Engineering assumption

The inherited 20 mV concordance window is treated as a project planning screen. v3.37 does not relabel it as a standards-derived equivalence criterion or confidence interval.

## Falsifiable metrology hypothesis

For a matched R2 observation acquired and analyzed under frozen comparable conditions, independently produced direct and reciprocity-derived `Delta V_nr` estimates can agree within the inherited 20 mV planning window while maintaining complete raw-data and analysis provenance.

## Synthetic/software verification only

The executable self-test uses arithmetic fixtures at 0, 20, and 20.000001 mV differences and uncertainty fixtures `(3,4) mV` and `(5,5) mV`. These values are not device measurements.

## Conventional/null explanations

A failure can be fully conventional: spectral truncation, low-signal tail bias, calibration error, temperature mismatch, injection/state filling, background subtraction, or mismatched analysis commits. A pass can also be misleading if shared calibration systematics drive both paths together.

The discriminator is prospective paired acquisition with independent analysis provenance and explicit shared-systematic correlation treatment.

## Claim boundary

A v3.37 `PASS` establishes only concordance of two metrology analysis paths for the tested configuration. It does not support a quantum-mechanism, EPC, performance, manufacturing, facility-equivalence, or commercial claim.
