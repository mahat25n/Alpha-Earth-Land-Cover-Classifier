"""Public monthly AlphaEarth sample explorer. No classifier fitting or annual fallback."""
import base64
import csv
import hashlib
import io
import json
import math
from collections import defaultdict
from datetime import date
from functools import lru_cache
from urllib.request import urlopen

ROOT = "gs://alphaearth_foundations_custom/custom_satellite_embedding/v1/"
BANDS = [f"A{i:02d}" for i in range(64)]
DATASETS = {
    "king_county_2025_monthly": ("King County: Jan-Jun 2025", "2025-01-01", "2025-07-01", 1),
    "meloland_california_2026_crop_cycles": ("Meloland: Nov 2025-May 2026 (15th to 15th)", "2025-11-15", "2026-05-15", 15),
}
GUIDE = "https://developers.google.com/earth-engine/guides/custom_embedding_samples_on_gcs_readme"


def public_text(uri):
    if not uri.startswith(ROOT):
        raise ValueError("Only Google's published custom-embedding bucket is supported.")
    url = "https://storage.googleapis.com/" + uri[5:]
    with urlopen(url, timeout=30) as response:
        return response.read().decode("utf-8")


def parse_manifest(dataset, text):
    if dataset not in DATASETS:
        raise ValueError("Unsupported monthly dataset.")
    grouped = defaultdict(list)
    seen = set()
    for uri in text.splitlines():
        uri = uri.strip()
        if not uri:
            continue
        if uri in seen:
            raise ValueError("Duplicate tile in source manifest.")
        seen.add(uri)
        prefix = ROOT + dataset + "/"
        if not uri.startswith(prefix):
            raise ValueError("Manifest contains a tile from another source.")
        parts = uri[len(prefix):].split("/")
        if len(parts) != 3 or parts[2] != "data.tiff":
            raise ValueError("Unexpected monthly tile path.")
        interval = parts[0].split("_")
        if len(interval) != 2:
            raise ValueError("Invalid interval.")
        start, end = [date.fromisoformat(f"{s[:4]}-{s[4:6]}-{s[6:]}") for s in interval]
        next_month = date(start.year + (start.month == 12), start.month % 12 + 1, start.day)
        if end != next_month or start.day != DATASETS[dataset][3]:
            raise ValueError("Source is not the documented monthly interval.")
        grouped[(start.isoformat(), end.isoformat())].append(uri)
    periods = sorted(grouped)
    _, first, last, _ = DATASETS[dataset]
    if len(periods) != 6 or periods[0][0] != first or periods[-1][1] != last:
        raise ValueError("Incomplete or changed monthly series; review source before use.")
    if any(a[1] != b[0] for a, b in zip(periods, periods[1:])):
        raise ValueError("Missing or overlapping monthly intervals.")
    return [(start, end, sorted(grouped[(start, end)])) for start, end in periods]


def validate_metadata(dataset, start, end, metadata):
    props = metadata["properties"]
    if (props["DATASET"], props["START_DATE"], props["END_DATE"]) != (dataset, start, end):
        raise ValueError("Tile dates or dataset disagree with source manifest.")
    bands = metadata["bands"]
    if [b["id"] for b in bands] != BANDS or [b["tileset_band_index"] for b in bands] != list(range(64)):
        raise ValueError("Unexpected embedding band order.")
    version = tuple(str(props[k]) for k in
                    ("MODEL_VERSION", "DATASET_VERSION", "PROCESSING_SOFTWARE_VERSION"))
    if any(not v for v in version):
        raise ValueError("Missing source version.")
    return version


@lru_cache(maxsize=2)
def catalogue(dataset):
    text = public_text(ROOT + dataset + "/manifest.txt")
    periods = parse_manifest(dataset, text)
    versions = set()
    for start, end, uris in periods:
        for uri in uris:
            meta = json.loads(public_text(uri.rsplit("/", 1)[0] + "/image_manifest.json"))
            versions.add(validate_metadata(dataset, start, end, meta))
    if len(versions) != 1:
        raise ValueError("Mixed source/model versions; temporal comparison disabled.")
    return periods, next(iter(versions)), hashlib.sha256(text.encode()).hexdigest()


def decode_vector(raw):
    if len(raw) != 64:
        raise ValueError("Expected all 64 embedding bands.")
    if any(v is None or v == -128 for v in raw):
        return None
    if any(not math.isfinite(v) or v < -127 or v > 127 or int(v) != v for v in raw):
        raise ValueError("Expected raw signed-byte embeddings, not pre-decoded values.")
    # Google's published inverse quantization, applied only once.
    return [math.copysign((v / 127.5) ** 2, v) for v in raw]


def cosine(a, b):
    if a is None or b is None:
        return None
    aa = sum(x*x for x in a)
    bb = sum(x*x for x in b)
    if not aa or not bb:
        return None
    return max(-1.0, min(1.0, sum(x*y for x, y in zip(a, b)) / math.sqrt(aa*bb)))


