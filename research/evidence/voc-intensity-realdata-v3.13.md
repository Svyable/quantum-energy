# Evidence record — v3.13 real-data `Voc`–intensity benchmark

## Primary publication

Chen Wang et al., **Rethinking Charge Transport and Recombination in Donor-Diluted Organic Solar Cells**, *Advanced Materials* (online 7 June 2026), DOI: `10.1002/adma.202523681`.

Primary URL: https://advanced.onlinelibrary.wiley.com/doi/10.1002/adma.202523681

Relevant evidence from the article:

- PM6:Y12 devices were measured over a wide donor-fraction range.
- light-intensity- and temperature-dependent suns-`Voc` measurements were used to evaluate recombination ideality factors / energetic-state behavior;
- the paper explicitly notes ideality factors below unity at high donor fraction and discusses surface recombination around one-sun conditions;
- the authors caution through their analysis, in effect, that transport/recombination interpretation depends on operating regime rather than a single universal slope.

## Primary public dataset

Zenodo dataset DOI: `10.5281/zenodo.20525023`, version v1.0, published June 2026.

Dataset URL: https://zenodo.org/records/20525023

The dataset description states that it contains the experimental data supporting the manuscript, including light-intensity-dependent measurements, JV, PL, time-resolved PL, X-ray, UPS, conductivity/mobility, EQE, TDCF, and related analysis, with figure data supplied as CSV.

Benchmark source file:

`Figure S3 + Figure S16a.csv`

Direct URL used by the executable:

https://zenodo.org/records/20525023/files/Figure%20S3%20%2B%20Figure%20S16a.csv?download=1

Zenodo-published MD5: `b430562c7fc5bbc6858553911efb8cc1`.

## Use in this repository

The upstream CSV is **not redistributed** in this repository. `models/voc_intensity_realdata_benchmark.py` downloads the source and verifies the published MD5 before calculation.

The benchmark uses the 45% PM6 light-intensity series to test the program's `Voc`-intensity ideality-factor extraction. The source also provides local `n_id` values, giving a useful external numerical comparator.

## Claim boundary

This evidence establishes a real public arithmetic/regression benchmark. It does not establish that an ideality-factor change uniquely identifies interface recombination in R2. H1 energetic disorder, H2 thickness/optical confounding, H3 interface/contact recombination, and H4 injection/state filling remain competing explanations in the R2 mechanism audit.
