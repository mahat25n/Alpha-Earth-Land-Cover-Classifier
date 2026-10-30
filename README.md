# Alpha-Earth-Land-Cover-Classifier

Interact with Google AlphaEarth Embeddings to Classify Land Covers

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/mahat25n/Alpha-Earth-Land-Cover-Classifier/main?labpath=alpha_earth_app.ipynb)

---

## Correctness update, 30 October 2026

This extension preserves the original classifiers and adds batch analysis, boundary inputs and exports. It does not retrain or improve the AlphaEarth foundation model.

The corrections repair polygon caching and CRS handling, retain exact drawn boundaries, preserve official band identifiers, and remove invented monthly/daily repetition. Every year still uses **ESA WorldCover 2020** as a fixed reference. A later-year score measures agreement with those reference labels, not verified land-cover change. Random-pixel holdout scores do not establish geographic transfer, and separate yearly fits are not cross-year transfer tests. Feature importance is model-dependent, not a physical interpretation or a causal effect.

Google Sheets logging is off by default. Existing logging can be enabled explicitly with `ENABLE_SHEETS_LOGGING=1` and configured credentials; it sends run metadata to the configured sheet. Do not enable it without reviewing the destination.

Tests: `python -m unittest discover -s tests -v`. See [validation instructions](VALIDATION.md), [corrections](CHANGELOG.md) and [publication assessment](review/CONTRIBUTION.md). The real-data comparison found prediction parity on a bounded benchmark, not improved accuracy. Previously exported monthly/daily CSVs and one-based band names must not be reused as measured data or official identifiers.

## Original Project Description

