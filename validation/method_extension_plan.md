# Additional classifier verification plan

Written before fitting the five added methods, 30 October 2026. Earlier four-model benchmark scores are already known. This is software verification, not a new scientific superiority test.

Use every row of the saved 400-record, 64-band benchmark. Verify its hash against comparison.json, finite values and class counts. Reuse seed 42, stratified 25% random holdout and the existing 0.1-degree group holdout. Save row indices once; all nine models receive identical training/test indices. No tuning on these results and no new data sampling.

Preserve the original four builders. Add standardized logistic regression (C=1, lbfgs, 2000 iterations), RBF SVC (C=1, gamma=scale, probability enabled), uniform five-neighbour KNN, CatBoost (300 trees, depth 6, learning rate 0.1), and a standardized 64/32-unit neural network (lbfgs, alpha=0.0001, 2000 iterations, 50000 function calls). Scaling is fit on training rows only. Seed stochastic methods at 42. Keep the existing probability >=0.5 prediction rule for all models. Treat convergence warnings as errors.

Check probability shape, finiteness and bounds; verify accuracy and AUC independently from labels and pairwise probability ranks. Compare original predictions before and after this change. Inspect scaler means against training means. Test all methods on a known separable synthetic fixture. Exercise the full batch and individual added-model widget callbacks, tables and annual export. Describe feature importance honestly: native model importance for trees; training permutation accuracy drops for methods without native importance. Their magnitudes are not comparable across methods.

Report both holdout settings descriptively. This bounded sample and single split cannot establish a generally superior algorithm. No causal, geographic-transfer, novelty or publication-readiness claim follows from these checks. Frontend rendering and large-region resource limits remain separate checks.
