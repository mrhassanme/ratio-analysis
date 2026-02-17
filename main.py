import streamlit as st
import pandas as pd

st.set_page_config(page_title="Financial Comparative Analysis Tool", layout="wide")

st.title("📊 Financial Comparative Analysis Tool (2-Year Comparison)")

# ----------------------------
# Utility Function
# ----------------------------
def safe_div(n, d):
    return n / d if d != 0 else 0

# ----------------------------
# INPUT SECTION (Excel Style)
# ----------------------------
st.header("📥 Enter Financial Data")

col1, col2, col3 = st.columns([2,1,1])

with col1:
    st.markdown("### Item")

with col2:
    st.markdown("### Year 1")

with col3:
    st.markdown("### Year 2")

def input_row(label):
    c1, c2, c3 = st.columns([2,1,1])
    with c1:
        st.write(label)
    with c2:
        y1 = st.number_input("", key=label+"y1")
    with c3:
        y2 = st.number_input("", key=label+"y2")
    return y1, y2

# Income Statement
y1_revenue, y2_revenue = input_row("Revenue")
y1_cogs, y2_cogs = input_row("Cost of Goods Sold")
y1_net_income, y2_net_income = input_row("Net Income")
y1_ebit, y2_ebit = input_row("EBIT")
y1_interest, y2_interest = input_row("Interest Expense")
y1_tax, y2_tax = input_row("Tax Expense")

# Balance Sheet
y1_current_assets, y2_current_assets = input_row("Current Assets")
y1_current_liabilities, y2_current_liabilities = input_row("Current Liabilities")
y1_inventory, y2_inventory = input_row("Inventory")
y1_receivables, y2_receivables = input_row("Accounts Receivable")
y1_total_assets, y2_total_assets = input_row("Total Assets")
y1_total_liabilities, y2_total_liabilities = input_row("Total Liabilities")
y1_equity, y2_equity = input_row("Equity")

# Cash Flow
y1_operating_cf, y2_operating_cf = input_row("Operating Cash Flow")

# ----------------------------
# CALCULATION SECTION
# ----------------------------
if st.button("Run Full Analysis"):

    st.header("📊 Ratio Analysis")

    ratios = {
        "Current Ratio": (
            safe_div(y1_current_assets, y1_current_liabilities),
            safe_div(y2_current_assets, y2_current_liabilities)
        ),
        "Quick Ratio": (
            safe_div(y1_current_assets - y1_inventory, y1_current_liabilities),
            safe_div(y2_current_assets - y2_inventory, y2_current_liabilities)
        ),
        "Debt to Equity": (
            safe_div(y1_total_liabilities, y1_equity),
            safe_div(y2_total_liabilities, y2_equity)
        ),
        "Gross Margin (%)": (
            safe_div(y1_revenue - y1_cogs, y1_revenue) * 100,
            safe_div(y2_revenue - y2_cogs, y2_revenue) * 100
        ),
        "Net Profit Margin (%)": (
            safe_div(y1_net_income, y1_revenue) * 100,
            safe_div(y2_net_income, y2_revenue) * 100
        ),
        "Return on Assets (%)": (
            safe_div(y1_net_income, y1_total_assets) * 100,
            safe_div(y2_net_income, y2_total_assets) * 100
        ),
        "Return on Equity (%)": (
            safe_div(y1_net_income, y1_equity) * 100,
            safe_div(y2_net_income, y2_equity) * 100
        ),
        "Interest Coverage": (
            safe_div(y1_ebit, y1_interest),
            safe_div(y2_ebit, y2_interest)
        ),
        "CFO to Net Income": (
            safe_div(y1_operating_cf, y1_net_income),
            safe_div(y2_operating_cf, y2_net_income)
        )
    }

    df = pd.DataFrame(ratios, index=["Year 1", "Year 2"]).T
    st.dataframe(df.style.format("{:.2f}"))

    # ----------------------------
    # RED FLAG ENGINE
    # ----------------------------
    st.header("🚨 Automatic Red-Flag Analysis")

    red_flags = []

    revenue_growth = safe_div((y2_revenue - y1_revenue), y1_revenue) * 100
    receivable_growth = safe_div((y2_receivables - y1_receivables), y1_receivables) * 100
    inventory_growth = safe_div((y2_inventory - y1_inventory), y1_inventory) * 100

    if receivable_growth > revenue_growth + 15:
        red_flags.append("Receivables growing faster than revenue → Possible revenue inflation")

    if inventory_growth > revenue_growth + 15:
        red_flags.append("Inventory growth exceeds revenue growth → Possible overstatement")

    if safe_div(y2_operating_cf, y2_net_income) < 0.8:
        red_flags.append("Low Operating Cash Flow relative to Net Income → Poor earnings quality")

    if safe_div(y2_total_liabilities, y2_equity) > 3:
        red_flags.append("High Debt-to-Equity → Financial distress risk")

    if safe_div(y2_ebit, y2_interest) < 1.5:
        red_flags.append("Low Interest Coverage → Default risk")

    if y2_operating_cf < 0:
        red_flags.append("Negative Operating Cash Flow → Sustainability concern")

    if red_flags:
        for flag in red_flags:
            st.error(flag)
    else:
        st.success("✅ No major red flags detected")

    # ----------------------------
    # SUMMARY
    # ----------------------------
    st.header("📌 Growth Summary")

    growth_df = pd.DataFrame({
        "Metric": ["Revenue Growth (%)", "Net Income Growth (%)"],
        "Value": [
            revenue_growth,
            safe_div((y2_net_income - y1_net_income), y1_net_income) * 100
        ]
    })

    st.dataframe(growth_df.style.format({"Value": "{:.2f}"}))
