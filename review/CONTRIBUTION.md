# Contribution assessment, 30 October 2026

The defensible contribution is an extension of Benavides's interactive classification workflow: batch comparisons, boundary inputs and traceable annual exports, with corrections to measurement and geometry handling. It is not a new foundation model, a new learning algorithm or an established improvement in prediction. The original author and source must remain credited.

Corrected code passed a bounded comparison against the pinned original implementation. Predictions were identical, while dedicated regression tests exercised the corrected defects. This establishes preservation of the original classifiers in the tested setting. It does not establish better accuracy, faster computation or easier use. The annual export no longer manufactures monthly or daily observations from an annual product.

## Closest work and remaining questions

| Source and evidence read | Existing contribution and stated limitation | Implication for this extension |
| --- | --- | --- |
| [Benavides and colleagues, original paper](https://arxiv.org/html/2603.16911v1), methods, limitations and conclusion | Interactive classification and embedding importance already exist. Regional and temporal stability, recovery-threshold sensitivity and physical interpretation remain open. | Preserve attribution. Extra controls alone do not establish a distinct scientific contribution. |
| [Rahman, AlphaEarth land intelligence](https://arxiv.org/html/2602.10354v1), methods and conclusion; [published record](https://doi.org/10.1016/j.rsase.2026.102045) | Spatially blocked evaluation, temporal analysis and environmental interpretation already exist. Geographic coverage and expert validation remain limited. | Neither interpretation nor spatial evaluation alone is an unfilled gap. The published venue is Remote Sensing Applications: Society and Environment. |
| [Mughees and colleagues, From Foundation Embeddings to Cropland Maps](https://arxiv.org/html/2609.17138v1), limitations and future work | Classifier comparisons, label efficiency, temporal transfer and human validation are studied. Single-state coverage and within-region transfer limit generalization. | Running several classifiers across several years is insufficient as the central research claim. |
| [Ma and colleagues, Harvesting AlphaEarth](https://arxiv.org/pdf/2601.00857), limitations and conclusion; [published record](https://doi.org/10.1016/j.jag.2026.105258) | Agricultural benchmarks compare embeddings with task-specific alternatives. Geographic transfer, interpretation and annual temporal resolution constrain applications. | An agricultural application needs task-specific baselines and cannot turn annual embeddings into observed seasonal dynamics. |
| [AlphaEarth Foundations in Earth Observation: A Systematic Review of Applications and Practices](https://www.preprints.org/manuscript/202605.0981), future-research sections; unreviewed preprint | Calls for spatial validation, multi-region evaluation, label quality and practical tools. | These are directions for a study, not evidence that this particular app fills them. |

A [cross-region and cross-year irrigation study](https://doi.org/10.3390/rs18071065) also overlaps with transfer claims. Its metadata and abstract were checked; full-text access was unsuccessful, so its detailed limitations are not treated as verified. The [AlphaEarth Viewer](https://github.com/ganghyunnnn/AlphaEarth-Viewer) supplies another example of an existing embedding interface. It is not the same classifier workflow, but an interactive viewer is not a unique contribution.

Google's [official dataset documentation](https://developers.google.com/earth-engine/datasets/catalog/GOOGLE_SATELLITE_EMBEDDING_V1_ANNUAL) establishes annual resolution and official A00-A63 identifiers. It also describes training provenance. Agreement with a reference land-cover product must not automatically be described as independent ground-truth validation.

## Publication decision

This is currently a useful software extension with verified defect repairs. Scientific publishability remains unresolved. A software paper would need evidence of research use, a clearly bounded workflow advantage, reproducible installation and appropriate licensing. A notebook interface alone does not meet the [JOSS submission criteria](https://joss.readthedocs.io/en/latest/submitting.html).

A possible empirical direction is the stability of selected embedding dimensions across regions, years, classifiers and recovery thresholds. The original paper identifies related limitations, but the overlap above prevents certifying this as an unfilled gap. Before proposing that study as a contribution, its exact estimand and comparison must be checked against the closest full texts and their citing literature. No scientific rejection or superiority verdict is made here.

The next useful evaluation is a pre-specified comparison across contrasting regions with spatially separated samples, justified reference dates, uncertainty across repeated splits and an independent reference where available. A temporal-transfer claim requires training in one year and testing in another, rather than fitting separately each year. This work has not been run.

## Search coverage and provenance

Searches covered 30 October 2021 through 30 October 2026. The strict OpenAlex title search returned all 165 matching records in its response; the saved metadata are in `openalex_title_search.json`. Completeness applies only to that query, not to the literature. Broader searches for AlphaEarth, interpretation, temporal transfer and software were also screened, but two focused queries hit the result cap and one pagination request failed. Those searches do not support an exhaustive-coverage claim. Full-text review concentrated on the closest studies above; not every discovered record was read. A complete forward-citation audit remains outstanding.

Crossref metadata checks are saved in `crossref_checks.json`. These verify bibliographic records, not scientific claims. Full-text sections, rather than metadata matches, support the comparison above.

The [original archived v1.0 release](https://zenodo.org/records/16911104) declares CC-BY-4.0; its metadata are saved in `upstream_release_metadata.json`. That record alone does not establish the licensing of every later commit. Confirm the applicable code license with the original author before a software-journal submission or relicensing. No replacement license has been invented. Dataset and software licenses are separate matters.
