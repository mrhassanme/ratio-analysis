import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from io import BytesIO

st.set_page_config(
    page_title="Financial Analysis Tool",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# Custom CSS
# --------------------------------------------------
st.markdown("""
<style>
    .main { padding: 1rem 2rem; }
    .metric-card {
        background: #f8f9fa;
        border-left: 4px solid #4C72B0;
        padding: 0.75rem 1rem;
        border-radius: 6px;
        margin-bottom: 0.5rem;
    }
    .red-flag {
        background: #fff5f5;
        border-left: 4px solid #e53e3e;
        padding: 0.5rem 1rem;
        border-radius: 6px;
        margin-bottom: 0.4rem;
    }
    .green-flag {
        background: #f0fff4;
        border-left: 4px solid #38a169;
        padding: 0.5rem 1rem;
        border-radius: 6px;
    }
    .section-header {
        font-size: 1.3rem;
        font-weight: 700;
        color: #2d3748;
        margin-top: 1.5rem;
        margin-bottom: 0.75rem;
        border-bottom: 2px solid #e2e8f0;
        padding-bottom: 0.4rem;
    }
    div[data-testid="stNumberInput"] label { font-size: 0.85rem; }
    .stDataFrame { border-radius: 8px; overflow: hidden; }
</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# Utility Functions
# --------------------------------------------------

def safe_div(n, d):
    return n / d if d and d != 0 else 0

def pct(n, d):
    return safe_div(n, d) * 100

def growth(current, previous):
    if previous == 0:
        return 0.0
    return ((current - previous) / abs(previous)) * 100

def avg(a, b):
    return (a + b) / 2 if (a + b) != 0 else 0

def color_change(val):
    if val > 0:
        return "color: #38a169; font-weight:600"
    elif val < 0:
        return "color: #e53e3e; font-weight:600"
    return "color: #718096"

def highlight_ratio(val, low, high, reverse=False):
    """Highlights ratio cells green/yellow/red based on benchmarks."""
    try:
        v = float(val)
    except Exception:
        return ""
    if reverse:
        good = v <= low
        warn = low < v <= high
    else:
        good = v >= high
        warn = low <= v < high
    if good:
        return "background-color: #c6f6d5; color: #22543d"
    elif warn:
        return "background-color: #fefcbf; color: #744210"
    else:
        return "background-color: #fed7d7; color: #742a2a"


# --------------------------------------------------
# SIDEBAR — Company Info & Settings
# --------------------------------------------------

with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/financial-analytics.png", width=60)
    st.title("⚙️ Settings")
    company_name = st.text_input("Company Name", placeholder="e.g. ABC Corp")
    industry = st.selectbox("Industry", [
        "General", "Manufacturing", "Retail", "Technology",
        "Banking/Finance", "Healthcare", "Real Estate", "Energy"
    ])
    currency = st.selectbox("Currency", ["USD ($)", "GBP (£)", "EUR (€)", "MYR (RM)", "INR (₹)", "SGD (S$)"])
    curr_sym = currency.split("(")[1].replace(")", "").strip()

    st.markdown("---")
    st.markdown("**📘 Guide**")
    st.info(
        "1. Enter Current & Previous Year data\n"
        "2. Click **Run Full Analysis**\n"
        "3. Review ratios, flags & charts\n"
        "4. Export to Excel"
    )


# --------------------------------------------------
# HEADER
# --------------------------------------------------

title = f"📊 Financial Analysis — {company_name}" if company_name else "📊 Advanced Financial Analysis Tool"
st.title(title)
st.caption("Comprehensive ratio analysis, horizontal & vertical analysis, red flag detection, and charting.")
st.markdown("---")


# --------------------------------------------------
# INPUT SECTION — Tabs for clean separation
# --------------------------------------------------

st.markdown('<div class="section-header">📥 Enter Financial Data</div>', unsafe_allow_html=True)

tab_is, tab_bs, tab_cf, tab_extra = st.tabs([
    "📋 Income Statement", "🏦 Balance Sheet", "💵 Cash Flow", "➕ Additional Inputs"
])

def two_col_input(label, key, help_text=""):
    c1, c2, c3 = st.columns([2.5, 1, 1])
    c1.markdown(f"**{label}**")
    if help_text:
        c1.caption(help_text)
    cy = c2.number_input(f"CY", value=0.0, step=1.0, format="%.2f", key=f"{key}_cy", label_visibility="collapsed")
    py = c3.number_input(f"PY", value=0.0, step=1.0, format="%.2f", key=f"{key}_py", label_visibility="collapsed")
    return cy, py

with tab_is:
    st.markdown(
        "<div style='display:grid;grid-template-columns:2.5fr 1fr 1fr;"
        "font-weight:700;color:#555;padding:0 0 8px 0'>"
        "<span>Item</span><span>Current Year</span><span>Previous Year</span></div>",
        unsafe_allow_html=True
    )
    cy_revenue,     py_revenue     = two_col_input("Revenue / Sales", "revenue")
    cy_cogs,        py_cogs        = two_col_input("Cost of Goods Sold (COGS)", "cogs")
    cy_gross,       py_gross       = two_col_input("Gross Profit", "gross", "Leave 0 to auto-calculate from Revenue - COGS")
    cy_ebitda,      py_ebitda      = two_col_input("EBITDA", "ebitda")
    cy_ebit,        py_ebit        = two_col_input("EBIT", "ebit")
    cy_interest,    py_interest    = two_col_input("Finance Cost / Interest Expense", "interest")
    cy_tax,         py_tax         = two_col_input("Tax Expense", "tax")
    cy_pbt,         py_pbt         = two_col_input("Profit Before Tax (PBT)", "pbt")
    cy_pat,         py_pat         = two_col_input("Profit After Tax (PAT) / Net Income", "pat")
    cy_sga,         py_sga         = two_col_input("SG&A Expenses", "sga")
    cy_depreciation,py_depreciation= two_col_input("Depreciation Expense", "depreciation")

with tab_bs:
    st.markdown(
        "<div style='display:grid;grid-template-columns:2.5fr 1fr 1fr;"
        "font-weight:700;color:#555;padding:0 0 8px 0'>"
        "<span>Item</span><span>Current Year</span><span>Previous Year</span></div>",
        unsafe_allow_html=True
    )
    cy_cash,           py_cash           = two_col_input("Cash & Bank Balances", "cash")
    cy_receivables,    py_receivables    = two_col_input("Trade Receivables", "receivables")
    cy_inventory,      py_inventory      = two_col_input("Inventory", "inventory")
    cy_current_assets, py_current_assets = two_col_input("Total Current Assets", "current_assets")
    cy_total_assets,   py_total_assets   = two_col_input("Total Assets", "total_assets")
    cy_gross_ppe,      py_gross_ppe      = two_col_input("Gross PP&E", "gross_ppe")
    cy_net_ppe,        py_net_ppe        = two_col_input("Net Fixed Assets / Net PP&E", "net_ppe")
    cy_current_liab,   py_current_liab   = two_col_input("Current Liabilities", "current_liab")
    cy_st_debt,        py_st_debt        = two_col_input("Short-Term Debt", "st_debt")
    cy_lt_debt,        py_lt_debt        = two_col_input("Long-Term Debt", "lt_debt")
    cy_total_debt,     py_total_debt     = two_col_input("Total Debt", "total_debt")
    cy_total_liab,     py_total_liab     = two_col_input("Total Liabilities", "total_liab")
    cy_equity,         py_equity         = two_col_input("Total Equity", "equity")
    cy_retained,       py_retained       = two_col_input("Retained Earnings", "retained")
    cy_payables,       py_payables       = two_col_input("Trade Payables", "payables")

with tab_cf:
    st.markdown(
        "<div style='display:grid;grid-template-columns:2.5fr 1fr 1fr;"
        "font-weight:700;color:#555;padding:0 0 8px 0'>"
        "<span>Item</span><span>Current Year</span><span>Previous Year</span></div>",
        unsafe_allow_html=True
    )
    cy_ocf, py_ocf = two_col_input("Operating Cash Flow (CFO)", "ocf")
    cy_icf, py_icf = two_col_input("Investing Cash Flow", "icf")
    cy_fcf, py_fcf = two_col_input("Financing Cash Flow", "fcf")

with tab_extra:
    st.markdown(
        "<div style='display:grid;grid-template-columns:2.5fr 1fr 1fr;"
        "font-weight:700;color:#555;padding:0 0 8px 0'>"
        "<span>Item</span><span>Current Year</span><span>Previous Year</span></div>",
        unsafe_allow_html=True
    )
    cy_credit_sales, py_credit_sales = two_col_input("Credit Sales (for Receivable Days)", "credit_sales",
                                                      "Leave 0 to use Total Revenue as proxy")

    st.info("💡 Average figures are auto-calculated as (Current Year + Previous Year) / 2")


# --------------------------------------------------
# RUN ANALYSIS BUTTON
# --------------------------------------------------

st.markdown("---")
run = st.button("🚀 Run Full Analysis", type="primary", use_container_width=True)

if run:

    # Auto-fill derived values
    cy_gross_profit  = cy_gross if cy_gross != 0 else cy_revenue - cy_cogs
    py_gross_profit  = py_gross if py_gross != 0 else py_revenue - py_cogs

    credit_sales_cy  = cy_credit_sales if cy_credit_sales != 0 else cy_revenue
    credit_sales_py  = py_credit_sales if py_credit_sales != 0 else py_revenue

    avg_inventory    = avg(cy_inventory, py_inventory)
    avg_receivables  = avg(cy_receivables, py_receivables)
    avg_payables     = avg(cy_payables, py_payables)
    avg_equity       = avg(cy_equity, py_equity)
    avg_total_assets = avg(cy_total_assets, py_total_assets)

    working_capital  = cy_current_assets - cy_current_liab
    py_wc            = py_current_assets - py_current_liab


    # ==============================================================
    # 1️⃣ RATIO ANALYSIS
    # ==============================================================

    st.markdown('<div class="section-header">📊 Ratio Analysis</div>', unsafe_allow_html=True)

    # --- Calculate all ratios ---

    # Profitability
    roce_cy  = pct(cy_ebit, cy_total_assets - cy_current_liab)
    roe_cy   = pct(cy_pat, avg_equity)
    roa_cy   = pct(cy_pat, avg_total_assets)
    gpm_cy   = pct(cy_gross_profit, cy_revenue)
    npm_cy   = pct(cy_pat, cy_revenue)
    ebitda_m_cy = pct(cy_ebitda, cy_revenue)

    roce_py  = pct(py_ebit, py_total_assets - py_current_liab)
    roe_py   = pct(py_pat, py_equity)
    roa_py   = pct(py_pat, py_total_assets)
    gpm_py   = pct(py_gross_profit, py_revenue)
    npm_py   = pct(py_pat, py_revenue)
    ebitda_m_py = pct(py_ebitda, py_revenue)

    # Liquidity
    cr_cy  = safe_div(cy_current_assets, cy_current_liab)
    qr_cy  = safe_div(cy_current_assets - cy_inventory, cy_current_liab)
    cash_r_cy = safe_div(cy_cash, cy_current_liab)
    cr_py  = safe_div(py_current_assets, py_current_liab)
    qr_py  = safe_div(py_current_assets - py_inventory, py_current_liab)
    cash_r_py = safe_div(py_cash, py_current_liab)

    # Leverage
    de_cy  = safe_div(cy_total_debt, cy_equity)
    gear_cy= pct(cy_lt_debt, cy_lt_debt + cy_equity)
    ic_cy  = safe_div(cy_ebit, cy_interest)
    de_py  = safe_div(py_total_debt, py_equity)
    gear_py= pct(py_lt_debt, py_lt_debt + py_equity)
    ic_py  = safe_div(py_ebit, py_interest)

    # Efficiency
    inv_turn_cy = safe_div(cy_cogs, avg_inventory)
    inv_days_cy = safe_div(avg_inventory, cy_cogs) * 365
    rec_days_cy = safe_div(avg_receivables, credit_sales_cy) * 365
    pay_days_cy = safe_div(avg_payables, cy_cogs) * 365
    wcc_cy      = inv_days_cy + rec_days_cy - pay_days_cy
    at_cy       = safe_div(cy_revenue, cy_total_assets)
    fat_cy      = safe_div(cy_revenue, cy_net_ppe)

    inv_turn_py = safe_div(py_cogs, avg(py_inventory, 0))
    inv_days_py = safe_div(py_inventory, py_cogs) * 365
    rec_days_py = safe_div(py_receivables, credit_sales_py) * 365
    pay_days_py = safe_div(py_payables, py_cogs) * 365
    wcc_py      = inv_days_py + rec_days_py - pay_days_py
    at_py       = safe_div(py_revenue, py_total_assets)
    fat_py      = safe_div(py_revenue, py_net_ppe)

    # Cash Flow
    ocf_cl_cy  = safe_div(cy_ocf, cy_current_liab)
    ocf_np_cy  = safe_div(cy_ocf, cy_pat)
    ccr_cy     = safe_div(cy_ocf, cy_ebitda)
    cfo_debt_cy= safe_div(cy_ocf, cy_total_debt)
    ocf_cl_py  = safe_div(py_ocf, py_current_liab)
    ocf_np_py  = safe_div(py_ocf, py_pat)
    ccr_py     = safe_div(py_ocf, py_ebitda)
    cfo_debt_py= safe_div(py_ocf, py_total_debt)

    # Quality / Other
    eff_tax_cy = pct(cy_tax, cy_pbt)
    sga_s_cy   = pct(cy_sga, cy_revenue)
    dep_rate_cy= pct(cy_depreciation, cy_gross_ppe)
    accruals_cy= pct(cy_pat - cy_ocf, cy_total_assets)
    eff_tax_py = pct(py_tax, py_pbt)
    sga_s_py   = pct(py_sga, py_revenue)
    dep_rate_py= pct(py_depreciation, py_gross_ppe)
    accruals_py= pct(py_pat - py_ocf, py_total_assets)

    # Altman Z-Score
    def altman(wc, ta, re, ebit, equity, tl, sales):
        if ta == 0 or tl == 0:
            return 0
        return (1.2*(wc/ta) + 1.4*(re/ta) + 3.3*(ebit/ta) +
                0.6*(equity/tl) + 1.0*(sales/ta))

    z_cy = altman(working_capital, cy_total_assets, cy_retained,
                  cy_ebit, cy_equity, cy_total_liab, cy_revenue)
    z_py = altman(py_wc, py_total_assets, py_retained,
                  py_ebit, py_equity, py_total_liab, py_revenue)

    # --- Build Ratio DataFrames ---

    ratio_groups = {
        "📈 Profitability": {
            "data": {
                "ROCE (%)":             (roce_cy,  roce_py),
                "ROE (%)":              (roe_cy,   roe_py),
                "ROA (%)":              (roa_cy,   roa_py),
                "Gross Profit Margin (%)": (gpm_cy, gpm_py),
                "Net Profit Margin (%)":   (npm_cy,  npm_py),
                "EBITDA Margin (%)":       (ebitda_m_cy, ebitda_m_py),
            },
            "benchmarks": {"low": 5, "high": 15}
        },
        "💧 Liquidity": {
            "data": {
                "Current Ratio":  (cr_cy,     cr_py),
                "Quick Ratio":    (qr_cy,     qr_py),
                "Cash Ratio":     (cash_r_cy, cash_r_py),
                "Working Capital (abs)": (working_capital, py_wc),
            },
            "benchmarks": {"low": 1.0, "high": 1.5}
        },
        "⚖️ Leverage": {
            "data": {
                "Debt to Equity":   (de_cy,   de_py),
                "Gearing Ratio (%)": (gear_cy, gear_py),
                "Interest Coverage": (ic_cy,   ic_py),
            },
            "benchmarks": {"low": 1, "high": 3}
        },
        "⚙️ Efficiency": {
            "data": {
                "Inventory Turnover (x)": (inv_turn_cy, inv_turn_py),
                "Inventory Days":         (inv_days_cy, inv_days_py),
                "Receivable Days":        (rec_days_cy, rec_days_py),
                "Payable Days":           (pay_days_cy, pay_days_py),
                "Working Capital Cycle":  (wcc_cy,      wcc_py),
                "Asset Turnover (x)":     (at_cy,       at_py),
                "Fixed Asset Turnover (x)":(fat_cy,     fat_py),
            },
            "benchmarks": {"low": 1, "high": 2}
        },
        "💵 Cash Flow": {
            "data": {
                "OCF Ratio":             (ocf_cl_cy,   ocf_cl_py),
                "OCF to Net Profit":     (ocf_np_cy,   ocf_np_py),
                "Cash Conversion Ratio": (ccr_cy,      ccr_py),
                "CFO to Total Debt":     (cfo_debt_cy, cfo_debt_py),
            },
            "benchmarks": {"low": 0.5, "high": 1.0}
        },
        "🔬 Quality & Other": {
            "data": {
                "Effective Tax Rate (%)":  (eff_tax_cy, eff_tax_py),
                "SG&A to Sales (%)":       (sga_s_cy,   sga_s_py),
                "Depreciation Rate (%)":   (dep_rate_cy, dep_rate_py),
                "Accruals to Assets (%)":  (accruals_cy, accruals_py),
                "Altman Z-Score":          (z_cy,        z_py),
            },
            "benchmarks": {"low": 0, "high": 0}
        }
    }

    for group_name, group_info in ratio_groups.items():
        with st.expander(group_name, expanded=True):
            df = pd.DataFrame(group_info["data"], index=["Current Year", "Previous Year"]).T
            df["Change"] = df["Current Year"] - df["Previous Year"]
            df["Change %"] = df.apply(
                lambda row: growth(row["Current Year"], row["Previous Year"]), axis=1
            )
            st.dataframe(
                df.style
                  .format("{:.2f}")
                  .applymap(lambda v: color_change(v), subset=["Change", "Change %"]),
                use_container_width=True
            )


    # ==============================================================
    # 2️⃣ HORIZONTAL ANALYSIS
    # ==============================================================

    st.markdown('<div class="section-header">📈 Horizontal Analysis (Year-on-Year %)</div>',
                unsafe_allow_html=True)

    horiz_items = {
        "Revenue":             (cy_revenue,       py_revenue),
        "Gross Profit":        (cy_gross_profit,  py_gross_profit),
        "EBIT":                (cy_ebit,          py_ebit),
        "Net Income / PAT":    (cy_pat,           py_pat),
        "Total Assets":        (cy_total_assets,  py_total_assets),
        "Total Liabilities":   (cy_total_liab,    py_total_liab),
        "Equity":              (cy_equity,        py_equity),
        "Operating Cash Flow": (cy_ocf,           py_ocf),
        "Trade Receivables":   (cy_receivables,   py_receivables),
        "Inventory":           (cy_inventory,     py_inventory),
        "Total Debt":          (cy_total_debt,    py_total_debt),
    }

    horiz_data = []
    for item, (cy, py) in horiz_items.items():
        g = growth(cy, py)
        horiz_data.append({
            "Item": item,
            f"Previous Year ({curr_sym})": py,
            f"Current Year ({curr_sym})": cy,
            "Change (%)": g,
            "Trend": "▲" if g > 0 else ("▼" if g < 0 else "—")
        })

    df_horiz = pd.DataFrame(horiz_data)

    st.dataframe(
        df_horiz.style
          .format({
              f"Previous Year ({curr_sym})": "{:,.2f}",
              f"Current Year ({curr_sym})": "{:,.2f}",
              "Change (%)": "{:.2f}"
          })
          .applymap(lambda v: color_change(v), subset=["Change (%)"]),
        use_container_width=True,
        hide_index=True
    )

    # Horizontal Bar Chart
    fig_horiz = px.bar(
        df_horiz,
        x="Change (%)", y="Item", orientation="h",
        color="Change (%)",
        color_continuous_scale=["#e53e3e", "#ecc94b", "#38a169"],
        title="Year-on-Year Growth (%)",
        text="Change (%)"
    )
    fig_horiz.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    fig_horiz.update_layout(
        height=400, showlegend=False,
        plot_bgcolor="white", paper_bgcolor="white",
        coloraxis_showscale=False
    )
    st.plotly_chart(fig_horiz, use_container_width=True)


    # ==============================================================
    # 3️⃣ VERTICAL ANALYSIS
    # ==============================================================

    st.markdown('<div class="section-header">📊 Vertical Analysis (Common Size)</div>',
                unsafe_allow_html=True)

    v_col1, v_col2 = st.columns(2)

    with v_col1:
        st.subheader("Income Statement (% of Revenue)")
        inc_vert_items = {
            "Revenue":     (100.0,                       100.0),
            "COGS":        (pct(cy_cogs, cy_revenue),    pct(py_cogs, py_revenue)),
            "Gross Profit":(pct(cy_gross_profit, cy_revenue), pct(py_gross_profit, py_revenue)),
            "SG&A":        (pct(cy_sga, cy_revenue),     pct(py_sga, py_revenue)),
            "EBIT":        (pct(cy_ebit, cy_revenue),    pct(py_ebit, py_revenue)),
            "Interest":    (pct(cy_interest, cy_revenue),pct(py_interest, py_revenue)),
            "Tax":         (pct(cy_tax, cy_revenue),     pct(py_tax, py_revenue)),
            "Net Income":  (pct(cy_pat, cy_revenue),     pct(py_pat, py_revenue)),
        }
        df_inc_vert = pd.DataFrame(inc_vert_items, index=["CY %", "PY %"]).T
        st.dataframe(df_inc_vert.style.format("{:.2f}"), use_container_width=True)

        # Waterfall-style bar for income composition
        fig_inc = go.Figure(go.Bar(
            y=list(inc_vert_items.keys()),
            x=[v[0] for v in inc_vert_items.values()],
            orientation='h',
            marker_color="#4C72B0",
            name="Current Year %"
        ))
        fig_inc.update_layout(
            title="Income Statement — Current Year %",
            height=300, plot_bgcolor="white",
            paper_bgcolor="white", margin=dict(l=20, r=20, t=40, b=20)
        )
        st.plotly_chart(fig_inc, use_container_width=True)

    with v_col2:
        st.subheader("Balance Sheet (% of Total Assets)")
        bs_vert_items = {
            "Cash":              (pct(cy_cash, cy_total_assets),           pct(py_cash, py_total_assets)),
            "Receivables":       (pct(cy_receivables, cy_total_assets),    pct(py_receivables, py_total_assets)),
            "Inventory":         (pct(cy_inventory, cy_total_assets),      pct(py_inventory, py_total_assets)),
            "Current Assets":    (pct(cy_current_assets, cy_total_assets), pct(py_current_assets, py_total_assets)),
            "Net Fixed Assets":  (pct(cy_net_ppe, cy_total_assets),        pct(py_net_ppe, py_total_assets)),
            "Current Liab.":     (pct(cy_current_liab, cy_total_assets),   pct(py_current_liab, py_total_assets)),
            "Total Liabilities": (pct(cy_total_liab, cy_total_assets),     pct(py_total_liab, py_total_assets)),
            "Equity":            (pct(cy_equity, cy_total_assets),         pct(py_equity, py_total_assets)),
        }
        df_bs_vert = pd.DataFrame(bs_vert_items, index=["CY %", "PY %"]).T
        st.dataframe(df_bs_vert.style.format("{:.2f}"), use_container_width=True)

        fig_bs = go.Figure()
        fig_bs.add_trace(go.Bar(
            y=list(bs_vert_items.keys()),
            x=[v[0] for v in bs_vert_items.values()],
            orientation='h', name="CY", marker_color="#4C72B0"
        ))
        fig_bs.add_trace(go.Bar(
            y=list(bs_vert_items.keys()),
            x=[v[1] for v in bs_vert_items.values()],
            orientation='h', name="PY", marker_color="#DD8452"
        ))
        fig_bs.update_layout(
            title="Balance Sheet — CY vs PY (%)",
            barmode="group", height=300,
            plot_bgcolor="white", paper_bgcolor="white",
            margin=dict(l=20, r=20, t=40, b=20)
        )
        st.plotly_chart(fig_bs, use_container_width=True)


    # ==============================================================
    # 4️⃣ TREND CHARTS
    # ==============================================================

    st.markdown('<div class="section-header">📉 Key Ratio Trends (CY vs PY)</div>',
                unsafe_allow_html=True)

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        # Profitability trend
        fig_prof = go.Figure()
        for label, cy_val, py_val in [
            ("Gross Margin %", gpm_cy, gpm_py),
            ("Net Margin %", npm_cy, npm_py),
            ("EBITDA Margin %", ebitda_m_cy, ebitda_m_py),
            ("ROE %", roe_cy, roe_py),
            ("ROA %", roa_cy, roa_py),
        ]:
            fig_prof.add_trace(go.Bar(
                name=label, x=["Previous Year", "Current Year"],
                y=[py_val, cy_val]
            ))
        fig_prof.update_layout(
            title="Profitability Margins (%)", barmode="group",
            height=350, plot_bgcolor="white", paper_bgcolor="white"
        )
        st.plotly_chart(fig_prof, use_container_width=True)

    with chart_col2:
        # Liquidity & Leverage trend
        fig_lev = go.Figure()
        for label, cy_val, py_val in [
            ("Current Ratio", cr_cy, cr_py),
            ("Quick Ratio", qr_cy, qr_py),
            ("Debt to Equity", de_cy, de_py),
            ("Interest Coverage", ic_cy, ic_py),
        ]:
            fig_lev.add_trace(go.Bar(
                name=label, x=["Previous Year", "Current Year"],
                y=[py_val, cy_val]
            ))
        fig_lev.update_layout(
            title="Liquidity & Leverage Ratios", barmode="group",
            height=350, plot_bgcolor="white", paper_bgcolor="white"
        )
        st.plotly_chart(fig_lev, use_container_width=True)

    # Working Capital Cycle Breakdown
    fig_wcc = go.Figure()
    fig_wcc.add_trace(go.Bar(
        name="Inventory Days",
        x=["Previous Year", "Current Year"],
        y=[inv_days_py, inv_days_cy], marker_color="#4C72B0"
    ))
    fig_wcc.add_trace(go.Bar(
        name="Receivable Days",
        x=["Previous Year", "Current Year"],
        y=[rec_days_py, rec_days_cy], marker_color="#55A868"
    ))
    fig_wcc.add_trace(go.Bar(
        name="Payable Days",
        x=["Previous Year", "Current Year"],
        y=[-pay_days_py, -pay_days_cy], marker_color="#DD8452"
    ))
    fig_wcc.update_layout(
        title="Working Capital Cycle (Days) — Payables offset as negative",
        barmode="relative", height=350,
        plot_bgcolor="white", paper_bgcolor="white"
    )
    st.plotly_chart(fig_wcc, use_container_width=True)


    # ==============================================================
    # 5️⃣ ALTMAN Z-SCORE GAUGE
    # ==============================================================

    st.markdown('<div class="section-header">🧮 Altman Z-Score</div>', unsafe_allow_html=True)

    def z_label(z):
        if z > 3.0:   return "✅ Safe Zone", "#38a169"
        elif z > 2.7: return "🟡 Caution Zone", "#d69e2e"
        elif z > 1.8: return "🟠 Distress Zone", "#dd6b20"
        else:         return "🔴 Danger Zone", "#e53e3e"

    z_lbl_cy, z_col_cy = z_label(z_cy)
    z_lbl_py, z_col_py = z_label(z_py)

    z1, z2 = st.columns(2)
    with z1:
        st.metric("Current Year Z-Score", f"{z_cy:.2f}", delta=f"{z_cy - z_py:.2f}")
        st.markdown(f"<span style='color:{z_col_cy};font-weight:700;font-size:1.1rem'>{z_lbl_cy}</span>",
                    unsafe_allow_html=True)
    with z2:
        st.metric("Previous Year Z-Score", f"{z_py:.2f}")
        st.markdown(f"<span style='color:{z_col_py};font-weight:700;font-size:1.1rem'>{z_lbl_py}</span>",
                    unsafe_allow_html=True)

    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=z_cy,
        delta={"reference": z_py, "valueformat": ".2f"},
        title={"text": "Altman Z-Score (Current Year)"},
        gauge={
            "axis": {"range": [0, 5]},
            "bar": {"color": "#4C72B0"},
            "steps": [
                {"range": [0, 1.8],  "color": "#fed7d7"},
                {"range": [1.8, 2.7],"color": "#fefcbf"},
                {"range": [2.7, 3.0],"color": "#feebc8"},
                {"range": [3.0, 5],  "color": "#c6f6d5"},
            ],
            "threshold": {"line": {"color": "black","width": 3}, "value": 3.0}
        }
    ))
    fig_gauge.update_layout(height=280, margin=dict(t=40, b=10))
    st.plotly_chart(fig_gauge, use_container_width=True)


    # ==============================================================
    # 6️⃣ RED FLAG ENGINE (Enhanced)
    # ==============================================================

    st.markdown('<div class="section-header">🚨 Red Flag & Health Check</div>',
                unsafe_allow_html=True)

    flags = []
    positives = []

    rev_growth    = growth(cy_revenue, py_revenue)
    rec_growth    = growth(cy_receivables, py_receivables)
    profit_growth = growth(cy_pat, py_pat)
    debt_growth   = growth(cy_total_debt, py_total_debt)

    # Liquidity
    if cr_cy < 1.0:
        flags.append(("🔴 Critical", "Current Ratio below 1.0 — Cannot cover short-term obligations"))
    elif cr_cy < 1.5:
        flags.append(("🟡 Warning", f"Current Ratio is low at {cr_cy:.2f} (target: ≥ 1.5)"))
    else:
        positives.append(f"Current Ratio is healthy at {cr_cy:.2f}")

    if qr_cy < 1.0:
        flags.append(("🟡 Warning", f"Quick Ratio below 1.0 at {qr_cy:.2f} — Limited liquid assets"))

    if working_capital < 0:
        flags.append(("🔴 Critical", "Negative Working Capital — Serious liquidity risk"))

    # Cash Flow
    if cy_ocf < 0:
        flags.append(("🔴 Critical", "Negative Operating Cash Flow — Business is burning cash from operations"))
    elif cy_ocf > cy_pat:
        positives.append("Operating Cash Flow exceeds Net Profit — Strong earnings quality")

    if cy_ocf < cy_pat * 0.8 and cy_pat > 0:
        flags.append(("🟡 Warning", "Operating CF is significantly lower than Net Profit — Possible earnings manipulation or weak cash conversion"))

    # Leverage
    if de_cy > 3.0:
        flags.append(("🔴 Critical", f"Debt-to-Equity at {de_cy:.2f} — Dangerously high leverage"))
    elif de_cy > 2.0:
        flags.append(("🟡 Warning", f"Debt-to-Equity at {de_cy:.2f} — High leverage (target: < 2.0)"))
    else:
        positives.append(f"Debt-to-Equity is manageable at {de_cy:.2f}")

    if ic_cy < 1.5 and cy_interest > 0:
        flags.append(("🔴 Critical", f"Interest Coverage of {ic_cy:.2f}x — At risk of defaulting on interest"))
    elif ic_cy < 3.0 and cy_interest > 0:
        flags.append(("🟡 Warning", f"Interest Coverage of {ic_cy:.2f}x — Should be above 3.0x"))

    # Revenue & Receivables Quality
    if rec_growth > rev_growth + 15:
        flags.append(("🟡 Warning", f"Receivables growing ({rec_growth:.1f}%) faster than Revenue ({rev_growth:.1f}%) — Potential collection issues"))

    if rev_growth > 0 and profit_growth < 0:
        flags.append(("🟡 Warning", "Revenue growing but profits declining — Margin compression or cost overruns"))

    if debt_growth > rev_growth + 20:
        flags.append(("🟡 Warning", f"Debt growing ({debt_growth:.1f}%) much faster than Revenue ({rev_growth:.1f}%)"))

    # Profitability
    if npm_cy < 0:
        flags.append(("🔴 Critical", "Negative Net Profit Margin — Company is loss-making"))
    elif npm_cy < 5:
        flags.append(("🟡 Warning", f"Net Profit Margin is very thin at {npm_cy:.1f}%"))

    # Accruals
    if abs(accruals_cy) > 5:
        flags.append(("🟡 Warning", f"High Accruals-to-Assets ({accruals_cy:.1f}%) — Earnings quality concern"))

    # Altman Z
    if z_cy < 1.8:
        flags.append(("🔴 Critical", f"Altman Z-Score of {z_cy:.2f} — High bankruptcy risk"))
    elif z_cy < 2.7:
        flags.append(("🟡 Warning", f"Altman Z-Score of {z_cy:.2f} — In financial distress zone"))
    elif z_cy > 3.0:
        positives.append(f"Altman Z-Score of {z_cy:.2f} — Company is in the safe zone")

    if npm_cy > npm_py and rev_growth > 0:
        positives.append("Profit margin improving alongside revenue growth — Quality performance")

    # Display
    crit_flags = [f for f in flags if f[0].startswith("🔴")]
    warn_flags = [f for f in flags if f[0].startswith("🟡")]

    fc1, fc2, fc3 = st.columns(3)
    fc1.metric("🔴 Critical Issues", len(crit_flags))
    fc2.metric("🟡 Warnings", len(warn_flags))
    fc3.metric("✅ Positives", len(positives))

    if crit_flags:
        st.markdown("**Critical Issues:**")
        for sev, msg in crit_flags:
            st.error(f"{sev}: {msg}")

    if warn_flags:
        st.markdown("**Warnings:**")
        for sev, msg in warn_flags:
            st.warning(f"{sev}: {msg}")

    if positives:
        st.markdown("**Positive Signals:**")
        for p in positives:
            st.success(f"✅ {p}")

    if not flags:
        st.success("✅ No major red flags detected. Financial health looks solid.")


    # ==============================================================
    # 7️⃣ EXPORT TO EXCEL
    # ==============================================================

    st.markdown('<div class="section-header">📤 Export Report</div>', unsafe_allow_html=True)

    output = BytesIO()

    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        workbook = writer.book

        # Formats
        header_fmt = workbook.add_format({
            'bold': True, 'bg_color': '#4C72B0', 'font_color': 'white',
            'border': 1, 'align': 'center'
        })
        green_fmt  = workbook.add_format({'bg_color': '#c6f6d5'})
        red_fmt    = workbook.add_format({'bg_color': '#fed7d7'})
        num_fmt    = workbook.add_format({'num_format': '#,##0.00'})

        # Sheet: Summary
        summary_data = {
            "Company": [company_name or "N/A"],
            "Industry": [industry],
            "Currency": [curr_sym],
            "Current Year Revenue": [cy_revenue],
            "Current Year Net Income": [cy_pat],
            "Gross Margin %": [gpm_cy],
            "Net Margin %": [npm_cy],
            "Current Ratio": [cr_cy],
            "Debt to Equity": [de_cy],
            "Altman Z-Score": [z_cy],
            "Critical Flags": [len(crit_flags)],
            "Warnings": [len(warn_flags)],
        }
        pd.DataFrame(summary_data).T.to_excel(writer, sheet_name='Summary', header=False)

        # Sheet: All Ratios
        all_ratios = {}
        for group_info in ratio_groups.values():
            all_ratios.update(group_info["data"])
        df_all = pd.DataFrame(all_ratios, index=["Current Year", "Previous Year"]).T
        df_all["Change"] = df_all["Current Year"] - df_all["Previous Year"]
        df_all.to_excel(writer, sheet_name='All Ratios')

        # Sheet: Horizontal
        df_horiz.to_excel(writer, sheet_name='Horizontal Analysis', index=False)

        # Sheet: Vertical - Income
        df_inc_vert.to_excel(writer, sheet_name='Vertical - Income')

        # Sheet: Vertical - Balance Sheet
        df_bs_vert.to_excel(writer, sheet_name='Vertical - Balance Sheet')

        # Sheet: Red Flags
        flags_data = [(sev, msg) for sev, msg in flags] + [("✅ Positive", p) for p in positives]
        pd.DataFrame(flags_data, columns=["Type", "Description"]).to_excel(
            writer, sheet_name='Red Flags', index=False
        )

    col_exp1, col_exp2 = st.columns([2, 1])
    col_exp1.download_button(
        label="📥 Download Excel Report",
        data=output.getvalue(),
        file_name=f"Financial_Analysis_{company_name or 'Report'}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True
    )
    col_exp2.info(f"Report includes {len(all_ratios)} ratios across 6 categories")
