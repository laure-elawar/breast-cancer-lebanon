"""Breast Cancer in Lebanon: The Numbers. MSBA 325 Final Project dashboard (Streamlit)."""
import os
import textwrap

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from icons import icon

st.set_page_config(page_title="Breast Cancer in Lebanon: The Numbers", page_icon="🎗️",
                   layout="wide", initial_sidebar_state="collapsed")

# ------------------------------------------------------------------ design tokens
PINK, PINK_D, PINK_L, PINK_XL = "#C2185B", "#880E4F", "#F48FB1", "#FCE8EF"
INK, INK2, MUTED, GREY, GREY_L, LINE, BG = "#1F2A30", "#455A64", "#78909C", "#B0BEC5", "#DCE2E5", "#E6EAEC", "#F6F7F8"
FONT = "Plus Jakarta Sans, Inter, Segoe UI, Arial, sans-serif"
CFG = {"displayModeBar": False, "responsive": True}
DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")


def html(s):
    """Render HTML without Markdown turning indented lines into code blocks."""
    st.markdown("".join(line.strip() for line in textwrap.dedent(s).splitlines()), unsafe_allow_html=True)


st.markdown(f"""<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
:root{{--pink:{PINK};--pink-d:{PINK_D};--pink-xl:{PINK_XL};--ink:{INK};--ink2:{INK2};--muted:{MUTED};--line:{LINE};--bg:{BG};}}
html, body, .stApp, [class*="css"], .stMarkdown, button, input {{font-family:{FONT};}}
.stApp{{background:var(--bg);}}
#MainMenu, footer, header[data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="stDecoration"]{{display:none!important;}}
.block-container{{max-width:1120px;padding:1.4rem 1.2rem 2.5rem;}}
@keyframes rise{{from{{opacity:0;transform:translateY(14px)}}to{{opacity:1;transform:none}}}}
@keyframes pop{{0%{{opacity:0;transform:scale(.4)}}70%{{transform:scale(1.08)}}100%{{opacity:1;transform:scale(1)}}}}
@keyframes grow{{from{{width:0}}}}
/* brand */
.brand{{display:flex;align-items:center;gap:14px;margin:2px 0 18px;animation:rise .5s ease both;}}
.logo{{width:46px;height:46px;border-radius:14px;background:var(--pink);display:grid;place-items:center;box-shadow:0 6px 18px rgba(194,24,91,.28);}}
.brand-name{{font-weight:800;font-size:1.25rem;color:var(--ink);letter-spacing:-.01em;line-height:1.1;}}
.brand-sub{{color:var(--muted);font-size:.88rem;font-weight:500;}}
/* tabs as pills (works with both older BaseWeb and newer react-aria tab markup) */
.stTabs [role="tablist"]{{gap:8px;border:none!important;box-shadow:none!important;overflow-x:auto;scrollbar-width:none;padding:2px 0 6px;}}
.stTabs [role="tablist"]::-webkit-scrollbar{{display:none;}}
.stTabs [role="tablist"]::after, .stTabs [role="tablist"]::before{{display:none!important;}}
.stTabs [role="tab"]{{height:42px;padding:0 16px;border-radius:999px;background:#fff;border:1px solid var(--line);white-space:nowrap;transition:all .2s ease;display:flex;align-items:center;flex:0 0 auto;}}
.stTabs [role="tab"] p{{font-weight:600;color:var(--ink2);font-size:.92rem;margin:0;}}
.stTabs [role="tab"]:hover{{border-color:var(--pink);}}
.stTabs [role="tab"][aria-selected="true"]{{background:var(--pink)!important;border-color:var(--pink)!important;box-shadow:0 6px 16px rgba(194,24,91,.25);}}
.stTabs [role="tab"][aria-selected="true"] p, .stTabs [role="tab"][aria-selected="true"] span{{color:#fff!important;}}
.stTabs [data-baseweb="tab-highlight"], .stTabs [data-baseweb="tab-border"], .stTabs .react-aria-SelectionIndicator{{display:none!important;}}
.stTabs [role="tabpanel"]{{padding-top:14px;animation:rise .45s ease both;}}
/* section header */
.eyebrow{{display:inline-flex;align-items:center;gap:8px;color:var(--pink);font-weight:700;font-size:.78rem;letter-spacing:.12em;text-transform:uppercase;}}
.h2{{font-size:2.05rem;font-weight:800;color:var(--ink);letter-spacing:-.02em;line-height:1.15;margin:6px 0 8px;}}
.lead{{color:var(--ink2);font-size:1.02rem;max-width:62ch;margin:0 0 18px;line-height:1.55;}}
.head{{animation:rise .5s ease both;}}
/* cards */
[class*="st-key-card"]{{background:#fff;border:1px solid var(--line);border-radius:20px;padding:18px 20px 10px;box-shadow:0 1px 2px rgba(31,42,48,.04),0 10px 28px rgba(31,42,48,.06);animation:rise .55s ease both;}}
.card-title{{font-weight:700;color:var(--ink);font-size:1.02rem;display:flex;align-items:center;gap:8px;margin-bottom:2px;}}
.card-sub{{color:var(--muted);font-size:.86rem;margin-bottom:4px;}}
.note{{color:var(--muted);font-size:.8rem;margin:2px 0 8px;}}
/* KPI cards */
.kpis{{display:grid;grid-template-columns:repeat(2,1fr);gap:14px;}}
.kpis.k3{{grid-template-columns:repeat(3,1fr);}}
.kpi{{background:#fff;border:1px solid var(--line);border-radius:20px;padding:18px 18px 16px;box-shadow:0 10px 28px rgba(31,42,48,.06);animation:rise .6s ease both;animation-delay:var(--d,0s);}}
.kpi-ic{{width:38px;height:38px;border-radius:12px;background:var(--pink-xl);display:grid;place-items:center;margin-bottom:10px;}}
.kpi-val{{font-size:2.25rem;font-weight:800;color:var(--pink);letter-spacing:-.02em;line-height:1.05;}}
.kpi-val.dark{{color:var(--ink);}}
.kpi-lab{{color:var(--ink2);font-size:.92rem;margin-top:4px;line-height:1.35;}}
/* overview */
.overview{{display:grid;grid-template-columns:1fr 1.25fr;gap:16px;align-items:stretch;}}
.waffle-card{{background:#fff;border:1px solid var(--line);border-radius:20px;padding:22px;box-shadow:0 10px 28px rgba(31,42,48,.06);animation:rise .55s ease both;display:flex;flex-direction:column;justify-content:center;}}
.waffle{{display:grid;grid-template-columns:repeat(10,1fr);gap:6px;max-width:330px;margin:0 auto;width:100%;}}
.cell{{aspect-ratio:1;border-radius:5px;background:{GREY_L};animation:pop .45s ease both;}}
.cell.on{{background:var(--pink);}}
.waffle-cap{{text-align:center;color:var(--ink2);margin-top:14px;font-size:.95rem;}}
.waffle-cap b{{color:var(--pink);font-size:1.15rem;}}
/* tile map */
.tiles{{display:grid;grid-template-columns:1fr 1.15fr .95fr;grid-template-rows:repeat(3,96px);gap:8px;margin:8px 0 6px;}}
.tile{{border-radius:16px;padding:12px 14px;display:flex;flex-direction:column;justify-content:space-between;color:#fff;animation:pop .5s ease both;animation-delay:var(--d,0s);}}
.tile .tn{{font-weight:600;font-size:.86rem;opacity:.95;}}
.tile .tv{{font-weight:800;font-size:1.7rem;letter-spacing:-.02em;}}
.tile.light{{color:var(--ink);}}
.legend{{display:flex;align-items:center;gap:8px;color:var(--muted);font-size:.78rem;margin:4px 0 6px;}}
.legend .bar{{height:8px;flex:0 0 120px;border-radius:99px;background:linear-gradient(90deg,{PINK_L},{PINK},{PINK_D});}}
/* CTA */
.cta{{margin-top:22px;display:flex;align-items:center;gap:16px;background:var(--pink);color:#fff;border-radius:22px;padding:18px 22px;box-shadow:0 14px 34px rgba(194,24,91,.28);animation:rise .6s ease both;}}
.cta-ic{{width:48px;height:48px;border-radius:14px;background:rgba(255,255,255,.16);display:grid;place-items:center;flex:0 0 48px;}}
.cta-txt{{flex:1;line-height:1.35;}} .cta-txt b{{font-size:1.12rem;display:block;}} .cta-txt span{{opacity:.92;font-size:.92rem;}}
.cta-btn{{background:#fff;color:var(--pink)!important;text-decoration:none!important;font-weight:700;border-radius:999px;padding:10px 16px;display:inline-flex;gap:8px;align-items:center;white-space:nowrap;transition:transform .2s ease;}}
.cta-btn:hover{{transform:translateY(-2px);}}
.segbar{{display:flex;height:46px;border-radius:12px;overflow:hidden;margin:10px 0 8px;gap:3px;}}
.seg{{display:grid;place-items:center;font-weight:800;font-size:1rem;transform-origin:left;animation:sx .8s cubic-bezier(.2,.8,.2,1) both;}}
@keyframes sx{{from{{transform:scaleX(0);opacity:.3}}to{{transform:none;opacity:1}}}}
.segkey{{display:flex;flex-wrap:wrap;gap:6px 16px;color:var(--ink2);font-size:.86rem;margin-bottom:6px;}}
.segkey i{{display:inline-block;width:10px;height:10px;border-radius:3px;margin-right:6px;vertical-align:-1px;}}
.foot{{color:var(--muted);font-size:.78rem;margin-top:14px;text-align:center;}}
/* about */
.src{{display:grid;grid-template-columns:repeat(2,1fr);gap:12px;}}
.src a{{display:flex;gap:12px;align-items:flex-start;background:#fff;border:1px solid var(--line);border-radius:16px;padding:14px 16px;text-decoration:none!important;color:var(--ink)!important;transition:all .2s ease;animation:rise .5s ease both;animation-delay:var(--d,0s);}}
.src a:hover{{border-color:var(--pink);transform:translateY(-2px);}}
.src .si{{width:34px;height:34px;border-radius:10px;background:var(--pink-xl);display:grid;place-items:center;flex:0 0 34px;}}
.src b{{display:block;font-size:.95rem;}} .src span{{color:var(--muted);font-size:.84rem;}}
.checks{{list-style:none;padding:0;margin:4px 0 0;}}
.checks li{{display:flex;gap:10px;align-items:flex-start;color:var(--ink2);margin:9px 0;font-size:.94rem;}}
[data-testid="stButtonGroup"]{{margin-bottom:2px;}}
@media (max-width:760px){{
  .block-container{{padding:1rem .9rem 2rem;}}
  .h2{{font-size:1.55rem;}} .lead{{font-size:.95rem;}}
  .overview{{grid-template-columns:1fr;}}
  .kpis.k3{{grid-template-columns:1fr 1fr;}} .kpis.k3 .kpi:last-child{{grid-column:span 2;}}
  .kpi{{padding:14px;}} .kpi-val{{font-size:1.75rem;}}
  .tiles{{grid-template-rows:repeat(3,84px);}} .tile .tv{{font-size:1.35rem;}}
  .cta{{flex-direction:column;align-items:flex-start;}}
  .src{{grid-template-columns:1fr;}}
}}
</style>""", unsafe_allow_html=True)


