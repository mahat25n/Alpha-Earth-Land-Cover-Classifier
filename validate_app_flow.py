"""Headless callback smoke test using the saved real benchmark sample.

Earth Engine still supplies the map layers. No new labels or synthetic observations.
This checks Python widget construction/callbacks, not browser rendering.
"""
import sys,json,base64,re,argparse
from pathlib import Path
from types import SimpleNamespace
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import ee
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'tests'))
from test_corrections import app_definitions
from analysis_helpers import geometry_cache_key

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--algorithm',default='all');args=parser.parse_args()
    ee.Initialize(project=None)
    ns=app_definitions();ns['EE_INITIALIZED']=True
    shown=[];ns['display']=lambda *items,**kwargs:shown.extend(items)
    ns['clear_output']=lambda **kwargs:None;plt.show=lambda:plt.close('all')
    app=ns['AlphaEarthApp'](None)
    app.country_dropdown.unobserve(app.on_country_changed,names='value')
    app.country_dropdown.value='Turkey'
    app.algorithm.value=args.algorithm;app.year_from_dropdown.value=2020;app.year_to_dropdown.value=2020
    app.n_samples.value=200;app.scale_m.value=500;app.test_size.value=25
    app.class_a.value=10;app.class_b.value=(40,)
    app.selected_bbox=[28.5,40.8,29.5,41.5]
    df=pd.read_csv(ROOT/'validation'/'benchmark_sample.csv')
    region=ee.Geometry.Rectangle(app.selected_bbox)
    feats=[ee.Feature(ee.Geometry.Point([r['longitude'],r['latitude']]),
                     {k:v for k,v in r.items() if k not in ['longitude','latitude','sample_id']})
           for r in df.to_dict('records')]
    fc=ee.FeatureCollection(feats);bands=[f'A{i:02d}' for i in range(64)]
    key=geometry_cache_key(region.serialize(),10,40,500,200,42,2020)
    app._ee_cache[key]=(df,bands,{'10':200,'40':200},400,fc)
    app.run_analysis(None)
    if 'Analysis completed!' not in app.status.value:raise RuntimeError(app.status.value)
    buttons=[]
    def walk(obj):
        if hasattr(obj,'description') and hasattr(obj,'click'):buttons.append(obj)
        for child in getattr(obj,'children',[]):walk(child)
    for obj in shown:walk(obj)
    annual=next(b for b in buttons if b.description=='Download Annual Samples')
    annual.click()
    htmls=[]
    def values(obj):
        if isinstance(getattr(obj,'value',None),str):htmls.append(obj.value)
        for child in getattr(obj,'children',[]):values(child)
    for obj in shown:values(obj)
    export=next(h for h in htmls if 'annual_samples.csv' in h)
    data=base64.b64decode(re.search(r'base64,([^"\s]+)',export).group(1))
    import io
    exported=pd.read_csv(io.BytesIO(data))
    assert len(exported)==400 and exported.reference_year.eq(2020).all()
    assert len(app.run_history)==(9 if args.algorithm=='all' else 1)
    result={'flow':'one real cached sample, nine-model batch, annual export callback',
            'algorithm':args.algorithm,'completed':True,'history_rows':len(app.run_history),'export_rows':len(exported),
            'browser_rendering_tested':False,'sheets_logging':False}
    (ROOT/'validation'/f'app_flow_{args.algorithm}.json').write_text(json.dumps(result,indent=2))
    print(json.dumps(result))

if __name__=='__main__':main()
