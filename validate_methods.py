"""Fixed-sample comparison of all nine methods, without network access."""
import hashlib
import json
import sys
import subprocess
import warnings
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, GroupShuffleSplit
from sklearn.metrics import accuracy_score, roc_auc_score
from model_extensions import MODEL_LABELS, fit_checked

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT/'tests'))
from test_corrections import app_definitions
from validate_against_original import functions


def main():
    path = ROOT/'validation/benchmark_sample.csv'
    previous = json.loads((ROOT/'validation/comparison.json').read_text())
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    assert digest == previous['sample_sha256']
    df = pd.read_csv(path)
    X = df[[f'A{i:02d}' for i in range(64)]].to_numpy(float)
    y = df.label.map({10:0, 40:1}).to_numpy(int)
    assert X.shape == (400, 64) and np.isfinite(X).all()
    assert df.label.value_counts().to_dict() == {10:200, 40:200}
    train, test = train_test_split(np.arange(len(y)), test_size=.25, stratify=y, random_state=42)
    groups = pd.factorize(pd.Series(list(zip(np.floor(df.longitude/.1), np.floor(df.latitude/.1)))))[0]
    spatial_train, spatial_test = next(GroupShuffleSplit(n_splits=1, test_size=.25, random_state=42).split(X,y,groups))
    assert set(groups[spatial_train]).isdisjoint(groups[spatial_test])
    splits = {'random': (train,test), 'spatial': (spatial_train,spatial_test)}
    app = app_definitions()['AlphaEarthApp']
    baseline_notebook=json.loads(subprocess.check_output(['git','show','f22b4da:alpha_earth_app.ipynb'],cwd=ROOT).decode('utf-8'))
    baseline=functions('\n'.join(''.join(c['source']) for c in baseline_notebook['cells'] if c['cell_type']=='code'))
    rows=[]
    for setting, (tr,te) in splits.items():
        for key,label in MODEL_LABELS.items():
            print(setting, label, flush=True)
            model = app.build_model(None,key,42)
            with warnings.catch_warnings(record=True) as caught:
                warnings.simplefilter('always')
                fit_checked(model,X[tr],y[tr])
            if hasattr(model,'steps'):
                np.testing.assert_allclose(model.steps[0][1].mean_, X[tr].mean(axis=0))
            p = model.predict_proba(X[te])
            assert p.shape == (len(te),2) and np.isfinite(p).all()
            assert ((p>=0)&(p<=1)).all()
            np.testing.assert_allclose(p.sum(axis=1),1,atol=1e-6)
            prob=p[:,list(model.classes_).index(1)];pred=(prob>=.5).astype(int)
            accuracy=float(np.mean(pred==y[te]))
            pos=prob[y[te]==1][:,None];neg=prob[y[te]==0][None,:]
            auc=float(np.mean((pos>neg)+.5*(pos==neg)))
            assert abs(accuracy-accuracy_score(y[te],pred))<1e-12
            assert abs(auc-roc_auc_score(y[te],prob))<1e-12
            old=next((r for r in previous['results'] if r['algorithm']==key),None)
            if old:
                unchanged=fit_checked(baseline['build_model'](None,key,42),X[tr],y[tr])
                np.testing.assert_allclose(p,unchanged.predict_proba(X[te]),atol=1e-12,rtol=0)
                assert abs(accuracy-old[f'{setting}_accuracy'])<1e-12
                assert abs(auc-old[f'{setting}_auc'])<1e-12
            rows.append(dict(setting=setting,algorithm=key,label=label,accuracy=accuracy,auc=auc,
                             train=len(tr),test=len(te),probabilities=prob.tolist(),
                             warnings=[str(w.message) for w in caught]))
    import sklearn,catboost
    result=dict(scope='Bounded descriptive software comparison, not superiority evidence',
                sample_sha256=digest,sklearn=sklearn.__version__,catboost=catboost.__version__,
                splits={k:dict(train=a.tolist(),test=b.tolist()) for k,(a,b) in splits.items()},results=rows)
    (ROOT/'validation/method_comparison.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    pd.DataFrame([{k:v for k,v in r.items() if k not in ('probabilities','warnings')} for r in rows]).to_csv(ROOT/'validation/method_comparison.csv',index=False)
    print('All shared-sample, metric and legacy-score checks passed.')


if __name__=='__main__':main()