# ------------------------------------------------------------------ data
@st.cache_data
def load():
    r = lambda f: pd.read_csv(os.path.join(DATA, f))
    return {k: r(f"{k}.csv") for k in ["year", "age", "band_index", "decomposition", "stage_region", "stage_compare", "world"]}


D = load()
Y = D["year"].set_index("year")
y24, y05 = Y.loc[2024], Y.loc[2005]


def layout(fig, h=380, **kw):
    base = dict(height=h, margin=dict(l=6, r=10, t=12, b=6), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(family=FONT, size=13, color=INK2), showlegend=False, hovermode="closest",
                hoverlabel=dict(bgcolor="#fff", bordercolor=LINE, font=dict(family=FONT, size=13, color=INK)))
    base.update(kw)
    fig.update_layout(**base)
    fig.update_xaxes(showgrid=False, zeroline=False, showline=False, tickfont=dict(color=MUTED), fixedrange=True)
    fig.update_yaxes(gridcolor="#EEF1F3", zeroline=False, showline=False, tickfont=dict(color=MUTED), fixedrange=True)
    return fig


def pct(x):
    return f"{int(x + 0.5)}%"


def header(eyebrow, ico, title, lead):
    html(f"""<div class="head"><span class="eyebrow">{icon(ico, 16, PINK, 2.4)}{eyebrow}</span>
             <div class="h2">{title}</div><p class="lead">{lead}</p></div>""")


