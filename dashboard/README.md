# Breast Cancer in Lebanon: The Numbers (dashboard)

Interactive, mobile-friendly dashboard for the MSBA 325 final project (Streamlit + Plotly).

**Tabs:** Overview · Over time · Age · Stage & region · Lebanon vs world · About the data.
A call to action (yearly mammogram from 40, free at public hospitals, hotline 1214) sits under every tab.

## Run it on your computer
```
pip install -r requirements.txt
streamlit run app.py
```

## Publish it (Streamlit Community Cloud, free)
1. Create a new **public** GitHub repository, e.g. `breast-cancer-lebanon`.
2. Upload the **contents** of this `dashboard` folder to the repository root (`app.py`, `icons.py`, `requirements.txt`, the `data` folder and the `.streamlit` folder). The `.streamlit` folder is hidden on Mac: press Cmd+Shift+. in Finder to see it.
3. Go to share.streamlit.io → **Create app** → pick the repository, branch `main`, main file `app.py` → **Deploy**.
4. Optional: in the app settings, set a custom subdomain such as `breast-cancer-lebanon.streamlit.app`.

## Embed it in the AUB blog post
Add an HTML/Custom HTML block with:
```
<iframe src="https://YOUR-APP.streamlit.app/?embed=true" width="100%" height="900" style="border:0;border-radius:16px"></iframe>
```

## Update the data
The `data` folder is generated from the project files one level up. After changing them, run:
```
python3 prepare_data.py
```

## Sources
Lebanese MoPH National Cancer Registry (2005–2024) · GLOBOCAN 2024 Cancer Today (IARC/WHO) · World Bank population estimates ·
EMHJ 2021;27(6):580–586 · AUBMC staging study (PMC7785066) · MoPH National Breast Cancer Awareness Campaign 2026.
Icons: Lucide (ISC License, see LICENSE-lucide-icons.txt).
