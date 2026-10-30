import ast
import json
import sys
import types
import unittest
import tempfile
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from analysis_helpers import annual_export_rows, comparable_winners, geometry_cache_key, validate_bbox

def notebook_source(path=ROOT/'alpha_earth_app.ipynb'):
    nb=json.loads(path.read_text(encoding='utf-8'))
    return '\n'.join(''.join(c['source']) if isinstance(c['source'],list) else c['source']
                     for c in nb['cells'] if c['cell_type']=='code')

def isolated(name, namespace=None, source=None):
    tree=ast.parse(source or notebook_source())
    f=next(n for n in ast.walk(tree) if isinstance(n,ast.FunctionDef) and n.name==name)
    ns={} if namespace is None else namespace
    exec(compile(ast.Module(body=[f],type_ignores=[]),'<isolated notebook function>','exec'),ns)
    return ns[name]

def app_definitions():
    # Load code definitions and imports, never authentication/install/logging blocks.
    tree=ast.parse(notebook_source())
    nodes=[n for n in tree.body if isinstance(n,(ast.Import,ast.ImportFrom,ast.FunctionDef,ast.ClassDef,ast.Assign))]
    ns={}
    exec(compile(ast.Module(body=nodes,type_ignores=[]),'<notebook definitions>','exec'),ns)
    ns['setup_google_sheets']=lambda:None
    return ns

