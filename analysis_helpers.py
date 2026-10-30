"""Pure helpers for annual sampling exports and honest comparison labels."""
import hashlib
import json
import math
import re

REFERENCE_YEAR = 2020
REFERENCE_ASSET = 'ESA/WorldCover/v100/2020'


def geometry_cache_key(region_serialized, class_a, class_b, scale, count, seed, year):
    digest = hashlib.sha256(region_serialized.encode('utf-8')).hexdigest()
    return (digest, class_a, class_b, scale, count, seed, year, REFERENCE_ASSET)


def validate_bbox(bbox):
    values = list(map(float, bbox))
    if len(values) != 4 or not all(math.isfinite(v) for v in values):
        raise ValueError('Enter four finite longitude/latitude coordinates.')
    x0, y0, x1, y1 = values
    if not (-180 <= x0 < x1 <= 180 and -85 <= y0 < y1 <= 85):
        raise ValueError('Bounds must be longitude [-180, 180], latitude [-85, 85], with minimum below maximum.')
    return values


def annual_export_rows(samples):
    """Export every sampled class pair/year, once; never invent temporal detail."""
    rows = []
    for (year, class_a, class_b), df in sorted(samples.items()):
        bands = [c for c in df.columns if re.fullmatch(r'A\d{2}', c)]
        if set(bands) != {f'A{i:02d}' for i in range(64)}:
            raise ValueError('Expected the 64 official embedding bands A00-A63.')
        for record in df.to_dict('records'):
            if any(record.get(k) is None or not math.isfinite(float(record[k]))
                   for k in ('latitude', 'longitude')):
                raise ValueError('Sample coordinates missing; export stopped.')
            row = {k: record[k] for k in ('sample_id', 'latitude', 'longitude')}
            row.update(year=int(year), reference_year=REFERENCE_YEAR,
                       reference_asset=REFERENCE_ASSET, temporal_resolution='annual',
                       class_a=class_a, class_b=class_b,
                       land_cover_class=record['label'])
            row.update({band: record[band] for band in sorted(bands)})
            rows.append(row)
    return rows


def comparable_winners(rows):
    """Mark only highest observed scores within the same class pair and year.

    This is descriptive, not model selection or evidence of significance.
    Include ties and do not declare a winner for a lone model.
    """
    groups = {}
    for i, row in enumerate(rows):
        key = (row['Class A'], row['Class B'], row['Year'])
        groups.setdefault(key, []).append(i)
    winners = set()
    for indices in groups.values():
        if len(indices) > 1:
            best = max(rows[i]['Accuracy'] for i in indices)
            winners.update(i for i in indices if rows[i]['Accuracy'] == best)
    return winners
