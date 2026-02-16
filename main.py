# financial_analysis_2year.py
# 2-Year Comparative Financial Ratio Analysis Tool

import streamlit as st

st.set_page_config(page_title="2-Year Financial Analysis Tool", layout="wide")
st.title("📊 2-Year Comparative Financial Ratio Analysis")

def safe_div(numerator, denominator):
    return numerator / denominator if denominator else 0

st.header("Enter Financial Data for Two Years")

col1, col2 = st.columns(2)

# ---------------- YEAR 1 ----------------
with col1:
    st.subheader("Year 1")

    y1_total_assets = st.number_input("Total Assets (Y1)", min_value=0.0)
    y1_current_assets = st.number_input("Current Assets (Y1)", min_value=0.0)
    y1_current_liabilities = st.number_input("Current Liabilities (Y1)", min_value=0.0)
    y1_total_liabilities = st.number_input("Total Liabilities (Y1)", min_value=0.0)
    y1_equity = st.number_input("Equity (Y1)", min_value=0.0)
    y1_revenue = st.number_input("Revenue (Y1)", min_value=0.0)
    y1_cogs = st.number_input("COGS (Y1)", min_value=0.0)
    y1_net_income = st.number_input("Net Income (Y1)", min_value=0.0)
    y1_ebit = st.number_input("EBIT (Y1)", min_value=0.0)
    y1_ebitda = st.number_input("EBITDA (Y1)", min_value=0.0)
    y1_inventory = st.number_input("Inventory (Y1)", min_value=0.0)
    y1_receivables = st.number_input("Accounts Receivable (Y1)", min_value=0.0)
    y1_payables = st.number_input("Accounts Payable (Y1)", min_value=0.0)
    y1_operating_cf = st.number_input("Operating Cash Flow (Y1)", min_value=0.0)
    y1_interest = st.number_input("Interest Expense (Y1)", min_value=0.0)
    y1_tax = st.number_input("Tax Expense (Y1)", min_value=0.0)
    y1_depreciation = st.number_input("Depreciation (Y1)", min_value=0.0)
    y1_fixed_assets = st.number_input("Fixed Assets (Y1)", min_value=0.0)

# ---------------- YEAR 2 ----------------
with col2:
    st.subheader("Year 2")

    y2_total_assets = st.number_input("Total Assets (Y2)", min_value=0.0)
    y2_current_assets = st.number_input("Current Assets (Y2)", min_value=0.0)
    y2_current_liabilities = st.number_input("Current Liabilities (Y2)", min_value=0.0)
    y2_total_liabilities = st.number_input("Total Liabilities (Y2)", min_value=0.0)
    y2_equity = st.number_input("Equity (Y2)", min_value=0.0)
    y2_revenue = st.number_input("Revenue (Y2)", min_value=0.0)
    y2_cogs = st.number_input("COGS (Y2)", min_value=0.0)
    y2_net_income = st.number_input("Net Income (Y2)", min_value=0.0)
    y2_ebit = st.number_input("EBIT (Y2)", min_value=0.0)
    y2_ebitda = st.number_input("EBITDA (Y2)", min_value=0.0)
    y2_inventory = st.number_input("Inventory (Y2)", min_value=0.0)
    y2_receivables = st.number_input("Accounts Receivable (Y2)", min_value=0.0)
    y2_payables = st.number_input("Accounts Payable (Y2)", min_value=0.0)
    y2_operating_cf = st.number_input("Operating Cash Flow (Y2)", min_value=0.0)
    y2_interest = st.number_input("Interest Expense (Y2)", min_value=0.0)
    y2_tax = st.number_input("Tax Expense (Y2)", min_value=0.0)
    y2_depreciation = st.number_input("Depreciation (Y2)", min_value=0.0)
    y2_fixed_assets = st.number_input("Fixed Assets (Y2)", min_value=0.0)

