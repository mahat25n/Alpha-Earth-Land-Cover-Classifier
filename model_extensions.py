"""Additional fixed-specification classifiers; no test-set tuning."""
import warnings
import numpy as np
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.exceptions import ConvergenceWarning
from sklearn.inspection import permutation_importance

MODEL_LABELS = {
    'rf': 'Random Forest', 'gbt': 'Gradient Boosting',
    'xgb': 'XGBoost', 'lgb': 'LightGBM',
    'lr': 'Logistic Regression', 'svm': 'Support Vector Machine',
    'knn': 'K-Nearest Neighbours', 'cat': 'CatBoost', 'mlp': 'Neural Network',
}
NEW_MODELS = ('lr', 'svm', 'knn', 'cat', 'mlp')


def build_extension(name, seed=42):
    if name == 'cat':
        try:
            from catboost import CatBoostClassifier
        except ImportError as exc:
            raise ImportError('Install catboost from requirements.txt to use CatBoost or All Algorithms.') from exc
        return CatBoostClassifier(iterations=300, depth=6, learning_rate=0.1,
                                  loss_function='Logloss', random_seed=seed,
                                  verbose=False, allow_writing_files=False, thread_count=1)
    choices = {
        'lr': lambda: LogisticRegression(C=1.0, solver='lbfgs', max_iter=2000, random_state=seed),
        'svm': lambda: SVC(C=1.0, kernel='rbf', gamma='scale', probability=True, random_state=seed),
        'knn': lambda: KNeighborsClassifier(n_neighbors=5, weights='uniform', n_jobs=1),
        'mlp': lambda: MLPClassifier(hidden_layer_sizes=(64, 32), solver='lbfgs',
                                    alpha=0.0001, max_iter=2000, max_fun=50000, random_state=seed),
    }
    if name not in choices:
        raise ValueError(f'Unknown extension: {name}')
    return make_pipeline(StandardScaler(), choices[name]())


def fit_checked(model, X, y):
    # A non-converged optimizer is an error, not an accepted result.
    with warnings.catch_warnings():
        warnings.simplefilter('error', ConvergenceWarning)
        model.fit(X, y)
    estimator = model.steps[-1][1] if hasattr(model, 'steps') else model
    if getattr(estimator, 'fit_status_', 0) != 0:
        raise RuntimeError('Classifier did not converge; results were not accepted.')
    return model


def display_importances(model, X_train, y_train, seed=42):
    """Retain native importance; otherwise label training permutation explicitly.

    Positive permutation drops are normalized only for existing percentage maps.
    They are descriptive, not holdout evidence or physical interpretation.
    """
    if hasattr(model, 'feature_importances_'):
        return np.asarray(model.feature_importances_, dtype=float), 'native model importance'
    values = permutation_importance(model, X_train, y_train, scoring='accuracy',
                                    n_repeats=5, random_state=seed, n_jobs=1).importances_mean
    return np.maximum(values, 0), 'training permutation accuracy drop; positive values only'