def kpi(val, label, ico, delay=0.0, dark=False):
    return (f'<div class="kpi" style="--d:{delay}s"><div class="kpi-ic">{icon(ico, 20, PINK, 2.2)}</div>'
            f'<div class="kpi-val{" dark" if dark else ""}">{val}</div><div class="kpi-lab">{label}</div></div>')


# ------------------------------------------------------------------ brand
html(f"""<div class="brand"><div class="logo">{icon("ribbon", 26, "#fff", 2.2)}</div>
         <div><div class="brand-name">Breast Cancer in Lebanon: <span style="color:var(--pink);white-space:nowrap">The Numbers</span></div><div class="brand-sub">Official data, 2005–2024 · what it means for you</div></div></div>""")

t_over, t_time, t_age, t_stage, t_world, t_about = st.tabs([
    ":material/home: Overview", ":material/show_chart: Over time", ":material/groups: Age",
    ":material/location_on: Stage & region", ":material/public: Lebanon vs world", ":material/info: About the data"])

# ================================================================== OVERVIEW
with t_over:
    header("The big picture", "heart-pulse", "Breast cancer is the #1 cancer in Lebanese women",
           "Four in every ten cancers diagnosed in Lebanese women are breast cancer. Found in time and treated, 80–90% of women are cured.")
    cells = "".join(f'<div class="cell{" on" if i < 40 else ""}" style="animation-delay:{i * 0.012:.3f}s"></div>' for i in range(100))
    ratio = y24.cases / y05.cases
    html(f"""<div class="overview">
      <div class="waffle-card"><div class="waffle">{cells}</div>
        <div class="waffle-cap"><b>{y24.share_of_women_cancers_pct:.0f}</b> of every 100 new cancers in women are breast cancer (2024)</div></div>
      <div class="kpis">
        {kpi(f"{int(y24.cases):,}", "women diagnosed in 2024", "users", .10)}
        {kpi(f"×{ratio:.1f}", f"more cases than in 2005 ({int(y05.cases):,})", "trending-up", .18)}
        {kpi("1 in 4", "women diagnosed before age 50", "user-round", .26)}
        {kpi("1 in 3", "women still found at a late stage", "clock", .34)}
      </div></div>""")

