# Bounded validation plan, 30 October 2026

Written before downloading benchmark samples or fitting classifiers. This is a software regression benchmark, not a publication result or global accuracy study.

Original upstream commit: bdc4c4c8464ffa1cf4e20f37f91725d15ba9ba3b. User baseline: 55bb25cb6af20eab28d28fa1ae2760f4e28f27f0.

Use rectangle [28.5, 40.8, 29.5, 41.5], annual embedding 2020, WorldCover2020 classes 10 (trees) and 40 (cropland), 200 requested points per class, 500m sampling scale, seed 42. Compare original and corrected requests for identical feature/label rows. Record requested and returned counts and any missing observations. No sample substitution if this fails.

Run the original and corrected RF, gradient boosting, XGBoost and LightGBM builders on exactly the same stratified 25% holdout and seed. Require absolute prediction-probability differences <= 1e-12 and identical predicted labels. This checks regression parity; it cannot show improved real-world accuracy or independently validate the algorithms.

Also run a separately labelled geographic-block holdout using 0.1-degree blocks with GroupShuffleSplit(test_size=.25, random_state=42). Record block counts and class coverage. This one-region, one-seed diagnostic is not a geographic generalization result. Do not select models or publish superiority from these scores.

No monthly/daily observations, new labels, or unverified claims of land-cover change. Literature and scientific publication decision remain separate from code correctness.
