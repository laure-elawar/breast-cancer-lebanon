"""
Builds the dashboard's data bundle (data/*.csv) from the project's cleaned and verified files.
Run from the dashboard folder:  python3 prepare_data.py
Inputs (one level up, in the Final Project folder):
  NCR_breast_clean.xlsx, Round2_tables.xlsx,
  round2_data/globocan2024_comparison_confirmed.csv, round2_data/stage_at_diagnosis_extracted.csv
"""
import os
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.dirname(HERE)
OUT = os.path.join(HERE, "data"); os.makedirs(OUT, exist_ok=True)

clean = pd.read_excel(os.path.join(SRC, "NCR_breast_clean.xlsx"), sheet_name=None)
r2 = pd.read_excel(os.path.join(SRC, "Round2_tables.xlsx"), sheet_name=None)

# yearly series (women) + recalculated age-standardised rate + men
y = clean["breast_women_year"][["year", "cases", "share_of_women_cancers_pct", "pct_under_50_known", "under_50", "median_age_est"]]
rates = r2["R1_consistent_rates"][["year", "asr_world"]].rename(columns={"asr_world": "asr_recalculated"})
men = clean["breast_by_gender"][["year", "male"]].rename(columns={"male": "men_cases"})
y = y.merge(rates, on="year").merge(men, on="year")
y.to_csv(os.path.join(OUT, "year.csv"), index=False)

# age distribution by year (known ages only)
a = clean["breast_women_age"]
a = a[a.age_group != "Unspecified"][["year", "age_group", "age_order", "age_start", "cases"]]
a.to_csv(os.path.join(OUT, "age.csv"), index=False)

# rate change by age band (3-year averages, 2006 = 100)
r2["R3_rate_index_2006_100"].dropna().to_csv(os.path.join(OUT, "band_index.csv"), index=False)

# growth decomposition 2005 -> 2024
r2["R2_decomposition"].to_csv(os.path.join(OUT, "decomposition.csv"), index=False)

# stage at diagnosis
st = pd.read_csv(os.path.join(SRC, "round2_data", "stage_at_diagnosis_extracted.csv"))
for k in ["I", "II", "III", "IV"]:
    st[f"stage_{k}_pct"] = (100 * st[f"stage_{k}_n"] / st.total_n).round(1)
st["late_pct"] = (st.stage_III_pct + st.stage_IV_pct).round(1)
st[st.group_type == "governorate"][["group", "total_n", "late_pct"]].rename(columns={"group": "governorate"}) \
    .to_csv(os.path.join(OUT, "stage_region.csv"), index=False)
cmp = st[st.group_type == "period"][["group", "stage_I_pct", "stage_II_pct", "stage_III_pct", "stage_IV_pct"]].copy()
gov = st[st.group_type == "governorate"]
nat = {f"stage_{k}_pct": round(100 * gov[f"stage_{k}_n"].sum() / gov.total_n.sum(), 1) for k in ["I", "II", "III", "IV"]}
cmp = pd.concat([cmp, pd.DataFrame([{"group": "National programme (2012-2017)", **nat}])], ignore_index=True)
cmp.to_csv(os.path.join(OUT, "stage_compare.csv"), index=False)

# Lebanon vs world (GLOBOCAN 2024, confirmed on Cancer Today)
g = pd.read_csv(os.path.join(SRC, "round2_data", "globocan2024_comparison_confirmed.csv"))
g = g[["country", "asr_incidence_female", "asr_mortality_female", "breast_cases_women", "breast_deaths_women"]]
g["deaths_per_10_cases"] = (10 * g.breast_deaths_women / g.breast_cases_women).round(1)
g["country"] = g.country.replace({"France (metropolitan)": "France", "Turkiye": "Türkiye"})
g.to_csv(os.path.join(OUT, "world.csv"), index=False)

print("Data bundle written to", OUT, sorted(os.listdir(OUT)))