class Corrections(unittest.TestCase):
    def test_notebook_parses_and_outputs_cleared(self):
        ast.parse(notebook_source())
        nb=json.loads((ROOT/'alpha_earth_app.ipynb').read_text(encoding='utf-8'))
        self.assertTrue(all(not c.get('outputs') for c in nb['cells']))

    def test_cache_distinguishes_shapes_same_bounds(self):
        a=geometry_cache_key('{"triangle":1}',10,20,500,100,42,2020)
        b=geometry_cache_key('{"rectangle":1}',10,20,500,100,42,2020)
        self.assertNotEqual(a,b)
        self.assertEqual(a,geometry_cache_key('{"triangle":1}',10,20,500,100,42,2020))

    def test_cache_method_does_not_return_other_geometry(self):
        class Region:
            def serialize(self): return 'new polygon'
        oldkey=geometry_cache_key('old polygon',10,20,500,100,42,2020)
        obj=types.SimpleNamespace(_ee_cache={oldkey:'wrong data'},_cache_msg_printed=True)
        def stop(year): raise RuntimeError('new sampling requested')
        method=isolated('ee_pairwise_sample_with_others',{'geometry_cache_key':geometry_cache_key,'load_stack':stop})
        with self.assertRaisesRegex(RuntimeError,'new sampling requested'):
            method(obj,10,20,year=2020,region=Region(),scale_m=500,n_per_class=100,seed=42)

    def test_all_pairs_export_without_temporal_duplication(self):
        record={f'A{i:02d}':i/100 for i in range(64)}
        record.update(sample_id='p',latitude=40.,longitude=29.,label=10)
        frame=pd.DataFrame([record])
        samples={(2020,10,20):frame,(2021,10,20):frame,(2021,10,30):frame}
        rows=annual_export_rows(samples)
        self.assertEqual(len(rows),3)
        self.assertEqual({r['class_b'] for r in rows},{20,30})
        self.assertTrue(all(r['reference_year']==2020 and r['temporal_resolution']=='annual' for r in rows))
        self.assertTrue(all('month' not in r and 'date' not in r for r in rows))
        self.assertEqual(rows[0]['A00'],0.)

    def test_export_requires_official_bands(self):
        with self.assertRaises(ValueError): annual_export_rows({(2020,10,20):pd.DataFrame([{'A01':1}])})

    def test_export_rejects_nonfinite_coordinates(self):
        record={f'A{i:02d}':0.1 for i in range(64)}
        record.update(sample_id='p',latitude=float('nan'),longitude=29.,label=10)
        with self.assertRaises(ValueError):
            annual_export_rows({(2020,10,40):pd.DataFrame([record])})

    def test_comparison_never_crosses_tasks_and_keeps_ties(self):
        rows=[{'Class A':'a','Class B':b,'Year':y,'Accuracy':v} for b,y,v in
              [('b',2020,.8),('b',2020,.8),('b',2021,.95),('c',2020,.7),('c',2020,.9)]]
        self.assertEqual(comparable_winners(rows),{0,1,4})

    def test_bounds_reject_projected_and_nonfinite(self):
        for box in ([500000,4500000,510000,4510000],[0,0,float('nan'),1],[1,0,0,1]):
            with self.assertRaises(ValueError): validate_bbox(box)
        self.assertEqual(validate_bbox([28,40,29,41]),[28,40,29,41])

    def test_draw_preserves_polygon_and_replaces_upload(self):
        field=lambda:types.SimpleNamespace(value='')
        obj=types.SimpleNamespace(min_lon_input=field(),min_lat_input=field(),max_lon_input=field(),max_lat_input=field(),
            update_region_info=lambda:None,update_button_state=lambda _:None,upload_geojson={'old':1},upload_ee_geom='old')
        geom={'type':'Polygon','coordinates':[[[0,0],[1,0],[0,1],[0,0]]]}
        isolated('handle_draw',{'validate_bbox':validate_bbox})(obj,None,'created',{'geometry':geom})
        self.assertEqual(obj.drawn_geometry,geom)
        self.assertIsNone(obj.upload_geojson)
        self.assertIsNone(obj.upload_ee_geom)

    def test_display_preserves_official_band_ids(self):
        bands=[f'A{i:02d}' for i in range(64)]
        vals=np.arange(64,dtype=float)
        top=isolated('top_k_importance',{'np':np})(vals,bands)
        allvals=isolated('all_embedding_importance',{'np':np})(vals,bands)
        self.assertEqual(top[0][0],'A63')
        self.assertEqual([x[0] for x in allvals],bands)
        self.assertAlmostEqual(sum(x[1] for x in allvals),100.)

    def test_annual_only_controls_and_reference_notice(self):
        s=notebook_source()
        self.assertIn("options=['Yearly']",s)
        self.assertNotIn("_r2['month']",s)
        self.assertNotIn("_r2['date']",s)
        self.assertIn('fixed ESA WorldCover 2020 reference',s)

    def test_widgets_construct_and_manual_bounds_clear_geometry(self):
        ns=app_definitions();app=ns['AlphaEarthApp'](None)
        self.assertEqual(tuple(app.temporal_res_dropdown.options),('Yearly',))
        app.drawn_geometry={'old':1};app.upload_geojson={'old':1};app.upload_ee_geom='old'
        app.min_lon_input.value=28;app.min_lat_input.value=40
        app.max_lon_input.value=29;app.max_lat_input.value=41
        app.apply_bbox_from_inputs(object())
        self.assertEqual(app.selected_bbox,[28,40,29,41])
        self.assertIsNone(app.drawn_geometry);self.assertIsNone(app.upload_geojson)

    def test_projected_boundary_reprojected_before_bounds(self):
        import geopandas as gpd
        from shapely.geometry import box
        ns=app_definitions();app=ns['AlphaEarthApp'](None)
        ns['ee']=types.SimpleNamespace(Geometry=lambda x:x)
        app.selection_map=types.SimpleNamespace(add_layer=lambda _:None, remove_layer=lambda _:None,fit_bounds=lambda _:None)
        gdf=gpd.GeoDataFrame({'name':['test']},geometry=[box(28,40,29,41)],crs='EPSG:4326').to_crs('EPSG:3857')
        content=gdf.to_json().encode()
        app.handle_upload({'new':({'name':'test.geojson','content':content},)})
        self.assertIsNotNone(app.upload_geojson,app.upload_status.value)
        np.testing.assert_allclose(app.selected_bbox,[28,40,29,41],atol=1e-6)
        self.assertIsNotNone(app.upload_ee_geom)

if __name__=='__main__': unittest.main()
