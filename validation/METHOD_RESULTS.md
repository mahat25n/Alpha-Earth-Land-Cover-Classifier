# Additional-method verification

Added logistic regression, RBF support vector machine, five-neighbour KNN, CatBoost and a small neural network. All nine methods used the complete saved 400-row benchmark and identical saved split indices. Training-only scaling and convergence checks passed. The original four methods retained identical probabilities against the preceding commit.

The highest observed random-holdout accuracy was 97% among the added models and 96% among the existing models. On the spatial holdout, the highest added-model and existing-model accuracies were both 98.08%. These are descriptive results from one region and split, not evidence of general superiority.

Seventeen unit and regression tests passed. All nine models completed both benchmark splits, with independently checked accuracy and AUC calculations. The full app batch and individual added methods are checked through Python widget callbacks and live map requests; their completion records are in app_flow_*.json. Browser rendering and large-region performance remain unverified.

The saved CSV and JSON retain the full comparison, sample hash, exact row indices, probabilities and package versions. No data were resampled or discarded for this comparison. No paper or publication claim was changed.
