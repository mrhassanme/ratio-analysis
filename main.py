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