# ================================================================== OVER TIME
with t_time:
    header("Over time", "chart-line", "Cases have more than doubled since 2005",
           "The rise is not only because Lebanon's population grew and aged — the rate itself has climbed to double the world average.")
    with st.container(border=False, key="card_time"):
        view = st.segmented_control("View", ["Women diagnosed", "Rate per 100,000 women"], default="Women diagnosed",
                                    label_visibility="collapsed", key="time_view") or "Women diagnosed"
        yrs = Y.index.tolist()
        fig = go.Figure()
        if view == "Women diagnosed":
            fig.add_trace(go.Scatter(x=yrs, y=Y.cases, mode="lines", line=dict(color=PINK, width=3.5, shape="spline", smoothing=.6),
                                     fill="tozeroy", fillcolor="rgba(194,24,91,.08)", hovertemplate="<b>%{x}</b><br>%{y:,} women diagnosed<extra></extra>"))
            fig.add_trace(go.Scatter(x=[2005, 2024], y=[y05.cases, y24.cases], mode="markers+text", marker=dict(size=11, color=PINK, line=dict(color="#fff", width=2.5)),
                                     text=[f"{int(y05.cases):,}", f"{int(y24.cases):,}"], textposition=["bottom right", "top center"],
                                     textfont=dict(size=15, color=PINK, family=FONT), hoverinfo="skip", cliponaxis=False))
            for yr, lab in [(2016, "Registry dip"), (2020, "COVID-19")]:
                fig.add_annotation(x=yr, y=Y.loc[yr, "cases"], text=lab, showarrow=True, arrowhead=0, arrowcolor=GREY, ay=36, ax=0,
                                   font=dict(size=11, color=MUTED))
            layout(fig, 380, yaxis=dict(range=[0, 4400], tickformat=",", title=None))
            caption = "Women diagnosed with breast cancer each year. Source: Lebanese MoPH National Cancer Registry."
        else:
            fig.add_trace(go.Scatter(x=yrs, y=Y.asr_recalculated, mode="lines", line=dict(color=PINK, width=3.5, shape="spline", smoothing=.6),
                                     hovertemplate="<b>%{x}</b><br>%{y:.1f} per 100,000 women<extra></extra>"))
            fig.add_hline(y=47.8, line=dict(color=INK, width=1.5, dash="dot"))
            fig.add_annotation(x=2005, y=47.8, xanchor="left", yanchor="bottom", text="World average (2024): 47.8", showarrow=False, font=dict(size=12, color=INK))
            fig.add_trace(go.Scatter(x=[2024], y=[y24.asr_recalculated], mode="markers+text", marker=dict(size=11, color=PINK, line=dict(color="#fff", width=2.5)),
                                     text=[f"{y24.asr_recalculated:.0f}"], textposition="top center", textfont=dict(size=15, color=PINK), hoverinfo="skip", cliponaxis=False))
            layout(fig, 380, yaxis=dict(range=[0, 125], title=None))
            caption = "Age-standardised rate, recalculated with World Bank population estimates so every year uses the same base."
        fig.update_xaxes(dtick=3, tick0=2005)
        st.plotly_chart(fig, config=CFG)
        html(f'<div class="note">{caption}</div>')

    dec = D["decomposition"].set_index("component")["share_of_increase_pct"].dropna()
    with st.container(border=False, key="card_dec"):
        html(f'<div class="card-title">{icon("search", 18, PINK, 2.4)}Why did cases grow?</div>'
             '<div class="card-sub">Share of the 2,300 extra cases a year between 2005 and 2024</div>')
        parts = [("More women", dec.iloc[0], GREY_L, INK2), ("Older population", dec.iloc[1], GREY, INK), ("Higher rate", dec.iloc[2], PINK, "#fff")]
        segs = "".join(f'<div class="seg" style="flex:{v:.1f};background:{c};color:{tc};animation-delay:{.15 * i:.2f}s">{pct(v)}</div>'
                       for i, (n, v, c, tc) in enumerate(parts))
        keys = "".join(f'<span><i style="background:{c}"></i>{n}</span>' for n, v, c, tc in parts)
        html(f'<div class="segbar">{segs}</div><div class="segkey">{keys}</div>')
        html('<div class="note">Holding 2005 rates fixed, population growth and ageing explain 43% of the rise; the other 57% comes from a higher rate (more risk, better detection and registration).</div>')