# ---------------- CALCULATION ----------------
if st.button("Calculate Comparative Ratios"):

    def calculate_ratios(total_assets, current_assets, current_liabilities,
                         total_liabilities, equity, revenue, cogs,
                         net_income, ebit, ebitda, inventory,
                         receivables, payables, operating_cf,
                         interest, tax, depreciation, fixed_assets):

        ratios = {}

        # Profitability
        ratios["ROA (%)"] = safe_div(net_income, total_assets) * 100
        ratios["ROE (%)"] = safe_div(net_income, equity) * 100
        ratios["ROCE (%)"] = safe_div(ebit, (total_assets - current_liabilities)) * 100
        ratios["Gross Margin (%)"] = safe_div((revenue - cogs), revenue) * 100
        ratios["Net Margin (%)"] = safe_div(net_income, revenue) * 100
        ratios["EBITDA Margin (%)"] = safe_div(ebitda, revenue) * 100

        # Liquidity
        ratios["Current Ratio"] = safe_div(current_assets, current_liabilities)
        ratios["Quick Ratio"] = safe_div((current_assets - inventory), current_liabilities)
        ratios["Operating CF Ratio"] = safe_div(operating_cf, current_liabilities)

        # Solvency
        ratios["Debt to Equity"] = safe_div(total_liabilities, equity)
        ratios["Interest Coverage"] = safe_div(ebit, interest)
        ratios["CFO to Total Debt (%)"] = safe_div(operating_cf, total_liabilities) * 100

        # Efficiency
        ratios["Inventory Turnover"] = safe_div(cogs, inventory)
        ratios["Receivable Days"] = safe_div(receivables, revenue) * 365
        ratios["Payable Days"] = safe_div(payables, cogs) * 365
        ratios["Asset Turnover"] = safe_div(revenue, total_assets)
        ratios["Fixed Asset Turnover"] = safe_div(revenue, fixed_assets)

        # Tax & Depreciation
        ratios["Effective Tax Rate (%)"] = safe_div(tax, ebit) * 100
        ratios["Depreciation Rate (%)"] = safe_div(depreciation, revenue) * 100

        return ratios

    ratios_y1 = calculate_ratios(
        y1_total_assets, y1_current_assets, y1_current_liabilities,
        y1_total_liabilities, y1_equity, y1_revenue, y1_cogs,
        y1_net_income, y1_ebit, y1_ebitda, y1_inventory,
        y1_receivables, y1_payables, y1_operating_cf,
        y1_interest, y1_tax, y1_depreciation, y1_fixed_assets
    )

    ratios_y2 = calculate_ratios(
        y2_total_assets, y2_current_assets, y2_current_liabilities,
        y2_total_liabilities, y2_equity, y2_revenue, y2_cogs,
        y2_net_income, y2_ebit, y2_ebitda, y2_inventory,
        y2_receivables, y2_payables, y2_operating_cf,
        y2_interest, y2_tax, y2_depreciation, y2_fixed_assets
    )

    st.header("📈 Comparative Analysis")

    for key in ratios_y1:
        change = ratios_y2[key] - ratios_y1[key]
        pct_change = safe_div(change, ratios_y1[key]) * 100

        st.write(f"""
        **{key}**
        - Year 1: {round(ratios_y1[key],2)}
        - Year 2: {round(ratios_y2[key],2)}
        - Change: {round(change,2)}
        - % Change: {round(pct_change,2)}%
        """)
# ---------------- RED FLAG ENGINE ----------------
    st.header("🚨 Automatic Red-Flag Analysis")

    red_flags = []

    # 1. Revenue vs Receivable Growth
    revenue_growth = safe_div((y2_revenue - y1_revenue), y1_revenue) * 100
    receivable_growth = safe_div((y2_receivables - y1_receivables), y1_receivables) * 100

    if receivable_growth > revenue_growth + 15:
        red_flags.append("🔴 Receivables growing significantly faster than revenue → Possible revenue inflation.")

    # 2. CFO vs Net Income Quality
    if y2_net_income != 0:
        cfo_to_ni = y2_operating_cf / y2_net_income
        if cfo_to_ni < 0.8:
            red_flags.append("🔴 Operating Cash Flow is weak compared to Net Income → Poor earnings quality.")

    # 3. Gross Margin Spike
    gross_margin_y1 = safe_div((y1_revenue - y1_cogs), y1_revenue) * 100
    gross_margin_y2 = safe_div((y2_revenue - y2_cogs), y2_revenue) * 100

    if gross_margin_y2 - gross_margin_y1 > 10:
        red_flags.append("🔴 Unusual Gross Margin increase → Possible cost deferral or inventory manipulation.")

    # 4. Debt Stress
    debt_equity_y2 = safe_div(y2_total_liabilities, y2_equity)
    if debt_equity_y2 > 3:
        red_flags.append("🔴 High Debt-to-Equity ratio → Financial distress risk.")

    # 5. Interest Coverage Risk
    interest_coverage_y2 = safe_div(y2_ebit, y2_interest)
    if interest_coverage_y2 < 1.5:
        red_flags.append("🔴 Low Interest Coverage → Default risk warning.")

    # 6. Inventory Build-Up
    inventory_growth = safe_div((y2_inventory - y1_inventory), y1_inventory) * 100
    if inventory_growth > revenue_growth + 15:
        red_flags.append("🔴 Inventory growing faster than sales → Possible overstatement or slow-moving stock.")

    # 7. Effective Tax Rate Drop
    etr_y1 = safe_div(y1_tax, y1_ebit) * 100
    etr_y2 = safe_div(y2_tax, y2_ebit) * 100

    if etr_y1 - etr_y2 > 10:
        red_flags.append("🔴 Sharp drop in Effective Tax Rate → Possible aggressive accounting.")

    # 8. Negative Operating Cash Flow
    if y2_operating_cf < 0:
        red_flags.append("🔴 Negative Operating Cash Flow → Sustainability concern.")

    # 9. Working Capital Deterioration
    wc_y1 = y1_current_assets - y1_current_liabilities
    wc_y2 = y2_current_assets - y2_current_liabilities

    if wc_y2 < wc_y1:
        red_flags.append("🔴 Working Capital deteriorating → Liquidity pressure.")

    # Display Results
    if red_flags:
        for flag in red_flags:
            st.error(flag)
    else:
        st.success("✅ No major red flags detected based on analytical review.")