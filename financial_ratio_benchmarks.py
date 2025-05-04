import pandas as pd

def get_ratio_benchmarks(): # this is used for creating and returning a dataframe with the FR benchmarks
    benchmarks = [
        ("Current Ratio", 1, "Conservative", "Aggressive"),
        ("Quick Ratio", 1, "Financially Sound", "Liquidity Risk"),
        ("Debt-to-Equity Ratio", 1, "Balanced", "Highly Leveraged"),
        ("Interest Coverage Ratio", 2, "Safe", "Risky"),
        ("Net Profit Margin (%)", 10, "Healthy", "Low Profitability"),
        ("Return on Assets (ROA) (%)", 5, "Efficient", "Inefficient"),
        ("Return on Equity (ROE) (%)", 15, "Good Return", "Weak Performance"),
        ("Gross Profit Margin (%)", 40, "Strong", "Weak"),
        ("Asset Turnover Ratio", 1, "Efficient Utilization", "Underutilization"),
        ("Inventory Turnover Ratio", 5, "Optimized", "Slow Moving Inventory"),
        ("Days Inventory on Hand", 100, "Efficient Management", "Excess Stock"),
        ("Earnings Per Share (EPS)", 10, "Strong Earnings", "Weak Earnings"),
        ("Dividend Payout Ratio", 50, "Sustainable", "Over-distribution"),
        ("Dividend Yield (%)", 4, "Attractive", "Low Yield"),
        ("Price-to-Earnings (P/E) Ratio", 15, "Undervalued", "Overvalued")
    ] # this represents a list of tuples where each tuple contains ratio name,threshold and respective interpretation for higher or lower
    
    df = pd.DataFrame(benchmarks, columns=["Ratio", "Threshold", "Interpretation (Higher)", "Interpretation (Lower)"]) # it creates a pd Dataframe from the bechmanrks list
    
    return df
df = get_ratio_benchmarks()
display(df) # This particular module can be used as a benchmark case that is sort of a one size fit all that evaluates the companies based on the financial ratios


