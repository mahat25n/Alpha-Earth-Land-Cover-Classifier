"""Real-data parity check. Downloads a bounded sample; never uploads or logs to Sheets."""
import argparse,ast,hashlib,json,platform,warnings
from pathlib import Path
from types import SimpleNamespace
import ee
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split,GroupShuffleSplit
from sklearn.ensemble import RandomForestClassifier,GradientBoostingClassifier
from sklearn.metrics import accuracy_score,roc_auc_score
import xgboost,lightgbm
from model_extensions import NEW_MODELS, build_extension
from analysis_helpers import geometry_cache_key,REFERENCE_ASSET

def source(path):
    n=json.loads(path.read_text(encoding='utf-8'))
    return '\n'.join(''.join(c['source']) if isinstance(c['source'],list) else c['source'] for c in n['cells'] if c['cell_type']=='code')

def functions(src):
    namespace=dict(NEW_MODELS=NEW_MODELS,build_extension=build_extension,ee=ee,np=np,pd=pd,geometry_cache_key=geometry_cache_key,REFERENCE_ASSET=REFERENCE_ASSET,
                   RandomForestClassifier=RandomForestClassifier,GradientBoostingClassifier=GradientBoostingClassifier,
                   _get_xgb=lambda:xgboost,_get_lgb=lambda:lightgbm)
    wanted={'load_stack','ee_pairwise_sample_with_others','build_model'}
    nodes=[n for n in ast.walk(ast.parse(src)) if isinstance(n,ast.FunctionDef) and n.name in wanted]
    exec(compile(ast.Module(body=nodes,type_ignores=[]),'<isolated comparison>','exec'),namespace)
    return namespace

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--original',type=Path,required=True);ap.add_argument('--project');args=ap.parse_args()
    ee.Initialize(project=args.project)
    root=Path(__file__).resolve().parent;out=root/'validation';out.mkdir(exist_ok=True)
    old=functions(source(args.original));new=functions(source(root/'alpha_earth_app.ipynb'))
    bbox=[28.5,40.8,29.5,41.5];region=ee.Geometry.Rectangle(bbox)
    kwargs=dict(year=2020,region=region,scale_m=500,n_per_class=200,seed=42)
    old_df,bands,old_hist,old_size,_=old['ee_pairwise_sample_with_others'](SimpleNamespace(),10,40,**kwargs)
    obj=SimpleNamespace(selected_bbox=bbox,_ee_cache={},_cache_msg_printed=False)
    df,new_bands,hist,size,_=new['ee_pairwise_sample_with_others'](obj,10,40,**kwargs)
    pd.testing.assert_frame_equal(old_df[bands+['label']],df[bands+['label']],check_dtype=False)
    assert bands==new_bands and hist==old_hist and size==old_size
    assert df[bands+['label','longitude','latitude']].notna().all().all()
    assert set(df.label)=={10,40}
    data=out/'benchmark_sample.csv';df.to_csv(data,index=False)
    X=df[bands].to_numpy(float);y=df.label.map({10:0,40:1}).to_numpy(int)
    train,test=train_test_split(np.arange(len(y)),test_size=.25,stratify=y,random_state=42)
    groups=list(zip(np.floor(df.longitude/.1).astype(int),np.floor(df.latitude/.1).astype(int)))
    group_ids=pd.factorize(pd.Series(groups))[0]
    spatial_train,spatial_test=next(GroupShuffleSplit(n_splits=1,test_size=.25,random_state=42).split(X,y,group_ids))
    assert set(group_ids[spatial_train]).isdisjoint(group_ids[spatial_test])
    records=[]
    for algorithm in ['rf','gbt','xgb','lgb']:
        print('Validating',algorithm,flush=True)
        a=old['build_model'](None,algorithm,42);b=new['build_model'](None,algorithm,42)
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter('always');a.fit(X[train],y[train]);b.fit(X[train],y[train])
            p=a.predict_proba(X[test])[:,1];q=b.predict_proba(X[test])[:,1]
        err=float(np.max(np.abs(p-q)));assert err<=1e-12
        assert np.array_equal(p>=.5,q>=.5)
        c=new['build_model'](None,algorithm,42)
        spatial={}
        if len(np.unique(y[spatial_train]))==2 and len(np.unique(y[spatial_test]))==2:
            c.fit(X[spatial_train],y[spatial_train]);sp=c.predict_proba(X[spatial_test])[:,1]
            spatial=dict(spatial_accuracy=accuracy_score(y[spatial_test],sp>=.5),spatial_auc=roc_auc_score(y[spatial_test],sp))
        records.append(dict(algorithm=algorithm,max_probability_difference=err,labels_identical=True,
            random_accuracy=accuracy_score(y[test],q>=.5),random_auc=roc_auc_score(y[test],q),
            warnings=[str(w.message) for w in caught],**spatial))
    result=dict(scope='One-region software parity benchmark; not an accuracy improvement claim',
        bbox=bbox,year=2020,reference_asset=REFERENCE_ASSET,requested_per_class=200,returned_histogram=hist,
        rows=len(df),missing_rows=0,feature_count=len(bands),sampling_scale_m=500,seed=42,
        train=len(train),test=len(test),spatial_train=len(spatial_train),spatial_test=len(spatial_test),
        spatial_train_blocks=len(set(group_ids[spatial_train])),spatial_test_blocks=len(set(group_ids[spatial_test])),
        sample_sha256=hashlib.sha256(data.read_bytes()).hexdigest(),python=platform.python_version(),
        numpy=np.__version__,pandas=pd.__version__,xgboost=xgboost.__version__,lightgbm=lightgbm.__version__,results=records)
    (out/'comparison.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
