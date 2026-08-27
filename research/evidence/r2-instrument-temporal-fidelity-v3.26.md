# Evidence note — R2 instrument temporal fidelity v3.26

## Established evidence

Checked 2026-08-27:

- NIST fast-pulse calibration work treats sampler step response, timebase error, deconvolution, and response uncertainty as measurement-system quantities that require calibration/characterization.
- NIST pulse-parameter guidance states that accurate step/pulse measurements depend on calibrated measurement-system variables.
- NIST 2024 digitizer work explicitly studies input-filter setting and digitization aperture as configuration variables.

Primary references:
- https://www.nist.gov/publications/fast-pulse-oscilloscope-calibration-system-1
- https://www.nist.gov/publications/measuring-response-high-speed-pulse-generators-and-samplers
- https://www.nist.gov/publications/digitizer-linearity-measurement-josephson-arbitrary-waveform-synthesizer

These support the general metrology principle only.

## Engineering assumptions

- The open v3.25 pointwise settling envelope of 69.5369142 uV is used as a parent budget pending review/merge.
- 20% of that envelope, 13.9073828 uV, is provisionally allocated to electrical acquisition-chain temporal error.
- Six repeated electrical steps are an operational minimum, not a standards-derived sample-size theorem.
- `|mean residual| + 1.959964 u` is an engineering upper envelope, not a general exact 95% confidence procedure for arbitrary correlated waveform noise.

## Synthetic/model result

For a synthetic first-order 100 mV step response, `t_min=tau ln(A/V_inst)` gives 0.3636–14.5421 s as tau ranges 0.05–2 s. These are planning calculations, not measured instrument performance.

## Falsifiable hypothesis

The exact configured R2 electrical acquisition chain has a directly measured residual response that enters and remains inside its allocated temporal-error envelope before the dwell used for optical/DUT acquisition.

## Conventional explanation / discriminator

Apparent DUT/source settling can arise from fixed-bandwidth filtering, aperture averaging, trigger/timestamp skew, autorange, compliance transitions, or firmware buffering. The discriminator is an electrical reference step through the same acquisition path with source/DUT temporal physics bypassed.

## Claim boundary

A v3.26 PASS is acquisition-chain evidence only. It does not establish R2 device behavior, source settling, recombination mechanism, EPC, or open-quantum transport.