# ================================================================== AGE
with t_age:
    header("Age at diagnosis", "user-round", "1 in 4 women is diagnosed before 50",
           "Screening starts at 40 — but breast cancer doesn't wait. Younger women should know the signs and see a doctor early.")
    A = D["age"]
    A = A[A.age_start >= 20]
    years = sorted(A.year.unique())
    cols = [PINK if s < 50 else GREY_L for s in A[A.year == 2024].age_start]

    def bar(yr):
        d = A[A.year == yr]
        return go.Bar(x=d.age_group.str.split("-").str[0], y=d.cases, customdata=d.age_group, marker=dict(color=cols), text=d.cases, textposition="outside",
                      textfont=dict(size=11, color=MUTED), cliponaxis=False, hovertemplate="Age %{customdata}<br><b>%{y:,}</b> women<extra></extra>")

    def ttl(yr):
        return dict(text=f"<b>{yr}</b>  ·  {pct(Y.loc[yr, 'pct_under_50_known'])} under 50",
                    x=0, xanchor="left", font=dict(size=15, color=INK, family=FONT))

    with st.container(border=False, key="card_age"):
        fig = go.Figure(data=[bar(2024)], frames=[go.Frame(data=[bar(yr)], name=str(yr), layout=dict(title=ttl(yr))) for yr in years])
        steps = [dict(method="animate", label=str(yr) if yr in (2005, 2010, 2015, 2020, 2024) else "", args=[[str(yr)], dict(mode="immediate", frame=dict(duration=500, redraw=True), transition=dict(duration=450, easing="cubic-in-out"))]) for yr in years]
        layout(fig, 470, title=ttl(2024), margin=dict(l=6, r=10, t=50, b=6), yaxis=dict(range=[0, 640], visible=False), bargap=.22,
               xaxis=dict(type="category", title=dict(text="Age group (starting age of each 5-year band)", font=dict(size=11, color=MUTED)), tickangle=0),
               barcornerradius=6,
               sliders=[dict(active=len(years) - 1, steps=steps, x=0, len=1, y=-0.1, pad=dict(t=36, b=0), currentvalue=dict(visible=False),
                             bgcolor=GREY_L, activebgcolor=PINK, bordercolor=LINE, tickcolor=GREY, font=dict(size=10, color=MUTED))],
               updatemenus=[dict(type="buttons", showactive=False, x=1, y=1.13, xanchor="right", yanchor="top", pad=dict(t=0, r=0),
                                 bgcolor=PINK_XL, bordercolor=PINK, font=dict(color=PINK, size=12),
                                 buttons=[dict(label="▶  Play", method="animate",
                                               args=[None, dict(frame=dict(duration=650, redraw=True), transition=dict(duration=450, easing="cubic-in-out"), fromcurrent=False, mode="immediate")])])])
        st.plotly_chart(fig, config=CFG)
        html('<div class="note">Press Play or drag the slider to watch 2005 → 2024. Pink = under 50. Women under 20 are rare (fewer than 25 a year) and not shown. Source: MoPH National Cancer Registry.</div>')

    bi = D["band_index"].set_index("year")
    html(f"""<div class="kpis" style="margin-top:14px">
        {kpi(f"+{bi.loc[2023, 'Under 40'] - 100:.0f}%", "rise in the breast cancer rate for women under 40 since 2006 — the fastest of any age group", "activity", .1)}
        {kpi(f"{int(y24.men_cases)} men", "diagnosed in 2024. Men get breast cancer too", "user-round", .18, dark=True)}
    </div>""")

