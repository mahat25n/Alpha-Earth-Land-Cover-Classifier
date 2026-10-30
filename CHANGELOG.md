# Corrections, 30 October 2026

Preserved the existing classifier definitions, batch processing, charts, downloads and location controls.

- Removed false monthly/daily expansion of annual samples. Export every selected class pair/year, including a single-year run, with reference metadata and the official A00-A63 names.
- Kept coordinates and sample properties from the same feature response rather than matching two responses by row order.
- Keyed the cache on the actual serialized region and sampling settings. Different polygons with the same bounding box no longer share a cache entry.
- Converted uploaded boundaries to EPSG:4326 before taking bounds. Reject missing CRS, invalid geometry, unsupported geometry and invalid coordinates. Failed uploads invalidate the selection.
- Preserved drawn polygons for sampling and clipping. Old upload display layers no longer decide the active sampling region.
- Limited descriptive score markers to algorithms for the same class pair and year, retaining ties. This does not establish statistical superiority.
- Recorded each run's own training/test counts and the primary model's correct name.
- Corrected inherited off-by-one embedding display labels. Official names are A00-A63, not A01-A64.
- Made the fixed 2020 reference and random-pixel evaluation scope explicit. Did not invent later-year reference data or silently substitute a dataset.
- Used the user's configured Earth Engine project, with environment overrides, instead of the original developer's project. Made optional Sheets logging opt-in and removed mandatory top-level gspread import.
- Kept warnings visible, cleared stale notebook outputs and added test/validation records.

Prior outputs affected by temporal duplication, band labels, region selection or sample-cache collisions require regeneration. Existing scientific results are not retroactively certified by this update.

## Additional classifiers

Added standardized logistic regression, RBF SVM, five-neighbour KNN, CatBoost and a small neural network. Shared samples, splits and threshold preserve comparisons; original model definitions are unchanged. Convergence warnings stop a run. Embedding displays support non-tree models with explicitly labelled training permutation importance. Importance exports retain provenance, and temporal charts no longer average importance across methods or class pairs.
