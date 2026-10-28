# CLT544 — Visualizing the Central Limit Theorem

Interactive SI 544 teaching app by Bobby Madamanchi, adapted from the course's `CLT_ShinyApp.R` and `W2Lecture544.pdf` (CLT explanation, pp. 8–9).

Compare normal, uniform, gamma and bimodal populations across four views: population density, repeated samples, sample means, and pooled individual observations. Change sample size separately from repetition count. Both a row-by-row view and the original full-panel view are available.

## Deploy on Streamlit Community Cloud

- Repository: `umsi-amadaman/clt544`
- Branch: `main`
- Main file: `streamlit_app.py`
- Python: 3.11
- Requested custom subdomain: `clt544` (availability is determined by Streamlit at deployment)
- No secrets or external data are required. The simulation uses mathematical distributions.

Open https://share.streamlit.io/ and create an app using those settings. Students use the deployed web URL; they do not need R or Python installed.

## Local development

```sh
python -m pip install -r requirements.txt
streamlit run streamlit_app.py
python test_app.py
```

## Statistical details

Normal, uniform and shifted gamma populations share the chosen mean and base SD. The bimodal population is an equal mixture with component means `mu ± separation * sd` and component SD `sd/2`. Its variance is therefore `(separation*sd)^2 + (sd/2)^2`; its normal approximation uses that actual population SD divided by `sqrt(n)`. This corrects the shared-SD overlay in the original R app.

At n=1, sample means have the population distribution. Increasing sample size concentrates the means and yields approximate normality under the usual independent, identically distributed, finite-variance conditions. Increasing repetition count stabilizes the empirical display without changing the theoretical SE at fixed n. Pooling individual observations does not make a nonnormal population normal.

The playground-age example is an analogy for bimodality; the plotted values are not real age observations. The visible sample-row panel shows the first 12 samples; means and pooled panels use every repetition.

`clt_core.py` is shared with the October 29 notebook and lecture figures. `test_app.py` checks moments, density normalization, reproducibility, the n=1 case and Streamlit controls.
