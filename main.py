# financial_analysis_full.py
# Streamlit Financial Analysis Tool with full ratio list

import streamlit as st

st.set_page_config(page_title="Comprehensive Financial Analysis Tool", layout="centered")
st.title("📊 Comprehensive Financial Ratio Analysis Tool")

# --- Input Section ---
st.header("Enter Financial Statement Data")

# Balance Sheet Inputs
total_assets = st.number_input("Total Assets", min_value=0.0)
current_assets = st.number_input("Current Assets", min_value=0.0)
current_liabilities = st.number_input("Current Liabilities", min_value=0.0)
total_liabilities = st.number_input("Total Liabilities", min_value=0.0)
equity = st.number_input("Shareholder's Equity", min_value=0.0)
short_term_debt = st.number_input("Short Term Debt", min_value=0.0)
fixed_assets = st.number_input("Fixed Assets", min_value=0.0)
working_capital = st.number_input("Working Capital", min_value=0.0)

# Income Statement Inputs
revenue = st.number_input("Revenue / Sales", min_value=0.0)
cogs = st.number_input("Cost of Goods Sold (COGS)", min_value=0.0)
operating_expenses = st.number_input("Operating Expenses (SG&A)", min_value=0.0)
net_income = st.number_input("Net Income", min_value=0.0)
ebit = st.number_input("EBIT", min_value=0.0)
ebitda = st.number_input("EBITDA", min_value=0.0)
tax_expense = st.number_input("Tax Expense", min_value=0.0)
depreciation = st.number_input("Depreciation", min_value=0.0)
interest_expense = st.number_input("Interest Expense", min_value=0.0)

# Cash Flow Inputs
operating_cf = st.number_input("Operating Cash Flow (CFO)", min_value=0.0)
cfo_to_net_income = net_income  # placeholder if needed

# Operational Inputs
inventory = st.number_input("Inventory", min_value=0.0)
accounts_receivable = st.number_input("Accounts Receivable", min_value=0.0)
accounts_payable = st.number_input("Accounts Payable", min_value=0.0)

# Growth Metrics Inputs
prev_revenue = st.number_input("Previous Period Revenue", min_value=0.0)
prev_receivables = st.number_input("Previous Period Receivables", min_value=0.0)

# --- Calculate Ratios ---
if st.button("Calculate Ratios"):

    ratios = {}

    # --- Profitability ---
    ratios["ROCE (%)"] = (ebit / (total_assets - current_liabilities)) * 100 if total_assets - current_liabilities else 0
    ratios["ROE (%)"] = (net_income / equity) * 100 if equity else 0
    ratios["ROA (%)"] = (net_income / total_assets) * 100 if total_assets else 0
    ratios["Gross Profit Margin (%)"] = ((revenue - cogs)/ revenue *100) if revenue else 0
    ratios["Net Profit Margin (%)"] = (net_income / revenue * 100) if revenue else 0
    ratios["EBITDA Margin (%)"] = (ebitda / revenue *100) if revenue else 0
    ratios["Operating CF to Net Profit (%)"] = (operating_cf / net_income *100) if net_income else 0
    ratios["Depreciation Rate (%)"] = (depreciation / revenue *100) if revenue else 0

    # --- Liquidity ---
    ratios["Current Ratio"] = current_assets / current_liabilities if current_liabilities else 0
    ratios["Quick Ratio"] = (current_assets - inventory) / current_liabilities if current_liabilities else 0
    ratios["Cash Ratio"] = operating_cf / current_liabilities if current_liabilities else 0
    ratios["Working Capital"] = current_assets - current_liabilities
    ratios["Working Capital Cycle"] = inventory / cogs * 365 if cogs else 0  # simplified

    # --- Solvency ---
    ratios["Debt to Equity"] = total_liabilities / equity if equity else 0
    ratios["Gearing Ratio (%)"] = (total_liabilities / total_assets *100) if total_assets else 0
    ratios["Interest Coverage"] = ebit / interest_expense if interest_expense else 0
    ratios["CFO to Total Debt (%)"] = operating_cf / total_liabilities *100 if total_liabilities else 0
    ratios["Short Term Debt to Total Debt"] = short_term_debt / total_liabilities if total_liabilities else 0

    # --- Efficiency ---
    ratios["Inventory Turnover"] = cogs / inventory if inventory else 0
    ratios["Inventory Days"] = 365 / (cogs / inventory) if inventory else 0
    ratios["Receivable Days"] = 365 / (revenue / accounts_receivable) if accounts_receivable else 0
    ratios["Payable Days"] = 365 / (cogs / accounts_payable) if accounts_payable else 0
    ratios["Asset Turnover"] = revenue / total_assets if total_assets else 0
    ratios["Fixed Asset Turnover"] = revenue / fixed_assets if fixed_assets else 0
    ratios["Cash Conversion Ratio"] = (operating_cf / (net_income + depreciation)) if (net_income + depreciation) else 0
    ratios["SG&A to Sales (%)"] = operating_expenses / revenue *100 if revenue else 0

    # --- Growth ---
    ratios["Revenue Growth Rate (%)"] = (revenue - prev_revenue) / prev_revenue *100 if prev_revenue else 0
    ratios["Receivable Growth Rate (%)"] = (accounts_receivable - prev_receivables)/ prev_receivables *100 if prev_receivables else 0
    ratios["Receivable Growth vs Revenue Growth"] = ratios["Receivable Growth Rate (%)"] - ratios["Revenue Growth Rate (%)"]

    # --- Tax ---
    ratios["Effective Tax Rate (%)"] = tax_expense / ebit *100 if ebit else 0

    # --- Altman Z-Score Placeholder ---
    ratios["Altman Z-Score"] = 1.2*(working_capital/total_assets) + 1.4*(ebit/total_assets) + 3.3*(revenue/total_assets) + 0.6*(equity/total_liabilities) + (1.0) # simplified

    # --- Display Results ---
    st.header("📈 Financial Ratios Results")
    for name, value in ratios.items():
        st.write(f"**{name}:** {round(value, 2)}")
