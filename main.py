import streamlit as st
import pandas as pd
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
    try:
        v = float(val)
        if v > 0:
            return "color: #38a169; font-weight:600"
        elif v < 0:
            return "color: #e53e3e; font-weight:600"
    except Exception:
        pass
    return "color: #718096"


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:
    st.title("⚙️ Settings")
    company_name = st.text_input("Company Name", placeholder="e.g. ABC Corp")
    industry = st.selectbox("Industry", [
        "General", "Manufacturing", "Retail", "Technology",
        "Banking/Finance", "Healthcare", "Real Estate", "Energy"
    ])
    currency = st.selectbox("Currency", [
        "USD ($)", "GBP (£)", "EUR (€)", "MYR (RM)", "INR (₹)", "SGD (S$)"
    ])
    curr_sym = currency.split("(")[1].replace(")", "").strip()

    st.markdown("---")
    st.markdown("**📘 How to use**")
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
st.caption("Ratio analysis · Horizontal & vertical analysis · Red flag detection · Charts · Excel export")
st.markdown("---")


# --------------------------------------------------
# INPUT SECTION
# --------------------------------------------------

st.markdown('<div class="section-header">📥 Enter Financial Data</div>', unsafe_allow_html=True)

tab_is, tab_bs, tab_cf, tab_extra = st.tabs([
    "📋 Income Statement", "🏦 Balance Sheet", "💵 Cash Flow", "➕ Additional"
])

def two_col_input(label, key, help_text=""):
    c1, c2, c3 = st.columns([2.5, 1, 1])
    c1.markdown(f"**{label}**")
    if help_text:
        c1.caption(help_text)
    cy = c2.number_input("CY", value=0.0, step=1.0, format="%.2f",
                         key=f"{key}_cy", label_visibility="collapsed")
    py = c3.number_input("PY", value=0.0, step=1.0, format="%.2f",
                         key=f"{key}_py", label_visibility="collapsed")
    return cy, py

with tab_is:
    hdr1, hdr2, hdr3 = st.columns([2.5, 1, 1])
    hdr1.markdown("**Item**")
    hdr2.markdown("**Current Year**")
    hdr3.markdown("**Previous Year**")
    cy_revenue,      py_revenue      = two_col_input("Revenue / Sales", "revenue")
    cy_cogs,         py_cogs         = two_col_input("Cost of Goods Sold (COGS)", "cogs")
    cy_gross,        py_gross        = two_col_input("Gross Profit", "gross",
                                                      "Leave 0 to auto-calc as Revenue − COGS")
    cy_ebitda,       py_ebitda       = two_col_input("EBITDA", "ebitda")
    cy_ebit,         py_ebit         = two_col_input("EBIT", "ebit")
    cy_interest,     py_interest     = two_col_input("Finance Cost / Interest Expense", "interest")
    cy_tax,          py_tax          = two_col_input("Tax Expense", "tax")
    cy_pbt,          py_pbt          = two_col_input("Profit Before Tax (PBT)", "pbt")
    cy_pat,          py_pat          = two_col_input("Profit After Tax (PAT) / Net Income", "pat")
    cy_sga,          py_sga          = two_col_input("SG&A Expenses", "sga")
    cy_depreciation, py_depreciation = two_col_input("Depreciation Expense", "depreciation")

with tab_bs:
    hdr1, hdr2, hdr3 = st.columns([2.5, 1, 1])
    hdr1.markdown("**Item**")
    hdr2.markdown("**Current Year**")
    hdr3.markdown("**Previous Year**")
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
    hdr1, hdr2, hdr3 = st.columns([2.5, 1, 1])
    hdr1.markdown("**Item**")
    hdr2.markdown("**Current Year**")
    hdr3.markdown("**Previous Year**")
    cy_ocf, py_ocf = two_col_input("Operating Cash Flow (CFO)", "ocf")
    cy_icf, py_icf = two_col_input("Investing Cash Flow", "icf")
    cy_fcf, py_fcf = two_col_input("Financing Cash Flow", "fcf")

with tab_extra:
    hdr1, hdr2, hdr3 = st.columns([2.5, 1, 1])
    hdr1.markdown("**Item**")
    hdr2.markdown("**Current Year**")
    hdr3.markdown("**Previous Year**")
    cy_credit_sales, py_credit_sales = two_col_input(
        "Credit Sales (for Receivable Days)", "credit_sales",
        "Leave 0 to use Total Revenue as proxy"
    )
    st.info("💡 Average figures are auto-calculated as (Current Year + Previous Year) / 2")


