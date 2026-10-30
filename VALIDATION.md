# Validation and reproduction

Install `requirements.txt` in a dedicated Python environment. Open `alpha_earth_app.ipynb` from this repository so `analysis_helpers.py` is importable. Use Run All. The app uses your saved Earth Engine project; alternatively set `EE_PROJECT_ID` to a project enabled for Earth Engine that your account can use. Do not commit credentials.

Run local checks:

```text
python -m unittest discover -s tests -v
```

To reproduce the original comparison, clone `https://github.com/FelipeBenavidesMz/Alpha-Earth-Land-Cover-Classifier`, check out `bdc4c4c8464ffa1cf4e20f37f91725d15ba9ba3b`, then run:

```text
python validate_against_original.py --original PATH_TO_ORIGINAL/alpha_earth_app.ipynb --project YOUR_PROJECT_ID
```

The settings were specified in `validation_plan.md` before fitting. `validation/benchmark_sample.csv` contains the complete returned sample for this bounded benchmark, not the full satellite dataset. `validation/comparison.json` records its hash, coverage, environment and results. All four original/corrected classifier pairs returned identical probabilities and labels in this environment. This confirms regression parity at this sample and specification; it is not an independent implementation of the estimators or proof of global equivalence.

The separate spatial holdout is a single-seed, within-region diagnostic using 0.1-degree groups. It has no buffer, no repeated folds, no independent ground truth and no publication-level uncertainty analysis. Do not present it as cross-region validation or select the best model from these scores.

`validate_app_flow.py` exercises the nine-model widget callback flow and annual export using the saved sample and live map requests. It does not test browser rendering. It uses saved authentication and leaves Sheets logging disabled.

Data sources: Google's annual Satellite Embedding collection and ESA WorldCover v100/2020. The AlphaEarth Foundations Satellite Embedding dataset is produced by Google and Google DeepMind. WorldCover attribution: ESA WorldCover project 2020 (v100). The CSV retains all 64 embedding bands, reference label, sample ID and coordinates. Labels 10 and 40 represent tree cover and cropland in this benchmark. Source labels are classified reference data, not independently observed ground truth.

No improvement in predictive accuracy, speed, usability or scientific interpretation has been established. The verified gains are corrections of specific software/measurement defects. Publication-level claims require a broader pre-specified evaluation and the license/provenance checks in `review/CONTRIBUTION.md`.

The additional-method comparison is reproduced with `python validate_methods.py`. It verifies the saved sample hash, identical split indices, training-only scaling, independently calculated metrics and probability parity for the original models against commit f22b4da. It requires that commit in the local Git history. See validation/METHOD_RESULTS.md for scope and results.