# ================================================================== STAGE & REGION
with t_stage:
    header("Stage at diagnosis", "map-pin", "Too many women are found late",
           "About 1 in 3 women is still diagnosed at an advanced stage today (MoPH, 2026). In 2012–2017, late diagnosis was most common in Bekaa and the North.")
    c1, c2 = st.columns([1, 1.1], gap="medium")
    R = D["stage_region"].set_index("governorate")["late_pct"]
    lo, hi = R.min(), R.max()

    def tile_color(v):
        t = (v - lo) / (hi - lo)  # 0..1 → light pink .. deep pink
        a, b = (0xF4, 0x8F, 0xB1), (0x88, 0x0E, 0x4F)
        return "#%02X%02X%02X" % tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))

    place = {"North Lebanon": "1 / 1 / 2 / 3", "Bekaa": "1 / 3 / 4 / 4", "Beirut": "2 / 1 / 3 / 2", "Mount Lebanon": "2 / 2 / 3 / 3", "South Lebanon": "3 / 1 / 4 / 3"}
    order = R.sort_values(ascending=False).index.tolist()
    tiles = "".join(
        f'<div class="tile{" light" if (R[g] - lo) / (hi - lo) < .35 else ""}" style="grid-area:{place[g]};background:{tile_color(R[g])};--d:{0.08 * order.index(g):.2f}s">'
        f'<div class="tn">{g}</div><div class="tv">{pct(R[g])}</div></div>' for g in place)
    with c1:
        with st.container(border=False, key="card_map"):
            html(f'<div class="card-title">{icon("map-pin", 18, PINK, 2.4)}Diagnosed at stage III–IV, by region</div>'
                 f'<div class="card-sub">2012–2017 · 3,320 women in the Ministry\'s cancer drug programme</div>'
                 f'<div class="tiles">{tiles}</div>'
                 f'<div class="legend"><span>{lo:.0f}%</span><div class="bar"></div><span>{hi:.0f}%</span><span>· schematic map, not to scale</span></div>')
    with c2:
        with st.container(border=False, key="card_hope"):
            html(f'<div class="card-title">{icon("sparkles", 18, PINK, 2.4)}Early detection works</div>'
                 '<div class="card-sub">Stage at diagnosis where screening campaigns reached women vs the national programme</div>')
            C = D["stage_compare"]
            labels = ["Private hospital,<br>before campaigns", "Private hospital,<br>after campaigns", "National<br>programme"]
            fig = go.Figure()
            for k, nm, col, tc in [("I", "Stage I", "#F8BBD0", INK), ("II", "Stage II", PINK_L, INK), ("III", "Stage III", PINK, "#fff"), ("IV", "Stage IV", PINK_D, "#fff")]:
                v = C[f"stage_{k}_pct"]
                fig.add_trace(go.Bar(y=labels, x=v, name=nm, orientation="h", marker=dict(color=col, line=dict(color="#fff", width=1.5)),
                                     text=[pct(x) if x >= 12 else "" for x in v], textposition="inside", insidetextanchor="middle", textangle=0,
                                     textfont=dict(color=tc, size=12), hovertemplate=f"{nm}: %{{x:.1f}}%<extra></extra>"))
            layout(fig, 300, barmode="stack", showlegend=True, legend=dict(orientation="h", y=-0.12, x=0, xanchor="left", traceorder="normal", font=dict(size=12, color=INK2)),
                   xaxis=dict(visible=False, range=[0, 100]), yaxis=dict(autorange="reversed", tickfont=dict(size=12, color=INK2)), bargap=.35,
                   margin=dict(l=6, r=6, t=6, b=6))
            st.plotly_chart(fig, config=CFG)
            html('<div class="note">Stage I diagnoses doubled (14% → 31%) after campaigns began at one private Beirut hospital. Different populations — indicative comparison.</div>')