# --------------------------------------------------
# RUN ANALYSIS
# --------------------------------------------------

st.markdown("---")
run = st.button("🚀 Run Full Analysis", type="primary", use_container_width=True)

if run:

    # ---------- Derived / averaged values ----------
    cy_gross_profit = cy_gross if cy_gross != 0 else cy_revenue - cy_cogs
    py_gross_profit = py_gross if py_gross != 0 else py_revenue - py_cogs

    credit_cy = cy_credit_sales if cy_credit_sales != 0 else cy_revenue
    credit_py = py_credit_sales if py_credit_sales != 0 else py_revenue

    avg_inventory    = avg(cy_inventory,    py_inventory)
    avg_receivables  = avg(cy_receivables,  py_receivables)
    avg_payables     = avg(cy_payables,     py_payables)
    avg_equity       = avg(cy_equity,       py_equity)
    avg_total_assets = avg(cy_total_assets, py_total_assets)

    working_capital = cy_current_assets - cy_current_liab
    py_wc           = py_current_assets - py_current_liab

    # ======================================================
    # 1️⃣  RATIO ANALYSIS
    # ======================================================

    st.markdown('<div class="section-header">📊 Ratio Analysis</div>', unsafe_allow_html=True)

    # --- Profitability ---
    roce_cy = pct(cy_ebit, cy_total_assets - cy_current_liab)
    roe_cy  = pct(cy_pat, avg_equity)
    roa_cy  = pct(cy_pat, avg_total_assets)
    gpm_cy  = pct(cy_gross_profit, cy_revenue)
    npm_cy  = pct(cy_pat, cy_revenue)
    ebitda_m_cy = pct(cy_ebitda, cy_revenue)

    roce_py = pct(py_ebit, py_total_assets - py_current_liab)
    roe_py  = pct(py_pat, py_equity)
    roa_py  = pct(py_pat, py_total_assets)
    gpm_py  = pct(py_gross_profit, py_revenue)
    npm_py  = pct(py_pat, py_revenue)
    ebitda_m_py = pct(py_ebitda, py_revenue)

    # --- Liquidity ---
    cr_cy     = safe_div(cy_current_assets, cy_current_liab)
    qr_cy     = safe_div(cy_current_assets - cy_inventory, cy_current_liab)
    cash_r_cy = safe_div(cy_cash, cy_current_liab)
    cr_py     = safe_div(py_current_assets, py_current_liab)
    qr_py     = safe_div(py_current_assets - py_inventory, py_current_liab)
    cash_r_py = safe_div(py_cash, py_current_liab)

    # --- Leverage ---
    de_cy   = safe_div(cy_total_debt, cy_equity)
    gear_cy = pct(cy_lt_debt, cy_lt_debt + cy_equity)
    ic_cy   = safe_div(cy_ebit, cy_interest)
    de_py   = safe_div(py_total_debt, py_equity)
    gear_py = pct(py_lt_debt, py_lt_debt + py_equity)
    ic_py   = safe_div(py_ebit, py_interest)

    # --- Efficiency ---
    inv_turn_cy = safe_div(cy_cogs, avg_inventory)
    inv_days_cy = safe_div(avg_inventory, cy_cogs) * 365
    rec_days_cy = safe_div(avg_receivables, credit_cy) * 365
    pay_days_cy = safe_div(avg_payables, cy_cogs) * 365
    wcc_cy      = inv_days_cy + rec_days_cy - pay_days_cy
    at_cy       = safe_div(cy_revenue, cy_total_assets)
    fat_cy      = safe_div(cy_revenue, cy_net_ppe)

    inv_turn_py = safe_div(py_cogs, avg(py_inventory, 0))
    inv_days_py = safe_div(py_inventory, py_cogs) * 365
    rec_days_py = safe_div(py_receivables, credit_py) * 365
    pay_days_py = safe_div(py_payables, py_cogs) * 365
    wcc_py      = inv_days_py + rec_days_py - pay_days_py
    at_py       = safe_div(py_revenue, py_total_assets)
    fat_py      = safe_div(py_revenue, py_net_ppe)

    # --- Cash Flow ---
    ocf_cl_cy   = safe_div(cy_ocf, cy_current_liab)
    ocf_np_cy   = safe_div(cy_ocf, cy_pat)
    ccr_cy      = safe_div(cy_ocf, cy_ebitda)
    cfo_debt_cy = safe_div(cy_ocf, cy_total_debt)
    ocf_cl_py   = safe_div(py_ocf, py_current_liab)
    ocf_np_py   = safe_div(py_ocf, py_pat)
    ccr_py      = safe_div(py_ocf, py_ebitda)
    cfo_debt_py = safe_div(py_ocf, py_total_debt)

    # --- Quality ---
    eff_tax_cy  = pct(cy_tax, cy_pbt)
    sga_s_cy    = pct(cy_sga, cy_revenue)
    dep_rate_cy = pct(cy_depreciation, cy_gross_ppe)
    accruals_cy = pct(cy_pat - cy_ocf, cy_total_assets)
    eff_tax_py  = pct(py_tax, py_pbt)
    sga_s_py    = pct(py_sga, py_revenue)
    dep_rate_py = pct(py_depreciation, py_gross_ppe)
    accruals_py = pct(py_pat - py_ocf, py_total_assets)

    # --- Altman Z-Score ---
    def altman(wc, ta, re, ebit, equity, tl, sales):
        if ta == 0 or tl == 0:
            return 0.0
        return (1.2*(wc/ta) + 1.4*(re/ta) + 3.3*(ebit/ta) +
                0.6*(equity/tl) + 1.0*(sales/ta))

    z_cy = altman(working_capital, cy_total_assets, cy_retained,
                  cy_ebit, cy_equity, cy_total_liab, cy_revenue)
    z_py = altman(py_wc, py_total_assets, py_retained,
                  py_ebit, py_equity, py_total_liab, py_revenue)

    # --- Build ratio groups ---
    ratio_groups = {
        "📈 Profitability": {
            "ROCE (%)":               (roce_cy,      roce_py),
            "ROE (%)":                (roe_cy,       roe_py),
            "ROA (%)":                (roa_cy,       roa_py),
            "Gross Profit Margin (%)": (gpm_cy,      gpm_py),
            "Net Profit Margin (%)":   (npm_cy,      npm_py),
            "EBITDA Margin (%)":       (ebitda_m_cy, ebitda_m_py),
        },
        "💧 Liquidity": {
            "Current Ratio":          (cr_cy,        cr_py),
            "Quick Ratio":            (qr_cy,        qr_py),
            "Cash Ratio":             (cash_r_cy,    cash_r_py),
            "Working Capital (abs)":  (working_capital, py_wc),
        },
        "⚖️ Leverage": {
            "Debt to Equity":         (de_cy,        de_py),
            "Gearing Ratio (%)":      (gear_cy,      gear_py),
            "Interest Coverage (x)":  (ic_cy,        ic_py),
        },
        "⚙️ Efficiency": {
            "Inventory Turnover (x)":  (inv_turn_cy, inv_turn_py),
            "Inventory Days":          (inv_days_cy, inv_days_py),
            "Receivable Days":         (rec_days_cy, rec_days_py),
            "Payable Days":            (pay_days_cy, pay_days_py),
            "Working Capital Cycle":   (wcc_cy,      wcc_py),
            "Asset Turnover (x)":      (at_cy,       at_py),
            "Fixed Asset Turnover (x)":(fat_cy,      fat_py),
        },
        "💵 Cash Flow": {
            "OCF Ratio":               (ocf_cl_cy,   ocf_cl_py),
            "OCF to Net Profit":       (ocf_np_cy,   ocf_np_py),
            "Cash Conversion Ratio":   (ccr_cy,      ccr_py),
            "CFO to Total Debt":       (cfo_debt_cy, cfo_debt_py),
        },
        "🔬 Quality & Other": {
            "Effective Tax Rate (%)":  (eff_tax_cy,  eff_tax_py),
            "SG&A to Sales (%)":       (sga_s_cy,    sga_s_py),
            "Depreciation Rate (%)":   (dep_rate_cy, dep_rate_py),
            "Accruals to Assets (%)":  (accruals_cy, accruals_py),
            "Altman Z-Score":          (z_cy,        z_py),
        },
    }

    all_ratio_data = {}
    for group_name, ratios in ratio_groups.items():
        with st.expander(group_name, expanded=True):
            df = pd.DataFrame(ratios, index=["Current Year", "Previous Year"]).T
            df["Change"] = df["Current Year"] - df["Previous Year"]
            df["Change %"] = df.apply(
                lambda row: growth(row["Current Year"], row["Previous Year"]), axis=1
            )
            st.dataframe(
                df.style
                  .format("{:.2f}")
                  .applymap(color_change, subset=["Change", "Change %"]),
                use_container_width=True
            )
        all_ratio_data.update(ratios)


    # ======================================================
    # 2️⃣  HORIZONTAL ANALYSIS
    # ======================================================

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

    horiz_rows = []
    for item, (cy, py) in horiz_items.items():
        g = growth(cy, py)
        horiz_rows.append({
            "Item": item,
            f"Previous Year ({curr_sym})": py,
            f"Current Year ({curr_sym})":  cy,
            "Change (%)": round(g, 2),
            "Trend": "▲" if g > 0 else ("▼" if g < 0 else "—"),
        })

    df_horiz = pd.DataFrame(horiz_rows)
    st.dataframe(
        df_horiz.style
          .format({
              f"Previous Year ({curr_sym})": "{:,.2f}",
              f"Current Year ({curr_sym})":  "{:,.2f}",
              "Change (%)": "{:.2f}",
          })
          .applymap(color_change, subset=["Change (%)"]),
        use_container_width=True,
        hide_index=True,
    )

    # Native bar chart for YoY growth
    st.caption("📊 Year-on-Year Growth (%)")
    chart_horiz = df_horiz.set_index("Item")[["Change (%)"]]
    st.bar_chart(chart_horiz)


    # ======================================================
    # 3️⃣  VERTICAL ANALYSIS
    # ======================================================

    st.markdown('<div class="section-header">📊 Vertical Analysis (Common Size)</div>',
                unsafe_allow_html=True)

    v_col1, v_col2 = st.columns(2)

    with v_col1:
        st.subheader("Income Statement (% of Revenue)")
        inc_vert = {
            "Revenue":      (100.0,                            100.0),
            "COGS":         (pct(cy_cogs,         cy_revenue), pct(py_cogs,         py_revenue)),
            "Gross Profit": (pct(cy_gross_profit, cy_revenue), pct(py_gross_profit, py_revenue)),
            "SG&A":         (pct(cy_sga,          cy_revenue), pct(py_sga,          py_revenue)),
            "EBIT":         (pct(cy_ebit,         cy_revenue), pct(py_ebit,         py_revenue)),
            "Interest":     (pct(cy_interest,     cy_revenue), pct(py_interest,     py_revenue)),
            "Tax":          (pct(cy_tax,          cy_revenue), pct(py_tax,          py_revenue)),
            "Net Income":   (pct(cy_pat,          cy_revenue), pct(py_pat,          py_revenue)),
        }
        df_inc_vert = pd.DataFrame(inc_vert, index=["CY %", "PY %"]).T
        st.dataframe(df_inc_vert.style.format("{:.2f}"), use_container_width=True)

        st.caption("📊 Income Statement — Current Year %")
        st.bar_chart(df_inc_vert[["CY %"]])

    with v_col2:
        st.subheader("Balance Sheet (% of Total Assets)")
        bs_vert = {
            "Cash":              (pct(cy_cash,           cy_total_assets), pct(py_cash,           py_total_assets)),
            "Receivables":       (pct(cy_receivables,    cy_total_assets), pct(py_receivables,    py_total_assets)),
            "Inventory":         (pct(cy_inventory,      cy_total_assets), pct(py_inventory,      py_total_assets)),
            "Current Assets":    (pct(cy_current_assets, cy_total_assets), pct(py_current_assets, py_total_assets)),
            "Net Fixed Assets":  (pct(cy_net_ppe,        cy_total_assets), pct(py_net_ppe,        py_total_assets)),
            "Current Liab.":     (pct(cy_current_liab,   cy_total_assets), pct(py_current_liab,   py_total_assets)),
            "Total Liabilities": (pct(cy_total_liab,     cy_total_assets), pct(py_total_liab,     py_total_assets)),
            "Equity":            (pct(cy_equity,         cy_total_assets), pct(py_equity,         py_total_assets)),
        }
        df_bs_vert = pd.DataFrame(bs_vert, index=["CY %", "PY %"]).T
        st.dataframe(df_bs_vert.style.format("{:.2f}"), use_container_width=True)

        st.caption("📊 Balance Sheet — CY vs PY (%)")
        st.bar_chart(df_bs_vert)


    # ======================================================
    # 4️⃣  TREND CHARTS
    # ======================================================

    st.markdown('<div class="section-header">📉 Key Ratio Trends (CY vs PY)</div>',
                unsafe_allow_html=True)

    ch1, ch2 = st.columns(2)

    with ch1:
        st.caption("📊 Profitability Margins (%)")
        df_prof = pd.DataFrame({
            "Gross Margin %":   [gpm_py,      gpm_cy],
            "Net Margin %":     [npm_py,      npm_cy],
            "EBITDA Margin %":  [ebitda_m_py, ebitda_m_cy],
            "ROE %":            [roe_py,      roe_cy],
            "ROA %":            [roa_py,      roa_cy],
        }, index=["Previous Year", "Current Year"])
        st.bar_chart(df_prof)

    with ch2:
        st.caption("📊 Liquidity & Leverage Ratios")
        df_lev = pd.DataFrame({
            "Current Ratio": [cr_py,  cr_cy],
            "Quick Ratio":   [qr_py,  qr_cy],
            "Debt/Equity":   [de_py,  de_cy],
            "Int. Coverage": [ic_py,  ic_cy],
        }, index=["Previous Year", "Current Year"])
        st.bar_chart(df_lev)

    st.caption("📊 Working Capital Cycle — Days (CY vs PY)")
    df_wcc = pd.DataFrame({
        "Inventory Days":  [inv_days_py, inv_days_cy],
        "Receivable Days": [rec_days_py, rec_days_cy],
        "Payable Days":    [pay_days_py, pay_days_cy],
    }, index=["Previous Year", "Current Year"])
    st.bar_chart(df_wcc)


    # ======================================================
    # 5️⃣  ALTMAN Z-SCORE
    # ======================================================

    st.markdown('<div class="section-header">🧮 Altman Z-Score</div>', unsafe_allow_html=True)

    def z_label(z):
        if z > 3.0:   return "✅ Safe Zone (> 3.0)",        "#38a169"
        elif z > 2.7: return "🟡 Caution Zone (2.7–3.0)",  "#d69e2e"
        elif z > 1.8: return "🟠 Distress Zone (1.8–2.7)", "#dd6b20"
        else:         return "🔴 Danger Zone (< 1.8)",      "#e53e3e"

    lbl_cy, col_cy = z_label(z_cy)
    lbl_py, col_py = z_label(z_py)

    z1, z2, z3 = st.columns(3)
    z1.metric("Current Year Z-Score",  f"{z_cy:.2f}", delta=f"{z_cy - z_py:.2f} vs PY")
    z2.metric("Previous Year Z-Score", f"{z_py:.2f}")
    z3.markdown(f"**Interpretation:**")
    z3.markdown(f"<span style='color:{col_cy};font-size:1.05rem;font-weight:700'>{lbl_cy}</span>",
                unsafe_allow_html=True)

    st.caption("Zones: < 1.8 Danger | 1.8–2.7 Distress | 2.7–3.0 Caution | > 3.0 Safe")
    df_z = pd.DataFrame({
        "Z-Score": [z_py, z_cy],
        "Safe Threshold (3.0)": [3.0, 3.0],
        "Danger Threshold (1.8)": [1.8, 1.8],
    }, index=["Previous Year", "Current Year"])
    st.line_chart(df_z)


    # ======================================================
    # 6️⃣  RED FLAG ENGINE
    # ======================================================

    st.markdown('<div class="section-header">🚨 Red Flag & Health Check</div>',
                unsafe_allow_html=True)

    flags     = []
    positives = []

    rev_growth    = growth(cy_revenue,    py_revenue)
    rec_growth    = growth(cy_receivables, py_receivables)
    profit_growth = growth(cy_pat,        py_pat)
    debt_growth   = growth(cy_total_debt, py_total_debt)

    # Liquidity
    if cr_cy < 1.0:
        flags.append(("🔴 Critical", "Current Ratio below 1.0 — Cannot cover short-term obligations"))
    elif cr_cy < 1.5:
        flags.append(("🟡 Warning",  f"Current Ratio is low at {cr_cy:.2f} (target ≥ 1.5)"))
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
        flags.append(("🟡 Warning", "Operating CF significantly below Net Profit — Weak cash conversion or aggressive accounting"))

    # Leverage
    if de_cy > 3.0:
        flags.append(("🔴 Critical", f"Debt-to-Equity at {de_cy:.2f} — Dangerously high leverage"))
    elif de_cy > 2.0:
        flags.append(("🟡 Warning",  f"Debt-to-Equity at {de_cy:.2f} — High leverage (target < 2.0)"))
    else:
        positives.append(f"Debt-to-Equity is manageable at {de_cy:.2f}")

    if ic_cy < 1.5 and cy_interest > 0:
        flags.append(("🔴 Critical", f"Interest Coverage of {ic_cy:.2f}x — At risk of defaulting on interest"))
    elif ic_cy < 3.0 and cy_interest > 0:
        flags.append(("🟡 Warning",  f"Interest Coverage of {ic_cy:.2f}x — Should be above 3.0x"))

    # Revenue & receivables
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
        flags.append(("🟡 Warning",  f"Net Profit Margin very thin at {npm_cy:.1f}%"))

    # Accruals
    if abs(accruals_cy) > 5:
        flags.append(("🟡 Warning", f"High Accruals-to-Assets ({accruals_cy:.1f}%) — Earnings quality concern"))

    # Altman
    if z_cy < 1.8:
        flags.append(("🔴 Critical", f"Altman Z-Score {z_cy:.2f} — High bankruptcy risk"))
    elif z_cy < 2.7:
        flags.append(("🟡 Warning",  f"Altman Z-Score {z_cy:.2f} — In financial distress zone"))
    elif z_cy > 3.0:
        positives.append(f"Altman Z-Score {z_cy:.2f} — Company is in the safe zone")

    if npm_cy > npm_py and rev_growth > 0:
        positives.append("Profit margin improving alongside revenue growth — Quality performance")

    crit_flags = [f for f in flags if "Critical" in f[0]]
    warn_flags = [f for f in flags if "Warning"  in f[0]]

    fc1, fc2, fc3 = st.columns(3)
    fc1.metric("🔴 Critical Issues", len(crit_flags))
    fc2.metric("🟡 Warnings",        len(warn_flags))
    fc3.metric("✅ Positives",       len(positives))

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


    # ======================================================
    # 7️⃣  EXPORT TO EXCEL
    # ======================================================

    st.markdown('<div class="section-header">📤 Export Report</div>', unsafe_allow_html=True)

    output = BytesIO()

    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        wb = writer.book

        hdr_fmt = wb.add_format({
            'bold': True, 'bg_color': '#4C72B0',
            'font_color': 'white', 'border': 1, 'align': 'center'
        })

        # Summary sheet
        summary_data = {
            "Company":                [company_name or "N/A"],
            "Industry":               [industry],
            "Currency":               [curr_sym],
            "Current Year Revenue":   [cy_revenue],
            "Current Year Net Income":[cy_pat],
            "Gross Margin %":         [round(gpm_cy,  2)],
            "Net Margin %":           [round(npm_cy,  2)],
            "Current Ratio":          [round(cr_cy,   2)],
            "Debt to Equity":         [round(de_cy,   2)],
            "Altman Z-Score":         [round(z_cy,    2)],
            "Critical Flags":         [len(crit_flags)],
            "Warnings":               [len(warn_flags)],
        }
        pd.DataFrame(summary_data).T.to_excel(writer, sheet_name="Summary", header=False)

        # All ratios
        df_all = pd.DataFrame(all_ratio_data, index=["Current Year", "Previous Year"]).T
        df_all["Change"] = df_all["Current Year"] - df_all["Previous Year"]
        df_all.to_excel(writer, sheet_name="All Ratios")

        # Horizontal
        df_horiz.to_excel(writer, sheet_name="Horizontal Analysis", index=False)

        # Vertical – Income
        df_inc_vert.to_excel(writer, sheet_name="Vertical - Income")

        # Vertical – Balance Sheet
        df_bs_vert.to_excel(writer, sheet_name="Vertical - Balance Sheet")

        # Red Flags
        flags_export = [(s, m) for s, m in flags] + [("✅ Positive", p) for p in positives]
        pd.DataFrame(flags_export, columns=["Type", "Description"]).to_excel(
            writer, sheet_name="Red Flags", index=False
        )

    e1, e2 = st.columns([2, 1])
    e1.download_button(
        label="📥 Download Excel Report",
        data=output.getvalue(),
        file_name=f"Financial_Analysis_{company_name or 'Report'}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True,
    )
    e2.info(f"Report includes {len(all_ratio_data)} ratios across 6 categories")
