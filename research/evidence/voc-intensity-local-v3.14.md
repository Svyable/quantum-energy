# v3.14 evidence note — local ideality / curvature benchmark

## Primary external source

Wang et al., *Rethinking Charge Transport and Recombination in Donor-Diluted Organic Solar Cells*, Advanced Materials (2026), DOI `10.1002/adma.202523681`.

Public supporting dataset: Zenodo `10.5281/zenodo.20525023`, exact file `Figure S3 + Figure S16a.csv`, upstream MD5 `b430562c7fc5bbc6858553911efb8cc1`.

The dataset contains light-intensity-dependent `Voc` measurements and source-provided local recombination ideality factors for PM6:Y12 blends, including the 45% PM6 series used here. The article states that light-intensity- and temperature-dependent suns-`Voc` ideality factors are used in its DOS/recombination analysis and reports sub-unity ideality in higher-donor devices near higher illumination, with surface recombination discussed as one possible contributor.

## Established from this source

- `Voc(Phi)` is measurably curved in the 45% PM6 series; one global slope depends on the selected intensity window.
- The source itself provides a local ideality-factor series, making it an external benchmark for derivative extraction.
- Ideality factor is not mechanistically unique in this material system; transport, DOS, surface/contact recombination, and changing recombination regimes are all relevant.

## Internal cross-check result

On the 45% PM6 points from 0.05–2 suns, a 7-point local quadratic derivative in `ln(Phi)` reproduces the source-provided local series with approximately MAE 0.00394, RMSE 0.00682, maximum absolute difference 0.02339, and Pearson correlation 0.99866. A 9-point sensitivity fit gives MAE about 0.00679 and RMSE about 0.00889.

These are derived from public experimental plot data and are therefore **real-data estimator checks**, not new measurements by this project.

## Synthetic planning layer

A separate independent noise stress adds Gaussian `Voc` noise with `sigma=0.5 mV`, seed `20260826`, 5,000 repetitions. This uncertainty is not supplied by the source dataset and is explicitly a planning assumption. The stress tests smoothing sensitivity only.

## Claim boundary

Passing the benchmark supports using a local derivative estimator in R2. It does **not** establish interface recombination, energetic disorder, CT-state filling, EPC, or any open-quantum mechanism. Those mechanisms require the joint FTPS/EL/temperature/contact discriminator already defined by the program.