# ================================================================== LEBANON VS WORLD
with t_world:
    header("Lebanon vs the world", "globe", "Double the world's rate — and double its death rate",
           "Lebanon's breast cancer rate is in the European range, yet it has the highest death rate of the nine places compared.")
    W = D["world"].sort_values("asr_incidence_female")
    colw = [PINK if c == "Lebanon" else (INK if c == "World" else GREY_L) for c in W.country]
    tcol = [PINK if c == "Lebanon" else (INK if c == "World" else MUTED) for c in W.country]

    def wbar(col, fmt="%{x:.1f}"):
        return go.Bar(y=W.country, x=W[col], orientation="h", marker=dict(color=colw), text=W[col].map(lambda v: f"{v:.1f}"),
                      textposition="outside", textfont=dict(size=12, color=tcol), cliponaxis=False,
                      hovertemplate="<b>%{y}</b><br>" + fmt + " per 100,000 women<extra></extra>")

    with st.container(border=False, key="card_world"):
        html(f'<div class="card-title">{icon("globe", 18, PINK, 2.4)}Breast cancer per 100,000 women, 2024</div>'
             '<div class="card-sub">Age-standardised rates · switch between new cases and deaths</div>')
        fig = go.Figure(data=[wbar("asr_incidence_female")],
                        frames=[go.Frame(data=[wbar("asr_incidence_female")], name="inc", layout=dict(xaxis=dict(range=[0, 120]))),
                                go.Frame(data=[wbar("asr_mortality_female")], name="mor", layout=dict(xaxis=dict(range=[0, 31])))])
        anim = lambda n: [[n], dict(mode="immediate", frame=dict(duration=650, redraw=True), transition=dict(duration=550, easing="cubic-in-out"))]
        layout(fig, 420, margin=dict(l=6, r=30, t=52, b=6), xaxis=dict(range=[0, 120], visible=False),
               yaxis=dict(tickfont=dict(size=13, color=INK2)), bargap=.32, barcornerradius=6,
               updatemenus=[dict(type="buttons", direction="left", x=0, y=1.14, xanchor="left", yanchor="top", showactive=True, active=0,
                                 bgcolor="#fff", bordercolor=PINK, font=dict(size=13, color=PINK), pad=dict(r=6, t=0),
                                 buttons=[dict(label="  New cases  ", method="animate", args=anim("inc")),
                                          dict(label="  Deaths  ", method="animate", args=anim("mor"))])])
        st.plotly_chart(fig, config=CFG)
        html('<div class="note">Source: GLOBOCAN 2024, Cancer Today (IARC/WHO).</div>')
    L, Wd = W.set_index("country").loc["Lebanon"], W.set_index("country").loc["World"]
    cy = W.set_index("country").loc["Cyprus"]
    html(f"""<div class="kpis k3" style="margin-top:14px">
        {kpi(f"{L.asr_incidence_female:.0f} vs {Wd.asr_incidence_female:.0f}", "new cases per 100,000 women — Lebanon vs world", "trending-up", .1)}
        {kpi(f"{L.asr_mortality_female:.0f} vs {Wd.asr_mortality_female:.0f}", "deaths per 100,000 women — the highest of the nine compared", "heart-pulse", .18)}
        {kpi(f"{L.deaths_per_10_cases:.1f}", f"deaths for every 10 new cases (Cyprus: {cy.deaths_per_10_cases:.1f}), a sign of later diagnosis", "clock", .26, dark=True)}
    </div>""")

