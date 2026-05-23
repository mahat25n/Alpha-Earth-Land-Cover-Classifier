# Alpha-Earth-Land-Cover-Classifier

Interact with Google AlphaEarth Embeddings to Classify Land Covers

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/mahat25n/Alpha-Earth-Land-Cover-Classifier/main?labpath=alpha_earth_app.ipynb)

---

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
- **Year range 2017-2024** - Year From and Year To dropdowns cover the full AlphaEarth dataset availability (2017-2024), allowing single-year or multi-year runs
- **Multi-algorithm mode** - An "All Algorithms" option runs Random Forest, Gradient Boosting, XGBoost, and LightGBM on the same data in one click
- **Samples/class slider** - Maximum increased from 300 to 5000 (step 100, default 100)
- **Scale (m) slider** - Range 100-2000 m, step 100, default 500

### Results and Comparison
- **Year x Algorithm comparison table** - When multiple years or algorithms are selected, a styled HTML table summarises Accuracy, ROC AUC, Precision, Recall, F1, and Top Embedding for every combination
- **Best model highlight** - The row with the highest accuracy is marked with a star (Best) and highlighted in green
- **Visual comparison chart** - Two matplotlib subplots (Accuracy and ROC AUC) are rendered as grouped bar charts after the comparison table
- **Download comparison table as CSV** - A one-click button exports all comparison rows to a CSV file

### Time Series Download
- **Time series data export** - After a year-range run a Download Time Series Data button appears
- **Temporal resolution selector** - Choose Yearly, Monthly, or Daily resolution
  - *Monthly*: Month From and Month To dropdowns (January-December) are revealed; a `month` column is included in the CSV
  - *Daily*: Day From and Day To text fields (YYYY-MM-DD) are revealed; a `date` column is included in the CSV
- **Full pixel export** - Each CSV row contains `latitude`, `longitude`, `year`, `land_cover_class`, and all 64 embedding values (`A01`-`A64`)

### Quality of Life
- **Session results history table** - Every run in the current session is appended to a summary table showing time, year, classes, algorithm, accuracy, ROC AUC, and top embedding
- **EE data caching** - Sampled Earth Engine data is cached by bbox + class + scale + seed + year; re-running with the same settings skips the slow EE sampling step
- **Suppressed warnings** - `warnings.filterwarnings('ignore')` and LightGBM log suppression keep notebook output clean
- **Lazy loading** - geopy, xgboost, and lightgbm are imported only when first used, reducing startup time
- **Clean app header** - Instructions updated to reflect all new features

---

## How to Use

1. **Open the notebook** - Click the Binder badge above, or open `alpha_earth_app.ipynb` in a Jupyter environment with Earth Engine authenticated.

2. **Authenticate Earth Engine** - The notebook auto-authenticates on startup. Follow the printed link if a manual auth code is needed.

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
   - **Download Time Series Data** - Exports a pixel-level CSV with lat/lon/year/class/A01-A64 (visible after year-range runs)

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
Ibrahim, M. (2025). Extended Alpha-Earth Land Cover Classifier.
GitHub. https://github.com/mahat25n/Alpha-Earth-Land-Cover-Classifier
```

---

## Requirements

- Google Earth Engine account (free for research)
- Python 3.8+
- Key packages: `earthengine-api`, `ipyleaflet`, `ipywidgets`, `folium`, `scikit-learn`, `xgboost`, `lightgbm`, `geopy`, `gspread`, `google-auth`

All packages are installed automatically when the notebook runs.
