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