# ================================================================== ABOUT
with t_about:
    header("About the data", "database", "Where these numbers come from",
           "Every figure on this dashboard comes from an official or peer-reviewed source and was checked before publishing.")
    srcs = [
        ("database", "Lebanese MoPH National Cancer Registry", "New cases by age and sex, 2005–2024", "https://moph.gov.lb/en/Pages/2/19523/national-cancer-registry"),
        ("globe", "GLOBOCAN 2024 · Cancer Today (IARC/WHO)", "Rates and deaths for Lebanon, neighbours and the world", "https://gco.iarc.who.int/today/"),
        ("users", "World Bank population estimates", "Female population by age, used to recalculate rates", "https://data.worldbank.org/indicator/SP.POP.TOTL.FE.IN?locations=LB"),
        ("map-pin", "EMHJ 2021 · stage at diagnosis in Lebanon", "3,320 women, 2012–2017, by region and age", "https://applications.emro.who.int/EMHJ/V27/06/1020-3397-2021-2706-580-586-eng.pdf"),
        ("sparkles", "AUBMC staging study (PMC7785066)", "Stage before and after screening campaigns", "https://pmc.ncbi.nlm.nih.gov/articles/PMC7785066"),
        ("calendar-check", "MoPH Breast Cancer Campaign 2026", "Screening age, free mammograms, hotline 1214", "https://www.moph.gov.lb/en/Pages/0/87129/national-breast-cancer-awareness-campaign-2026"),
    ]
    html('<div class="src">' + "".join(
        f'<a href="{u}" target="_blank" style="--d:{0.06 * i:.2f}s"><div class="si">{icon(ic, 18, PINK, 2.2)}</div><div><b>{n}</b><span>{d}</span></div></a>'
        for i, (ic, n, d, u) in enumerate(srcs)) + '</div><div style="height:16px"></div>')
    c1, c2 = st.columns(2, gap="medium")
    ok = icon("shield-check", 18, PINK, 2.2)
    with c1:
        with st.container(border=False, key="card_checks"):
            html(f'<div class="card-title">How we checked</div><ul class="checks">'
                 f'<li>{ok}<span>All 140 registry tables checked automatically: age groups add up to totals in every case.</span></li>'
                 f'<li>{ok}<span>Stage data spot-checked against the published paper: 0% error.</span></li>'
                 f'<li>{ok}<span>International figures confirmed on GLOBOCAN Cancer Today.</span></li></ul>')
    with c2:
        with st.container(border=False, key="card_care"):
            inf = icon("info", 18, MUTED, 2.2)
            html(f'<div class="card-title">Read with care</div><ul class="checks">'
                 f'<li>{inf}<span>Rising rates mix real risk with better detection and registration.</span></li>'
                 f'<li>{inf}<span>Lebanon\'s population figures are estimates; read 2013–2017 rates with caution.</span></li>'
                 f'<li>{inf}<span>The national registry does not record stage; stage data comes from published studies.</span></li></ul>')
    html('<div class="foot">MSBA 325 · Data Visualization and Communication · American University of Beirut · Data accessed October 2026 · Icons: Lucide (ISC)</div>')

# ------------------------------------------------------------------ call to action (every tab)
html(f"""<div class="cta"><div class="cta-ic">{icon("calendar-check", 26, "#fff", 2.2)}</div>
  <div class="cta-txt"><b>Women 40+: one mammogram a year</b><span>Free at all public hospitals until 8 Oct 2027 — even without symptoms.</span></div>
  <a class="cta-btn" href="tel:1214">{icon("phone", 18, PINK, 2.4)}Hotline 1214</a></div>""")
