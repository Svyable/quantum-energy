# Synthetic weak-EL facility-export example

This directory is a **synthetic software-validation fixture**, not experimental R2 data and not a facility capability claim.

It deliberately uses 2 nm spectral bins so software must distinguish `photons/s/bin` from `photons/s/nm`. `background_counts` includes detector dark and optical stray/background under the same integration condition; calibrated signal is therefore `sample_counts - background_counts`. `dark_counts` is retained as a QC diagnostic and is **not subtracted a second time**.

The radiometric factor is emitted photons represented by one background-subtracted detector count for that channel, including the calibrated collection/detection chain. Real packages must replace every synthetic value with facility calibration data and uncertainty/provenance.
