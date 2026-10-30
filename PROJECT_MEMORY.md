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

Remote verification completed successfully: GitHub Actions run 41108082271 on commit 31d7e795d11b3bddf791c45101d3c2ce0dcd2255. Seven safeguard tests passed, including exact preservation of the four pre-existing notebook cells and syntax compilation without execution. Live metadata checks covered all 30 tiles: 24 King County tiles and six Meloland tiles, each series six monthly periods, consistent versions (model 2.1, dataset 1.0, processing 1.02). Manifest SHA-256: King County 599437be7cc08f85ebefeb36441ff150e80a59be9aa0dfa3b15de897aa02e85f; Meloland 201a25ccf14191af9a4cbdc483b9e97032d4b3d289dcdc6b0cdc667a3b71d4be. No training, Earth Engine pixel extraction or browser launch was performed by these checks. Public app launch and monthly pixel retrieval remain unverified.


## Live monthly retrieval and public launch follow-up
On 30 October 2026, sample_series from published commit 31d7e795 ran against Earth Engine with the authorized saved project. Both example points returned six valid 64-axis monthly vectors and changing similarities. Exact summary results are in validation/monthly_live_retrieval.json. No classifier was fitted. The only functional correction was continuous_update=True for both monthly coordinate widgets (54bb21e7), matching the earlier annual input fix. The original main-branch Binder URL opened a fresh public JupyterLab notebook in Chrome on hub.gesis.mybinder.org; this was observed directly, not inferred from HTTP status. Earlier in-app-browser stream failures did not establish a repository build failure. Public notebook rendering is confirmed; interactive Earth Engine authentication and the complete monthly widget callback were not exercised in the fresh Binder session. Users must run notebook cells and authenticate their own Earth Engine account/project. Existing annual cells and Top 5 remained unchanged.