def sample_series(dataset, longitude, latitude):
    if not math.isfinite(longitude) or not math.isfinite(latitude) or not (-180 <= longitude <= 180 and -90 <= latitude <= 90):
        raise ValueError("Invalid coordinates.")
    import ee
    periods, version, fingerprint = catalogue(dataset)
    point = ee.Geometry.Point([longitude, latitude])
    rows, vectors = [], []
    for start, end, uris in periods:
        images = []
        for uri in uris:
            raw = ee.Image.loadGeoTIFF(uri).select(list(range(64)), BANDS)
            # Mask the entire vector if any axis is nodata, before mosaicking.
            raw = raw.updateMask(raw.neq(-128).reduce(ee.Reducer.min()))
            images.append(raw)
        image = ee.ImageCollection.fromImages(images).mosaic()
        values = image.reduceRegion(
            reducer=ee.Reducer.first(), geometry=point, crs="EPSG:4326",
            scale=10, maxPixels=100, bestEffort=False
        ).getInfo()
        vector = decode_vector([values.get(b) for b in BANDS])
        vectors.append(vector)
        rows.append(dict(dataset=dataset, start_inclusive=start, end_exclusive=end,
                         longitude=longitude, latitude=latitude,
                         status="valid" if vector is not None else "outside coverage or masked",
                         model_version=version[0], dataset_version=version[1],
                         processing_version=version[2], manifest_sha256=fingerprint,
                         sampling_crs="EPSG:4326", sampling_scale_m=10,
                         source_tiles=json.dumps(uris)))
    # Baseline is always the first published interval, never a silently moved date.
    for i, row in enumerate(rows):
        similarity = cosine(vectors[0], vectors[i])
        previous = cosine(vectors[i-1], vectors[i]) if i else None
        row["cosine_to_first_interval"] = similarity
        row["cosine_to_previous_interval"] = previous
        row["distance_to_first_interval"] = None if similarity is None else 1 - similarity
        row.update(zip(BANDS, vectors[i] if vectors[i] is not None else [None]*64))
    return rows


def monthly_panel():
    import ipywidgets as widgets
    from IPython.display import display, HTML, clear_output
    dataset = widgets.Dropdown(options=[(v[0], k) for k, v in DATASETS.items()],
                               description="Dataset:", layout=widgets.Layout(width="95%"))
    lon = widgets.BoundedFloatText(value=-122.33, min=-180, max=180, description="Longitude:", continuous_update=True)
    lat = widgets.BoundedFloatText(value=47.60, min=-90, max=90, description="Latitude:", continuous_update=True)
    run = widgets.Button(description="Read monthly point", icon="calendar",
                         layout=widgets.Layout(width="200px"))
    output = widgets.Output()
    def choose(change):
        lon.value, lat.value = ((-122.33, 47.60) if dataset.value == "king_county_2025_monthly"
                               else (-115.43, 32.80))
        output.clear_output()
    dataset.observe(choose, names="value")
    def clicked(_):
        run.disabled = True
        with output:
            clear_output(wait=True)
            try:
                rows = sample_series(dataset.value, lon.value, lat.value)
                import pandas as pd
                frame = pd.DataFrame(rows)
                display(frame[["start_inclusive", "end_exclusive", "status",
                               "cosine_to_first_interval", "cosine_to_previous_interval"]])
                if not any(r["status"] == "valid" for r in rows):
                    print("No valid monthly pixels at this point. Choose a point inside the selected sample area.")
                elif rows[0]["status"] != "valid":
                    print("The first interval is missing here. Baseline comparisons remain blank.")
                else:
                    import matplotlib.pyplot as plt
                    fig, ax = plt.subplots(figsize=(9, 3.5), constrained_layout=True)
                    x = [r["start_inclusive"] for r in rows]
                    y = [r["distance_to_first_interval"] if r["distance_to_first_interval"] is not None
                         else float("nan") for r in rows]
                    ax.plot(x, y, "o-", color="black")
                    ax.set_ylabel("1 - cosine similarity")
                    ax.set_xlabel("Interval start (end dates shown above)")
                    ax.set_title("Embedding distance from first published interval")
                    ax.tick_params(axis="x", rotation=30)
                    display(fig)
                    plt.close(fig)
                payload = base64.b64encode(frame.to_csv(index=False).encode()).decode()
                display(HTML('<a download="monthly_alphaearth_point.csv" href="data:text/csv;base64,'
                             + payload + '">Download monthly point CSV</a>'))
            except Exception as exc:
                print("Monthly data could not be read: " + str(exc))
                print("No annual substitute or invented dates were used. Annual controls remain available.")
            finally:
                run.disabled = False
    run.on_click(clicked)
    intro = widgets.HTML(
        "<p>Published monthly samples only. Enter a point inside King County or Meloland. "
        "All six published intervals are retained; missing pixels stay blank. "
        "This uses all 64 embedding axes and does not fit classifiers or validate land-cover change. "
        "Monthly and annual model versions must not be compared directly.</p>"
        '<p><a href="' + GUIDE + '" target="_blank">Google sample coverage and dates</a></p>'
        "<p>Custom Satellite Embeddings from AlphaEarth Foundations are produced by Google and Google DeepMind. CC-BY 4.0.</p>"
    )
    panel = widgets.Accordion(children=[widgets.VBox([intro, dataset, widgets.HBox([lon, lat]), run, output])],
                              selected_index=None)
    panel.set_title(0, "Monthly AlphaEarth samples")
    return panel
