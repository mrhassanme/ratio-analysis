import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="Advanced Financial Analysis Tool", layout="wide")

st.title("📊 Advanced Financial Analysis Tool")

# --------------------------------------------------
# Utility Functions
# --------------------------------------------------

def safe_div(n, d):
    return n / d if d != 0 else 0

def growth(current, previous):
    if previous == 0:
        return 0
    return ((current - previous) / abs(previous)) * 100


# --------------------------------------------------
# INPUT SECTION
# --------------------------------------------------

st.header("📥 Enter Financial Data")

col1, col2, col3 = st.columns([2,1,1])
col1.markdown("### Item")
col2.markdown("### Current Year")
col3.markdown("### Previous Year")

def input_row(label):
    c1, c2, c3 = st.columns([2,1,1])
    c1.write(label)
    current = c2.number_input("", value=0.0, step=1.0, format="%.2f", key=label+"_current")
    previous = c3.number_input("", value=0.0, step=1.0, format="%.2f", key=label+"_previous")
    return current, previous


# Income Statement
cy_revenue, py_revenue = input_row("Revenue")
cy_cogs, py_cogs = input_row("Cost of Goods Sold")
cy_net_income, py_net_income = input_row("Net Income")
cy_ebit, py_ebit = input_row("EBIT")
cy_interest, py_interest = input_row("Interest Expense")
cy_tax, py_tax = input_row("Tax Expense")

# Balance Sheet
cy_current_assets, py_current_assets = input_row("Current Assets")
cy_current_liabilities, py_current_liabilities = input_row("Current Liabilities")
cy_inventory, py_inventory = input_row("Inventory")
cy_receivables, py_receivables = input_row("Accounts Receivable")
cy_total_assets, py_total_assets = input_row("Total Assets")
cy_total_liabilities, py_total_liabilities = input_row("Total Liabilities")
cy_equity, py_equity = input_row("Equity")

# Cash Flow
cy_operating_cf, py_operating_cf = input_row("Operating Cash Flow")


# --------------------------------------------------
# ANALYSIS
# --------------------------------------------------

if st.button("Run Full Analysis"):

    # =========================
    # 1️⃣ RATIO ANALYSIS
    # =========================
    st.header("📊 Ratio Analysis")

    ratios = {
        "Current Ratio": (safe_div(cy_current_assets, cy_current_liabilities),
                          safe_div(py_current_assets, py_current_liabilities)),

        "Debt to Equity": (safe_div(cy_total_liabilities, cy_equity),
                           safe_div(py_total_liabilities, py_equity)),

        "Gross Margin (%)": (safe_div(cy_revenue - cy_cogs, cy_revenue) * 100,
                             safe_div(py_revenue - py_cogs, py_revenue) * 100),

        "Net Profit Margin (%)": (safe_div(cy_net_income, cy_revenue) * 100,
                                  safe_div(py_net_income, py_revenue) * 100),

        "ROA (%)": (safe_div(cy_net_income, cy_total_assets) * 100,
                    safe_div(py_net_income, py_total_assets) * 100),

        "ROE (%)": (safe_div(cy_net_income, cy_equity) * 100,
                    safe_div(py_net_income, py_equity) * 100)
    }

    df_ratios = pd.DataFrame(ratios, index=["Current Year", "Previous Year"]).T
    st.dataframe(df_ratios.style.format("{:.2f}"), use_container_width=True)


    # =========================
    # 2️⃣ HORIZONTAL ANALYSIS
    # =========================
    st.header("📈 Horizontal Analysis (YoY Change %)")

    horizontal_data = {
        "Revenue": growth(cy_revenue, py_revenue),
        "Net Income": growth(cy_net_income, py_net_income),
        "Total Assets": growth(cy_total_assets, py_total_assets),
        "Total Liabilities": growth(cy_total_liabilities, py_total_liabilities),
        "Operating Cash Flow": growth(cy_operating_cf, py_operating_cf)
    }

    df_horizontal = pd.DataFrame(horizontal_data.items(), columns=["Item", "Growth %"])
    st.dataframe(df_horizontal.style.format({"Growth %": "{:.2f}"}), use_container_width=True)


    # =========================
    # 3️⃣ VERTICAL ANALYSIS
    # =========================
    st.header("📊 Vertical Analysis (Common Size %)")

    # Income Statement Vertical
    income_vertical = pd.DataFrame({
        "Item": ["Revenue", "COGS", "Net Income"],
        "Current Year %": [
            100,
            safe_div(cy_cogs, cy_revenue) * 100,
            safe_div(cy_net_income, cy_revenue) * 100
        ],
        "Previous Year %": [
            100,
            safe_div(py_cogs, py_revenue) * 100,
            safe_div(py_net_income, py_revenue) * 100
        ]
    })

    st.subheader("Income Statement (as % of Revenue)")
    st.dataframe(income_vertical.style.format("{:.2f}"), use_container_width=True)

    # Balance Sheet Vertical
    balance_vertical = pd.DataFrame({
        "Item": ["Current Assets", "Total Liabilities", "Equity"],
        "Current Year %": [
            safe_div(cy_current_assets, cy_total_assets) * 100,
            safe_div(cy_total_liabilities, cy_total_assets) * 100,
            safe_div(cy_equity, cy_total_assets) * 100
        ],
        "Previous Year %": [
            safe_div(py_current_assets, py_total_assets) * 100,
            safe_div(py_total_liabilities, py_total_assets) * 100,
            safe_div(py_equity, py_total_assets) * 100
        ]
    })

    st.subheader("Balance Sheet (as % of Total Assets)")
    st.dataframe(balance_vertical.style.format("{:.2f}"), use_container_width=True)


    # =========================
    # 4️⃣ RED FLAG ENGINE
    # =========================
    st.header("🚨 Red Flag Indicators")

    red_flags = []

    if growth(cy_receivables, py_receivables) > growth(cy_revenue, py_revenue) + 15:
        red_flags.append("Receivables growing faster than revenue")

    if cy_operating_cf < 0:
        red_flags.append("Negative Operating Cash Flow")

    if safe_div(cy_total_liabilities, cy_equity) > 3:
        red_flags.append("High Debt-to-Equity ratio")

    if red_flags:
        for flag in red_flags:
            st.error(flag)
    else:
        st.success("No major red flags detected")


    # =========================
    # 5️⃣ EXPORT TO EXCEL
    # =========================
    st.header("📤 Export Report")

    output = BytesIO()

    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df_ratios.to_excel(writer, sheet_name='Ratios')
        df_horizontal.to_excel(writer, sheet_name='Horizontal Analysis', index=False)
        income_vertical.to_excel(writer, sheet_name='Vertical Income', index=False)
        balance_vertical.to_excel(writer, sheet_name='Vertical Balance', index=False)

    st.download_button(
        label="Download Excel Report",
        data=output.getvalue(),
        file_name="Financial_Analysis_Report.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
