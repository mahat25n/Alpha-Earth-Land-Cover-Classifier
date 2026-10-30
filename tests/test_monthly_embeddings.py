import json
import math
import subprocess
import unittest
from monthly_embeddings import BANDS, DATASETS, ROOT, parse_manifest, decode_vector, cosine, validate_metadata

class MonthlySafeguards(unittest.TestCase):
    def manifest(self, dataset="king_county_2025_monthly"):
        return "\n".join(ROOT + dataset + f"/2025{m:02d}01_2025{m+1:02d}01/tile/data.tiff"
                         for m in range(1, 7))

    def test_exact_six_intervals(self):
        periods = parse_manifest("king_county_2025_monthly", self.manifest())
        self.assertEqual(len(periods), 6)
        self.assertEqual(periods[0][:2], ("2025-01-01", "2025-02-01"))
        self.assertEqual(periods[-1][:2], ("2025-06-01", "2025-07-01"))

    def test_missing_duplicate_and_foreign_sources_rejected(self):
        source = self.manifest()
        for bad in ["\n".join(source.splitlines()[1:]), source+"\n"+source.splitlines()[0],
                    source.replace("gs://alphaearth_foundations_custom", "gs://another_bucket")]:
            with self.assertRaises(ValueError):
                parse_manifest("king_county_2025_monthly", bad)

    def test_daily_relabel_rejected(self):
        with self.assertRaises(ValueError):
            parse_manifest("king_county_2025_monthly", self.manifest().replace("20250101_20250201", "20250101_20250102"))

    def test_inverse_quantization(self):
        # Independent algebra: signed q*q divided by 127.5 squared.
        raw = [-127, -64, 0, 64, 127] + [1]*59
        result = decode_vector(raw)
        for q, actual in zip(raw, result):
            expected = q * abs(q) / 16256.25
            self.assertAlmostEqual(actual, expected, places=14)
        self.assertAlmostEqual(cosine(result, result), 1)
        self.assertAlmostEqual(cosine(result, [-x for x in result]), -1)

    def test_missing_and_invalid_vectors(self):
        self.assertIsNone(decode_vector([-128]+[1]*63))
        self.assertIsNone(decode_vector([None]+[1]*63))
        self.assertIsNone(cosine(None, [1]*64))
        self.assertIsNone(cosine([0]*64, [1]*64))
        for bad in [[1]*63, [128]+[1]*63, [float("nan")]+[1]*63, [0.5]+[1]*63]:
            with self.assertRaises(ValueError):
                decode_vector(bad)

    def test_metadata_order(self):
        meta = dict(properties=dict(DATASET="king_county_2025_monthly",
                    START_DATE="2025-01-01", END_DATE="2025-02-01",
                    MODEL_VERSION="2.1", DATASET_VERSION="1.0", PROCESSING_SOFTWARE_VERSION="1.02"),
                    bands=[dict(id=b, tileset_band_index=i) for i,b in enumerate(BANDS)])
        validate_metadata("king_county_2025_monthly", "2025-01-01", "2025-02-01", meta)
        meta["bands"].reverse()
        with self.assertRaises(ValueError):
            validate_metadata("king_county_2025_monthly", "2025-01-01", "2025-02-01", meta)

    def test_existing_notebook_preserved(self):
        baseline = json.loads(subprocess.check_output(["git", "show",
            "eff62226ac7cbaad15cb9fd3355c19629cf76d2f:alpha_earth_app.ipynb"], text=True))
        with open("alpha_earth_app.ipynb", encoding="utf-8") as f:
            current = json.load(f)
        self.assertEqual(current["cells"][:len(baseline["cells"])], baseline["cells"])
        self.assertEqual(len(current["cells"]), len(baseline["cells"])+1)
        source = "".join(current["cells"][2]["source"])
        self.assertIn("('Top 3', 3), ('Top 5', 5), ('Top 10', 10)", source)
        for cell in current["cells"]:
            if cell["cell_type"] == "code":
                compile("".join(cell["source"]), "<notebook>", "exec")

if __name__ == "__main__":
    unittest.main()
