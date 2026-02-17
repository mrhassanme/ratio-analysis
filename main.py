import streamlit as st
import pandas as pd

st.set_page_config(page_title="2-Year Financial Analysis Tool", layout="wide")
st.title("📊 2-Year Comparative Financial Analysis Tool")

# ---------------- SAFE DIVISION FUNCTION ----------------
def safe_div(numerator, denominator):
    return numerator / denominator if denominator else 0


# ---------------- INPUT SECTION ----------------
st.header("Enter Financial Data (Year 1 vs Year 2)")

def input_row(label):
    col1, col2 = st.columns(2)
    with col1:
        y1 = st.number_input(f"{label} (Year 1)", min_value=0.0, key=f"{label}_y1")
    with col2:
        y2 = st.number_input(f"{label} (Year 2)", min_value=0.0, key=f"{label}_y2")
    return y1, y2


# -------- BALANCE SHEET --------
st.subheader("Balance Sheet")

y1_total_assets, y2_total_assets = input_row("Total Assets")
y1_current_assets, y2_current_assets = input_row("Current Assets")
y1_current_liabilities, y2_current_liabilities = input_row("Current Liabilities")
y1_total_liabilities, y2_total_liabilities = input_row("Total Liabilities")
y1_equity, y2_equity = input_row("Equity")
y1_inventory, y2_inventory = input_row("Inventory")
y1_receivables, y2_receivables = input_row("Accounts Receivable")
y1_payables, y2_payables = input_row("Accounts Payable")
y1_fixed_assets, y2_fixed_assets = input_row("Fixed Assets")

# -------- INCOME STATEMENT --------
st.subheader("Income Statement")

y1_revenue, y2_revenue = input_row("Revenue")
y1_cogs, y2_cogs = input_row("COGS")
y1_net_income, y2_net_income = input_row("Net Income")
y1_ebit, y2_ebit = input_row("EBIT")
y1_ebitda, y2_ebitda = input_row("EBITDA")
y1_interest, y2_interest = input_row("Interest Expense")
y1_tax, y2_tax = input_row("Tax Expense")
y1_depreciation, y2_depreciation = input_row("Depreciation")

# -------- CASH FLOW --------
st.subheader("Cash Flow")

y1_operating_cf, y2_operating_cf = input_row("Operating Cash Flow")


# ---------------- RUN FULL ANALYSIS ----------------
if st.button("Run Full Analysis"):

    # ---------------- RATIO CALCULATION FUNCTION ----------------
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

        # Solvency
        ratios["Debt to Equity"] = safe_div(total_liabilities, equity)
        ratios["Interest Coverage"] = safe_div(ebit, interest)

        # Efficiency
        ratios["Inventory Turnover"] = safe_div(cogs, inventory)
        ratios["Receivable Days"] = safe_div(receivables, revenue) * 365
        ratios["Payable Days"] = safe_div(payables, cogs) * 365
        ratios["Asset Turnover"] = safe_div(revenue, total_assets)
        ratios["Fixed Asset Turnover"] = safe_div(revenue, fixed_assets)

        # Cash Quality
        ratios["CFO to Net Income"] = safe_div(operating_cf, net_income)

        # Tax
        ratios["Effective Tax Rate (%)"] = safe_div(tax, ebit) * 100

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

    # ---------------- COMPARATIVE TABLE ----------------
    st.header("📊 Comparative Ratio Table")

    comparison_data = []

    for key in ratios_y1:
        y1_val = ratios_y1[key]
        y2_val = ratios_y2[key]
        change = y2_val - y1_val
        pct_change = safe_div(change, y1_val) * 100

        comparison_data.append({
            "Ratio": key,
            "Year 1": round(y1_val, 2),
            "Year 2": round(y2_val, 2),
            "Change": round(change, 2),
            "% Change": round(pct_change, 2)
        })

    df = pd.DataFrame(comparison_data)
    st.dataframe(df, use_container_width=True)

    # ---------------- RED FLAG ENGINE ----------------
    st.header("🚨 Automatic Red-Flag Analysis")

    red_flags = []

    revenue_growth = safe_div((y2_revenue - y1_revenue), y1_revenue) * 100
    receivable_growth = safe_div((y2_receivables - y1_receivables), y1_receivables) * 100

    if receivable_growth > revenue_growth + 15:
        red_flags.append("Receivables growing faster than revenue → Possible revenue inflation.")

    if safe_div(y2_operating_cf, y2_net_income) < 0.8 and y2_net_income != 0:
        red_flags.append("Weak Operating Cash Flow vs Net Income → Earnings quality concern.")

    gross_margin_y1 = safe_div((y1_revenue - y1_cogs), y1_revenue) * 100
    gross_margin_y2 = safe_div((y2_revenue - y2_cogs), y2_revenue) * 100

    if gross_margin_y2 - gross_margin_y1 > 10:
        red_flags.append("Unusual Gross Margin increase → Possible manipulation.")

    if safe_div(y2_total_liabilities, y2_equity) > 3:
        red_flags.append("High Debt-to-Equity ratio → Financial distress risk.")

    if safe_div(y2_ebit, y2_interest) < 1.5:
        red_flags.append("Low Interest Coverage → Default risk.")

    inventory_growth = safe_div((y2_inventory - y1_inventory), y1_inventory) * 100
    if inventory_growth > revenue_growth + 15:
        red_flags.append("Inventory growing faster than sales → Possible overstatement.")

    if y2_operating_cf < 0:
        red_flags.append("Negative Operating Cash Flow → Sustainability concern.")

    wc_y1 = y1_current_assets - y1_current_liabilities
    wc_y2 = y2_current_assets - y2_current_liabilities
    if wc_y2 < wc_y1:
        red_flags.append("Working Capital deterioration → Liquidity pressure.")

    if red_flags:
        for flag in red_flags:
            st.error("🔴 " + flag)
    else:
        st.success("✅ No major red flags detected.")
