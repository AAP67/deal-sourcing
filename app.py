import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from datetime import datetime
from config import STAGE_KPIS, INDUSTRIES, STAGES, GEOS
from research import research_deals


def scroll_to_top():
    """Inject JS to scroll the page to the top."""
    components.html(
        "<script>window.parent.document.querySelector('section.main').scrollTo(0, 0);</script>",
        height=0,
    )

# ─── Page Config ─────────────────────────────────────────────
st.set_page_config(
    page_title="Deal Sourcing",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── Custom CSS ──────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

    /* Global */
    .stApp { background: #09090b; }
    header[data-testid="stHeader"] { background: transparent; }
    .block-container { padding: 2rem 2rem 4rem; max-width: 1200px; }

    /* Hide streamlit elements */
    #MainMenu, footer, .stDeployButton { display: none !important; }

    /* Typography */
    h1, h2, h3, p, span, div, label { font-family: 'DM Sans', sans-serif !important; }
    h1 { color: #fafafa !important; font-weight: 700 !important; letter-spacing: -0.03em !important; }
    h3 { color: #fafafa !important; font-weight: 600 !important; font-size: 1.1rem !important; }

    /* Section labels */
    .field-label {
        font-size: 11px; font-weight: 600; color: #71717a;
        text-transform: uppercase; letter-spacing: 0.07em;
        margin-bottom: 8px;
    }

    /* Chips container */
    .chip-container { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 4px; }
    .chip {
        display: inline-flex; align-items: center; padding: 8px 16px;
        border-radius: 10px; border: 1px solid #27272a; background: #111113;
        color: #a1a1aa; font-size: 13px; font-weight: 500;
        cursor: pointer; transition: all 0.15s ease; user-select: none;
    }
    .chip:hover { border-color: #3f3f46; color: #d4d4d8; }
    .chip.selected { border-color: #3b82f6; background: #0c1a2e; color: #60a5fa; }

    /* KPI checkbox items */
    .kpi-item {
        display: flex; align-items: center; gap: 10px;
        padding: 11px 14px; background: #111113;
        border: 1px solid #1e1e22; border-radius: 10px;
        font-size: 13px; color: #71717a;
        cursor: pointer; transition: all 0.15s ease;
        margin-bottom: 6px;
    }
    .kpi-item.selected { background: #0c1a2e; border-color: #1e3a5f; color: #93c5fd; }
    .kpi-item:hover { border-color: #27272a; }

    /* Result card */
    .result-card {
        background: #0c0c0e; border: 1px solid #1e1e22;
        border-radius: 12px; padding: 20px 24px;
        margin-bottom: 8px; transition: all 0.15s ease;
    }
    .result-card:hover { background: #111115; border-color: #27272a; }

    .company-name { font-size: 16px; font-weight: 600; color: #fafafa; margin-bottom: 2px; }
    .company-domain {
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 11.5px; color: #60a5fa; opacity: 0.7;
    }
    .company-meta { font-size: 12px; color: #71717a; margin-top: 4px; }

    .rationale { font-size: 13px; line-height: 1.6; color: #a1a1aa; margin: 12px 0; }

    .match-score {
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 22px; font-weight: 700;
    }
    .match-high { color: #34d399; }
    .match-mid { color: #fbbf24; }
    .match-low { color: #f87171; }

    .match-bar { width: 100%; height: 4px; background: #1e1e22; border-radius: 4px; overflow: hidden; margin-top: 6px; }
    .match-bar-fill { height: 100%; border-radius: 4px; transition: width 0.6s ease; }

    .signal-tag {
        display: inline-block; padding: 3px 10px; border-radius: 100px;
        font-size: 11px; font-weight: 500; letter-spacing: 0.02em;
        margin-right: 6px; margin-bottom: 4px;
        background: #1e1e22; border: 1px solid #2a2a2e; color: #a1a1aa;
    }

    /* Search param tags */
    .param-tag {
        display: inline-flex; align-items: center; gap: 6px;
        padding: 5px 12px; background: #12120f; border: 1px solid #292524;
        border-radius: 8px; font-size: 12px; color: #d6d3d1;
        margin-right: 6px; margin-bottom: 6px;
    }
    .param-label { color: #78716c; }
    .kpi-tag { background: #0f1115; border-color: #1e2433; }

    /* Stat cards */
    .stat-row { display: flex; gap: 16px; margin: 16px 0 24px; }
    .stat-card {
        background: #111113; border: 1px solid #1e1e22;
        border-radius: 12px; padding: 14px 20px; min-width: 110px;
    }
    .stat-label {
        font-size: 10px; color: #71717a; font-weight: 600;
        text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 4px;
    }
    .stat-value {
        font-size: 22px; font-weight: 700; color: #fafafa;
        font-family: 'JetBrains Mono', monospace !important;
    }

    /* Expander override */
    .detail-row {
        display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 16px;
        padding: 12px 0 4px;
    }
    .detail-label {
        font-size: 10px; color: #52525b; font-weight: 600;
        text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 4px;
    }
    .detail-value { font-size: 13px; color: #d4d4d8; }

    /* Disclaimer */
    .disclaimer {
        margin-top: 24px; padding: 14px 20px; background: #111113;
        border-radius: 10px; border: 1px solid #1e1e22;
        font-size: 12px; color: #52525b; line-height: 1.5;
    }

    /* Input overrides */
    .stSelectbox > div > div { background: #111113 !important; border-color: #27272a !important; }
    .stTextInput > div > div > input { background: #111113 !important; border-color: #27272a !important; color: #e4e4e7 !important; }
    .stSlider > div > div > div { color: #71717a !important; }

    /* Button overrides */
    .stButton > button {
        width: 100%; padding: 14px 24px; border-radius: 12px;
        background: linear-gradient(135deg, #2563eb, #1d4ed8) !important;
        color: white !important; font-weight: 600 !important;
        font-size: 15px !important; border: none !important;
        transition: all 0.2s ease;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #3b82f6, #2563eb) !important;
        box-shadow: 0 8px 30px rgba(37,99,235,0.25);
    }
    .stButton > button:disabled { opacity: 0.35 !important; }

    /* Center the input form */
    .input-centered { max-width: 560px; margin: 0 auto; }

    /* Logo */
    .logo-icon {
        display: inline-flex; align-items: center; justify-content: center;
        width: 44px; height: 44px; border-radius: 12px;
        background: linear-gradient(135deg, #1e3a5f, #172554);
        border: 1px solid #1e3a5f; margin-bottom: 12px; font-size: 20px; color: #60a5fa;
    }

    /* Spinner override */
    .stSpinner > div { border-top-color: #3b82f6 !important; }
</style>
""", unsafe_allow_html=True)


# ─── Session State Init ──────────────────────────────────────
if "screen" not in st.session_state:
    st.session_state.screen = "input"
if "results" not in st.session_state:
    st.session_state.results = []
if "search_params" not in st.session_state:
    st.session_state.search_params = {}


# ─── INPUT SCREEN ────────────────────────────────────────────
def render_input():
    st.markdown('<div class="input-centered">', unsafe_allow_html=True)

    # Header
    st.markdown("""
    <div style="text-align: center; margin-bottom: 32px;">
        <div class="logo-icon">◆</div>
        <h1 style="font-size: 26px; margin-bottom: 4px;">Deal Sourcing</h1>
        <p style="color: #52525b; font-size: 14px;">AI-powered research to find your next investment</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Industry ──
    st.markdown('<div class="field-label">INDUSTRY</div>', unsafe_allow_html=True)
    industry = st.selectbox(
        "Industry",
        options=[""] + INDUSTRIES,
        format_func=lambda x: "Select an industry..." if x == "" else x,
        label_visibility="collapsed",
    )
    custom_industry = st.text_input(
        "Or type a custom industry",
        placeholder="Or type a custom industry...",
        label_visibility="collapsed",
    )
    selected_industry = custom_industry.strip() if custom_industry.strip() else industry

    st.markdown("<div style='height: 8px'></div>", unsafe_allow_html=True)

    # ── Stage ──
    st.markdown('<div class="field-label">STAGE · select one or more</div>', unsafe_allow_html=True)
    selected_stages = st.multiselect(
        "Stages",
        options=STAGES,
        default=[],
        label_visibility="collapsed",
    )

    st.markdown("<div style='height: 8px'></div>", unsafe_allow_html=True)

    # ── Geography ──
    st.markdown('<div class="field-label">GEOGRAPHY</div>', unsafe_allow_html=True)
    geo = st.selectbox(
        "Geography",
        options=GEOS,
        label_visibility="collapsed",
    )

    st.markdown("<div style='height: 8px'></div>", unsafe_allow_html=True)

    # ── KPIs ──
    available_kpis = []
    seen = set()
    for stage in selected_stages:
        for kpi in STAGE_KPIS.get(stage, []):
            if kpi not in seen:
                seen.add(kpi)
                available_kpis.append(kpi)

    kpi_count_text = f" · select which to score against" if available_kpis else ""
    st.markdown(f'<div class="field-label">SCORING KPIS{kpi_count_text}</div>', unsafe_allow_html=True)

    selected_kpis = []
    if not available_kpis:
        st.markdown("""
        <div style="padding: 20px; text-align: center; color: #3f3f46; font-size: 13px;
                    border: 1px dashed #27272a; border-radius: 10px;">
            Select a stage above to load relevant KPIs
        </div>
        """, unsafe_allow_html=True)
    else:
        selected_kpis = st.multiselect(
            "KPIs",
            options=available_kpis,
            default=[],
            label_visibility="collapsed",
        )

    # Custom KPI
    if available_kpis:
        custom_kpi = st.text_input(
            "Add custom KPI",
            placeholder="+ Add a custom KPI...",
            label_visibility="collapsed",
        )
        if custom_kpi.strip() and custom_kpi.strip() not in selected_kpis:
            selected_kpis.append(custom_kpi.strip())

    st.markdown("<div style='height: 8px'></div>", unsafe_allow_html=True)

    # ── Result count ──
    st.markdown('<div class="field-label">NUMBER OF RESULTS</div>', unsafe_allow_html=True)
    result_count = st.slider(
        "Results",
        min_value=5,
        max_value=25,
        value=10,
        step=5,
        label_visibility="collapsed",
    )

    st.markdown("<div style='height: 16px'></div>", unsafe_allow_html=True)

    # ── Search button ──
    api_key = st.secrets.get("ANTHROPIC_API_KEY", "")
    can_search = bool(selected_industry) and len(selected_stages) > 0 and len(selected_kpis) > 0 and bool(api_key)

    if not api_key:
        st.markdown("""
        <div style="padding: 14px 20px; background: #1a1212; border: 1px solid #3b1c1c; border-radius: 10px;
                    font-size: 13px; color: #f87171; margin-bottom: 16px;">
            ⚠️ API key not configured. Add ANTHROPIC_API_KEY to .streamlit/secrets.toml
        </div>
        """, unsafe_allow_html=True)

    def start_search():
        st.session_state.search_params = {
            "industry": selected_industry,
            "stages": selected_stages,
            "geo": geo,
            "kpis": selected_kpis,
            "result_count": result_count,
            "api_key": api_key,
        }
        st.session_state.screen = "loading"

    if can_search:
        st.button(
            "🔍 Research Deals",
            use_container_width=True,
            on_click=start_search,
        )
    else:
        st.button(
            "Select industry, stage & KPIs to begin",
            disabled=True,
            use_container_width=True,
        )

    # Cost estimate
    st.markdown(
        f'<div style="text-align: center; margin-top: 12px; font-size: 12px; color: #3f3f46;">'
        f'Estimated cost: ~${result_count * 0.03:.2f} per search</div>',
        unsafe_allow_html=True,
    )

    st.markdown('</div>', unsafe_allow_html=True)


# ─── LOADING / RESEARCH SCREEN ──────────────────────────────
def render_loading():
    params = st.session_state.search_params

    scroll_to_top()

    st.markdown(f"""
    <div style="text-align: center; margin: 60px auto 8px; max-width: 400px;">
        <h2 style="color: #fafafa; font-size: 20px; margin-bottom: 8px;">Researching deals...</h2>
        <p style="color: #52525b; font-size: 13px; margin-bottom: 24px;">
            Searching {', '.join(params['stages'])} stage · {params['industry']} · {params['geo']}
        </p>
    </div>
    """, unsafe_allow_html=True)

    progress_bar = st.progress(0)
    status_text = st.empty()

    steps = [
        (10, "🔍 Constructing research queries..."),
        (25, "🌐 Scanning startup databases & news..."),
        (50, "👤 Analyzing founder backgrounds..."),
        (75, "📊 Scoring against your KPIs..."),
    ]

    def status_callback(msg):
        for pct, label in steps:
            if label.split(" ", 1)[1] in msg:
                progress_bar.progress(pct)
                break
        status_text.markdown(
            f'<p style="text-align:center; color:#60a5fa; font-size:13px; margin-top:8px;">{msg}</p>',
            unsafe_allow_html=True,
        )

    try:
        results = research_deals(
            api_key=params["api_key"],
            industry=params["industry"],
            stages=params["stages"],
            geo=params["geo"],
            kpis=params["kpis"],
            result_count=params["result_count"],
            status_callback=status_callback,
        )

        progress_bar.progress(100)
        status_text.markdown(
            f'<p style="text-align:center; color:#34d399; font-size:13px; margin-top:8px;">✅ Found {len(results)} deals!</p>',
            unsafe_allow_html=True,
        )

        if results:
            st.session_state.results = results
            st.session_state.screen = "results"
            st.rerun()
        else:
            st.warning("No results found matching your exact stage and KPI criteria. Try broadening your search.")

            def go_back_no_results():
                st.session_state.screen = "input"

            st.button("← Back to Search", on_click=go_back_no_results, key="back_no_results")

    except Exception as e:
        progress_bar.empty()
        st.error(f"Research failed: {str(e)}")

        def go_back_error():
            st.session_state.screen = "input"

        st.button("← Back to Search", on_click=go_back_error, key="back_error")


# ─── RESULTS SCREEN ─────────────────────────────────────────
def render_results():
    params = st.session_state.search_params
    results = st.session_state.results

    scroll_to_top()

    # ── Header ──
    col_left, col_right = st.columns([3, 1])
    with col_left:
        def go_back():
            st.session_state.screen = "input"
            st.session_state.results = []

        st.button("← New Search", on_click=go_back)

        st.markdown(f"""
        <div style="margin-top: 8px;">
            <span style="font-size: 22px; font-weight: 700; color: #fafafa;">Results</span>
            <span style="padding: 3px 10px; border-radius: 6px; font-size: 11px; font-weight: 600;
                         background: linear-gradient(135deg, #1e3a5f, #1e293b);
                         color: #60a5fa; border: 1px solid #1e3a5f;
                         letter-spacing: 0.04em; text-transform: uppercase; margin-left: 8px;">
                {len(results)} found
            </span>
        </div>
        <p style="font-size: 13px; color: #71717a; margin-top: 4px;">
            {datetime.now().strftime("%b %d, %Y")}
        </p>
        """, unsafe_allow_html=True)

    # ── Params display ──
    params_html = ""
    params_html += f'<span class="param-tag"><span class="param-label">Industry:</span> {params["industry"]}</span>'
    params_html += f'<span class="param-tag"><span class="param-label">Stage:</span> {", ".join(params["stages"])}</span>'
    params_html += f'<span class="param-tag"><span class="param-label">Geo:</span> {params["geo"]}</span>'
    for kpi in params["kpis"]:
        params_html += f'<span class="param-tag kpi-tag"><span style="color:#60a5fa;">✦</span> {kpi}</span>'
    st.markdown(f'<div style="margin: 12px 0 8px;">{params_html}</div>', unsafe_allow_html=True)

    # ── Stats row ──
    avg_match = round(sum(r["kpi_match"] for r in results) / len(results)) if results else 0
    stage_counts = {}
    regions = set()
    for r in results:
        stage_counts[r["stage"]] = stage_counts.get(r["stage"], 0) + 1
        loc_parts = r["location"].split(", ")
        if len(loc_parts) > 1:
            regions.add(loc_parts[-1])
        else:
            regions.add(r["location"])

    stat_style = "background:#111113; border:1px solid #1e1e22; border-radius:12px; padding:14px 20px; min-width:110px; display:inline-block; margin-right:12px; margin-bottom:8px;"
    stat_label_style = "font-size:10px; color:#71717a; font-weight:600; text-transform:uppercase; letter-spacing:0.06em; margin-bottom:4px;"
    stat_val_style = "font-size:22px; font-weight:700; color:#fafafa; font-family:'JetBrains Mono',monospace;"

    stats_html = f'<div style="display:flex; flex-wrap:wrap; gap:12px; margin:16px 0 24px;">'
    stats_html += f'<div style="{stat_style}"><div style="{stat_label_style}">Avg Match</div><div style="{stat_val_style} color:#34d399;">{avg_match}%</div></div>'
    for stage, count in stage_counts.items():
        stats_html += f'<div style="{stat_style}"><div style="{stat_label_style}">{stage}</div><div style="{stat_val_style}">{count}</div></div>'
    stats_html += f'<div style="{stat_style}"><div style="{stat_label_style}">Regions</div><div style="{stat_val_style}">{len(regions)}</div></div>'
    stats_html += '</div>'
    st.markdown(stats_html, unsafe_allow_html=True)

    # ── Results cards ──
    for i, company in enumerate(results):
        score = company["kpi_match"]
        score_class = "match-high" if score >= 85 else "match-mid" if score >= 75 else "match-low"
        bar_color = "#10b981" if score >= 85 else "#f59e0b" if score >= 75 else "#ef4444"

        signals_html = "".join(f'<span class="signal-tag">{s}</span>' for s in company["signals"])

        st.markdown(f"""
        <div class="result-card">
            <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                <div style="flex: 1;">
                    <div class="company-name">{company["name"]}</div>
                    <div class="company-domain">{company["domain"]}</div>
                    <div class="company-meta">
                        {company["stage"]} · {company["location"]} · {company["last_round"]}
                    </div>
                </div>
                <div style="text-align: right; min-width: 70px;">
                    <div class="match-score {score_class}">{score}%</div>
                    <div class="match-bar">
                        <div class="match-bar-fill" style="width: {score}%; background: {bar_color};"></div>
                    </div>
                </div>
            </div>
            <div class="rationale">{company["rationale"]}</div>
            <div>{signals_html}</div>
        </div>
        """, unsafe_allow_html=True)

        if st.checkbox(f"Show details: {company['name']}", key=f"details_{i}"):
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f"""
                <div class="detail-label">FOUNDERS</div>
                <div class="detail-value">{company["founders"]}</div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown(f"""
                <div class="detail-label">FOUNDED</div>
                <div class="detail-value">{company["founded"]}</div>
                """, unsafe_allow_html=True)
            with col3:
                st.markdown(f"""
                <div class="detail-label">SOURCES</div>
                <div class="detail-value" style="color: #71717a;">{company["source"]}</div>
                """, unsafe_allow_html=True)

    # ── Export CSV ──
    st.markdown("<div style='height: 16px'></div>", unsafe_allow_html=True)

    df = pd.DataFrame([
        {
            "Company": r["name"],
            "Domain": r["domain"],
            "Stage": r["stage"],
            "Location": r["location"],
            "Founded": r["founded"],
            "Last Round": r["last_round"],
            "Founders": r["founders"],
            "KPI Match": f'{r["kpi_match"]}%',
            "Signals": ", ".join(r["signals"]),
            "Rationale": r["rationale"],
            "Source": r["source"],
        }
        for r in results
    ])

    csv = df.to_csv(index=False)
    st.download_button(
        label="📥 Export CSV",
        data=csv,
        file_name=f"deal-sourcing-{params['industry'].lower().replace(' ', '-')}-{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv",
        use_container_width=True,
    )

    # ── Disclaimer ──
    st.markdown("""
    <div class="disclaimer">
        ⚠️ Data sourced from public web results via AI research.
        Verify funding details independently before outreach.
        Match scores are AI-estimated based on your KPI criteria.
    </div>
    """, unsafe_allow_html=True)


# ─── ROUTER ──────────────────────────────────────────────────
if st.session_state.screen == "input":
    render_input()
elif st.session_state.screen == "loading":
    render_loading()
elif st.session_state.screen == "results":
    render_results()
