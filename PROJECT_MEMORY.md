# Project record: 30 October 2026

Authorized scope: correct the user's AlphaEarth extension, preserve useful features, compare against the original, assess the publication claim and commit. No claimed improvement without evidence.

User baseline: 55bb25cb6af20eab28d28fa1ae2760f4e28f27f0. Original comparison: FelipeBenavidesMz/Alpha-Earth-Land-Cover-Classifier at bdc4c4c8464ffa1cf4e20f37f91725d15ba9ba3b. Corrections are listed in CHANGELOG.md.

Earth Engine access succeeded using the user's project. Credentials were not included. Google Sheets logging was disabled throughout testing.

The complete returned benchmark has 400 rows, 64 embedding features and no missing rows. Its settings were recorded before fitting in validation_plan.md. Original and corrected predictions match for all four classifiers. Results, sample hash and environment are in validation/comparison.json. The app callback and annual export test completed; browser rendering was not tested. Regression tests cover geometry, CRS, caching, exports, identifiers, comparison grouping and widgets.

Do not reuse older monthly/daily exports as observations, or older A01-A64 labels as official band identifiers. Annual comparisons retain a fixed 2020 reference and do not measure verified change. Model and history comparisons corrected here do not change the original estimator definitions.

Scientific contribution remains not yet determined. Literature coverage, source overlap, license questions and required validation are in review/CONTRIBUTION.md. Outstanding: forward-citation audit, multi-region scientific evaluation, repeated spatial inference, independent references, frontend rendering, deployment and applicable license for later upstream revisions. No complete scientific acceptance/rejection gate has been claimed.

## Nine-method extension

User authorized adding logistic regression, SVM, KNN, CatBoost and a small neural network, preserving features and committing after tests. The specification was written before fitting in validation/method_extension_plan.md. All 400 saved benchmark rows were used and verified against the prior SHA-256. Every method received the same saved random and spatial split indices. Scaling used training rows only, with no tuning from these results. Predictions for the four existing methods were checked against commit f22b4da.

The nine-model scores are descriptive and saved in method_comparison.json/CSV. Numerical metric calculations were independently checked, but this is not independent reimplementation of every estimator or scientific superiority evidence. Seventeen unit/regression checks cover the existing functions, new methods, separable positive control, scaler and convergence guard. UI callback results are in validation/app_flow_*.json; browser rendering is not covered.

Native and training-permutation importance must not be averaged or compared as a common measure. The temporal importance chart now follows the first model/class pair. CSV exports retain the method name. GitHub authentication failed on the earlier push; a local commit is not an online deployment.


## 30 October 2026: bounded monthly extension
User authorized genuine supported subannual data only. Scope: add two official public monthly point series, preserve every existing annual notebook cell, no daily fabrication, no classifier reruns. Complete source manifests inspected: King County 24 tiles across six intervals; Meloland six tiles across six mid-month intervals. Google manifests and inverse-quantization example are authoritative. New module validates intervals, source identities, 64-band order and consistent model/data versions. Missing periods/pixels do not become annual substitutes. Temporal comparisons use all axes and the fixed first interval; exported provenance retains source tiles, versions and manifest hash. Monthly observations are not verified land-cover changes and are never scored against the 2020 labels. Remote CI covers arithmetic, metadata and preservation without fitting any model. Earth Engine pixel extraction, browser display and public Binder launch remain unverified in this addition. No browser opened; no local app or models run.