This app uses **Google AlphaEarth satellite embeddings** ([`GOOGLE/SATELLITE_EMBEDDING/V1/ANNUAL`](https://developers.google.com/earth-engine/datasets/catalog/GOOGLE_SATELLITE_EMBEDDING_V1_ANNUAL)) together with the ESA WorldCover land cover map to classify pairs of land cover classes using machine learning. Users draw a region of interest on an interactive map, select two land cover classes, choose a classifier, and run the analysis. The app samples Earth Engine pixels, trains a model, and visualizes the most discriminative embedding dimensions.

Created by **Felipe Benavides**, SDS Lab, Northeastern University and Gulf of Maine Research Institute.
`pipeben@gmail.com`

---

## Extended By

**Mahat Maalim Ibrahim**
School of Business, Department of Economics
Ibn Haldun University, Istanbul, Turkey
`mahatibrahim@ihu.edu.tr` | `mahatmaalimibrahim@gmail.com`

---

## Extended Version - New Features

This repository extends the original app with the following improvements:

### Region Selection
- **Precise coordinate input** - Min Lon, Min Lat, Max Lon, Max Lat text boxes with an Apply button let users type exact bounding box coordinates instead of drawing
- **Location search box** - Type any place name and click Go to recenter the map using geopy geocoding
- **Polygon and rectangle drawing tools** - Both shape types are enabled on the interactive ipyleaflet map
- **Auto-fill coordinates when drawing** - After drawing a rectangle or polygon, the coordinate input boxes are automatically populated with the shape's bounding box
- **Map auto-centers on country selection** - Choosing a country from the dropdown geocodes it and recenters the map to that country
- **Full country list** - Dropdown covers all 195 UN-recognized countries in alphabetical order

### Algorithm and Year Settings
- **Download top N embeddings** - Dropdown to show the top 3, 5, or 10 most important embeddings on the results map
- **Year range 2017-2024** - Year From and Year To dropdowns cover the full AlphaEarth dataset availability (2017-2024), allowing single-year or multi-year runs against a fixed 2020 reference
- **Multi-algorithm mode** - An "All Algorithms" option runs Random Forest, Gradient Boosting, XGBoost, LightGBM, Logistic Regression, Support Vector Machine, K-Nearest Neighbours, CatBoost and a small Neural Network on the same data and split in one click
- **Samples/class slider** - Maximum increased from 300 to 5000 (step 100, default 100)
- **Scale (m) slider** - Range 100-2000 m, step 100, default 500

### Results and Comparison
- **Year x Algorithm comparison table** - When multiple years or algorithms are selected, a styled HTML table summarises Accuracy, ROC AUC, Precision, Recall, F1, and Top Embedding for every combination
- **Best model highlight** - The highest observed score is marked only among algorithms for the same class pair and year; ties are retained. This is descriptive, not a significance test or model-selection procedure
- **Visual comparison chart** - Two matplotlib subplots (Accuracy and ROC AUC) are rendered as grouped bar charts after the comparison table
- **Download comparison table as CSV** - A one-click button exports all comparison rows to a CSV file
- **Multi-select Class B** - Users can hold Ctrl (Windows/Linux) or Cmd (Mac) to select multiple Class B classes; all combinations run automatically and appear in the comparison table with a dynamic title showing the actual classes, years, and algorithm selected
- **Temporal embedding importance chart** - A line chart showing how the top 5 embedding importances change across selected years, with one colored line per embedding and a Download PNG button
- **Download charts as PNG** - Each comparison chart (Accuracy, ROC AUC, and temporal embedding) has a Download PNG button that exports the figure at 300 dpi
- **Download embedding PNGs** - A button exports each of the top N embedding layers as a publication-ready PNG map with the same color palette shown on the folium map, a colorbar, and the embedding name and importance percentage in the title

### Annual Sample Download
- Export all sampled class pairs and years, including a single-year run.
- Each row contains a sample ID, coordinates, embedding year, fixed reference year and asset, class-pair codes, label and the official A00-A63 bands.
- Values describe annual composites. Monthly and daily duplication has been removed.
- Sampling is separate for each year and class pair. This export is not a balanced panel of identical pixels across years. Repeated pixels across comparisons are not independent observations.

### Quality of Life
- **Session results history table** - Every run in the current session is appended to a summary table showing time, year, classes, algorithm, accuracy, ROC AUC, and top embedding
- **EE data caching** - Samples are keyed by exact serialized geometry, class pair, scale, count, seed, year and reference asset; different polygons with the same bounds cannot share a cache entry
- **Visible warnings** - Global warning suppression has been removed so numerical and dependency warnings remain visible
- **Lazy loading** - geopy, xgboost, and lightgbm are imported only when first used, reducing startup time
- **Clean app header** - Instructions updated to reflect all new features

---

## How to Use

1. **Open the notebook** - Click the Binder badge above, or open `alpha_earth_app.ipynb` in a Jupyter environment with Earth Engine authenticated.

2. **Authenticate Earth Engine** - The notebook uses your saved Earth Engine project, or `EE_PROJECT_ID` / `GOOGLE_CLOUD_PROJECT` if set. Follow the authentication prompt if needed. Use an Earth Engine-enabled project you can access; the original developer's project is no longer hard-coded.

3. **Select your country** - Choose the country you are currently in from the dropdown. The map will automatically recenter to that country.

4. **Define your region of interest** - Either:
   - Use the rectangle or polygon drawing tool on the map, or
   - Type a location name in the search box and click **Go**, then draw, or
   - Enter coordinates directly in the Min Lon / Min Lat / Max Lon / Max Lat boxes and click **Apply**

5. **Choose land cover classes** - Select Class A and Class B from the ESA WorldCover class list. The app classifies pixels belonging to these two classes.

6. **Configure algorithm settings**:
   - *Algorithm* - Pick a single classifier (Random Forest, Gradient Boosting, XGBoost, or LightGBM) or select **All Algorithms** to compare all four
   - *Year From / Year To* - Set a single year or a range (2017-2024)
   - *Show top N* - Choose how many embedding layers to display on the results map (3, 5, or 10)
   - *Temporal Res* - Select Yearly, Monthly, or Daily for the time series export (optional)

7. **Run the analysis** - Click **RUN ANALYSIS**. A progress bar tracks sampling, training, and map generation.

8. **Explore results**:
   - The folium results map shows land cover pixels and the top-N embedding layers with colorbars
   - If multiple years or algorithms were selected, a comparison table and chart appear first
   - Accuracy, ROC AUC, per-class Precision/Recall/F1, confusion matrix, and embedding importance bar chart are displayed below the map

9. **Download outputs**:
   - **Download Top N Embedding Rasters** - Generates GeoTIFF download links via Earth Engine
   - **Download CSV** - Exports all 64 embedding importances for the primary run
   - **Download Comparison Table as CSV** - Exports the year x algorithm comparison table (visible in multi-mode)
   - **Download Annual Samples** - Exports every sampled class pair/year with coordinates and annual A00-A63 values.

10. **Provide feedback** - Use the feedback section at the bottom to share your experience with the AlphaEarth embeddings.

---

## Citation

### Original Project

Benavides, F. (2025). AlphaEarth Foundation Model for Land Cover Classification App.
SDS Lab, Northeastern University and Gulf of Maine Research Institute.
*Zenodo*. https://doi.org/10.5281/zenodo.16911104

If you use this app or build upon it, please also cite the Google AlphaEarth embeddings dataset:

```
Google (2024). Satellite Embedding V1 Annual.
Google Earth Engine Data Catalog.
https://developers.google.com/earth-engine/datasets/catalog/GOOGLE_SATELLITE_EMBEDDING_V1_ANNUAL
```

### This Extended Version

```
Ibrahim, M.M. (2025). Extended Alpha-Earth Land Cover Classifier.
GitHub. https://github.com/mahat25n/Alpha-Earth-Land-Cover-Classifier
ORCID: https://orcid.org/0000-0001-8450-7551
```

---

## Requirements

- Google Earth Engine account (free for research)
- Tested with Python 3.10; dependency compatibility must be checked for other versions
- Key packages: `earthengine-api`, `ipyleaflet`, `ipywidgets`, `folium`, `scikit-learn`, `xgboost`, `lightgbm`, `catboost`, `geopy`, `gspread`, `google-auth`

Install the dependencies before launch: `python -m pip install -r requirements.txt`. Optional classifier/geocoder imports retain their existing fallback installation behaviour.

## Additional methods

All Algorithms now runs nine methods. The original four specifications are unchanged. StandardScaler is fitted inside a training-only pipeline for logistic regression, SVM, KNN and the neural network. CatBoost uses the original embedding values. All models use the same sample, split, seed and probability threshold; fixed parameters are documented in `validation/method_extension_plan.md`. These are baseline specifications, not equally tuned models.

Tree models retain native importance. Other models use training permutation accuracy drops, with negative drops set to zero and positive drops normalized for the existing percentage maps. This display is descriptive and is not holdout validation, physical interpretation or a common scale across methods. Importance CSVs identify the method. The temporal importance chart follows the first model/class pair rather than averaging incompatible importance measures. See the [scikit-learn permutation documentation](https://scikit-learn.org/stable/modules/permutation_importance.html) and [CatBoost API](https://catboost.ai/docs/en/concepts/python-reference_catboostclassifier).

A convergence warning stops the run; a non-converged result is not accepted. Install CatBoost from requirements.txt before using CatBoost or All Algorithms. More methods increase runtime, especially kernel SVM and permutation displays at large sample settings. Large-region performance has not been benchmarked.

Run `python validate_methods.py` for the saved-sample comparison and `python validate_app_flow.py` for the nine-model callback/export test. The latter requires Earth Engine access. An individual method can be checked with `--algorithm lr`, `svm`, `knn`, `cat` or `mlp`. Scores and exact shared row indices are saved in `validation/method_comparison.json`; the CSV contains the comparison table. These bounded results do not establish general superiority.
