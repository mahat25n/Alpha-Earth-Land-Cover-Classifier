import unittest
import warnings
import numpy as np
from sklearn.exceptions import ConvergenceWarning
from model_extensions import MODEL_LABELS, NEW_MODELS, build_extension, fit_checked, display_importances
from test_corrections import app_definitions


class AdditionalMethods(unittest.TestCase):
    def test_all_nine_are_selectable(self):
        app=app_definitions()['AlphaEarthApp'](None)
        self.assertEqual({v for _,v in app.algorithm.options},set(MODEL_LABELS)|{'all'})

    def test_known_separable_control_and_training_scaler(self):
        rng=np.random.RandomState(13)
        y=np.repeat([0,1],40)
        X=rng.normal(0,.1,(80,64))+(2*y[:,None]-1)
        for name in NEW_MODELS:
            with self.subTest(name=name):
                model=fit_checked(build_extension(name),X,y)
                self.assertGreater(np.mean((model.predict_proba(X)[:,1]>=.5)==y),.95)
                if hasattr(model,'steps'):
                    np.testing.assert_allclose(model.steps[0][1].mean_,X.mean(axis=0))
                imp,label=display_importances(model,X,y)
                self.assertEqual(imp.shape,(64,))
                self.assertTrue(np.isfinite(imp).all() and (imp>=0).all())
                self.assertIn('importance' if name=='cat' else 'training permutation',label)

    def test_nonconvergence_is_not_accepted(self):
        class Bad:
            def fit(self,X,y): warnings.warn('no convergence',ConvergenceWarning)
        with self.assertRaises(ConvergenceWarning):fit_checked(Bad(),[[1]],[0])

    def test_unknown_model_rejected(self):
        with self.assertRaises(ValueError):build_extension('unknown')
