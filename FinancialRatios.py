import pandas as pd

class FinancialRatios: # it is important to note that market price per share and shares outstanding are exogeneous variables hence they are to be asked as input
    def __init__(self, efile):
        self.efile = efile
        self.data = pd.read_excel(efile)
        
        self.current_balance_sheet = self.data.iloc[:51, :2]
        self.current_balance_sheet.columns = ["Particulars", "CY"]
        self.current_balance_sheet.fillna(0, inplace=True)
        self.current_income_statement = self.data.iloc[52:76, :2]
        self.current_income_statement.columns = ["Particulars", "CY"]
        self.current_income_statement.fillna(0, inplace=True)
        self.current_cash_flow = self.data.iloc[76:131, :2]
        self.current_cash_flow.columns = ["Particulars", "CY"]
        self.current_cash_flow.fillna(0, inplace=True)
        self.previous_balance_sheet = self.data.iloc[:51, [0, 2]]
        self.previous_balance_sheet.columns = ["Particulars", "PY"]
        self.previous_balance_sheet.fillna(0, inplace=True)
        self.previous_income_statement = self.data.iloc[52:76, [0, 2]]
        self.previous_income_statement.columns = ["Particulars", "PY"]
        self.previous_income_statement.fillna(0, inplace=True)
        self.previous_cash_flow = self.data.iloc[76:131, [0, 2]]
        self.previous_cash_flow.columns = ["Particulars", "PY"]
        self.previous_cash_flow.fillna(0, inplace=True)

# The above commands are done in order to ensure that the financial statements of the company in question are clearly segregated as to whether it pertains to the current or previous year.

    
    def liquidity_ratios(self, year="CY"):
        try:
            if year == "CY":
                bs = self.current_balance_sheet
            else:
                bs = self.previous_balance_sheet
                
            current_assets_row = bs[bs["Particulars"].str.lower().str.contains("total - current assets", case=False, na=False)]
            if not current_assets_row.empty:
                current_assets = float(current_assets_row[year].iloc[0])
            else:
                current_assets = 0
            
            current_liabilities_row = bs[bs["Particulars"].str.lower().str.contains("total - current liabilities", case=False, na=False)]
            if not current_liabilities_row.empty:
                current_liabilities = float(current_liabilities_row[year].iloc[0])
            else:
                current_liabilities = 0
            
            inventory_row = bs[bs["Particulars"].str.lower().str.contains("inventories", case=False, na=False)]
            if not inventory_row.empty:
                inventory = float(inventory_row[year].iloc[0])
            else:
                inventory = 0
            
            if current_liabilities > 0:
                current_ratio = current_assets / current_liabilities
            else:
                current_ratio = 0
            
            quick_assets = current_assets - inventory
            if current_liabilities > 0:
                quick_ratio = quick_assets / current_liabilities
            else:
                quick_ratio = 0
            
            year_label = "Current Year" if year == "CY" else "Previous Year"
            print(f"==== Liquidity Ratios ({year_label}) ====")
            print(f"Current ratio: {round(current_ratio, 2)}")
            print(f"Quick ratio: {round(quick_ratio, 2)}")
            print(f"Current assets: {current_assets}")
            print(f"current liabilities: {current_liabilities}")
            print(f"inventory: {inventory}")
            
            return {
                "Current ratio": round(current_ratio, 2),
                "Quick ratio": round(quick_ratio, 2),
                "Current assets": current_assets,
                "Current liabilities": current_liabilities,
                "inventory": inventory
            }
        except Exception as e:
            print(f"The error that you are facing right now is likely to be: ({year}): {e}")
            return {
                "Current Ratio": "NP",
                "Quick Ratio": "NP",
            }
# NP used in the above commands refers to not possible (that is the calculation of the particular ratio is not possible)
    def turnover_ratios(self, year="CY"):
        try:
            if year == "CY":
                is_df = self.current_income_statement
                bs = self.current_balance_sheet
            else:
                is_df = self.previous_income_statement
                bs = self.previous_balance_sheet
# COGS cannot be direcly derieved from the financials since it includes a number of items such as the ones listed below                
            cogs_accounts = [
                "Cost of materials consumed",
                "Purchases of Stock-in-trade",
                "Changes in inventories of finished goods, work-in-progress and stock-in-trade"
            ]
            
            cogs = 0
            for account in cogs_accounts:
                cogs_row = is_df[
                    is_df["Particulars"].str.lower().str.contains(account.lower(), case=False, na=False)
                ]
                if not cogs_row.empty:
                    cogs += cogs_row[year].sum()
            
            inventory_row = bs[bs["Particulars"].str.lower().str.contains("inventories", case=False, na=False)]
            if not inventory_row.empty:
                inventory = float(inventory_row[year].iloc[0])
            else:
                inventory = 0
            
            if cogs > 0:
                inventory_turnover = cogs / inventory
            else:
                inventory_turnover = 0
            
            if inventory_turnover > 0:
                days_inventory = 365 / inventory_turnover
            else:
                days_inventory = 0
            
            year_label = "Current Year" if year == "CY" else "Previous Year"
            print(f"==== Turnover Ratios ({year_label}) ====")
            print(f"Inventory Turnover (Inventory/COGS): {round(inventory_turnover, 2)}")
            print(f"Days Inventory on Hand: {round(days_inventory, 1)}")
            print(f"Cost of Goods Sold: {cogs}")
            print(f"Inventory: {inventory}")
            
            return {
                "Inventory Turnover": round(inventory_turnover, 2),
                "Days Inventory on Hand": round(days_inventory, 1),
                "Cost of Goods Sold": cogs,
                "Inventory": inventory
            }
        except Exception as e:
            print(f"The error that you are facing right now is:({year}): {str(e)}")
            return {
                "Inventory Turnover": "NA",
                "Days Inventory on Hand": "NA",
            }
# NA in the above commands refers to not applicable    
    def profitability_ratios(self, year="CY"):
        try:
            if year == "CY":
                is_df = self.current_income_statement
                bs = self.current_balance_sheet
            else:
                is_df = self.previous_income_statement
                bs = self.previous_balance_sheet
                
            revenue_row = is_df[is_df["Particulars"] == "TOTAL INCOME"]
            if not revenue_row.empty:
                revenue = float(revenue_row[year].iloc[0])
            else:
                revenue = 0
            
            net_income_row = is_df[is_df["Particulars"] == "PROFIT FOR THE YEAR (A)"]
            if not net_income_row.empty:
                net_income = float(net_income_row[year].iloc[0])
            else:
                net_income = 0
            
            total_equity_row = bs[bs["Particulars"].str.lower().str.contains("total - equity", case=False, na=False)]
            if not total_equity_row.empty:
                total_equity = float(total_equity_row[year].iloc[0])
            else:
                total_equity = 0
            
            total_assets_row = bs[bs["Particulars"].str.lower().str.contains("total assets", case=False, na=False)]
            if not total_assets_row.empty:
                total_assets = float(total_assets_row[year].iloc[0])
            else:
                total_assets = 0
            
            cogs_accounts = [
                "Cost of materials consumed",
                "Purchases of Stock-in-trade",
                "Changes in inventories of finished goods, work-in-progress and stock-in-trade"
            ]
            
            cogs = 0
            for account in cogs_accounts:
                cogs_row = is_df[
                    is_df["Particulars"].str.lower().str.contains(account.lower(), case=False, na=False)
                ]
                if not cogs_row.empty:
                    cogs += cogs_row[year].sum()
            
            pbt_row = is_df[is_df["Particulars"] == "Profit before tax"]
            if not pbt_row.empty:
                pbt = float(pbt_row[year].iloc[0])
            else:
                pbt = 0
            
            gross_profit = revenue - cogs
            
            if revenue > 0:
                gross_profit_margin = (gross_profit / revenue) * 100
                net_profit_margin = (net_income / revenue) * 100
                pbt_margin = (pbt / revenue) * 100
            else:
                gross_profit_margin = 0
                net_profit_margin = 0
                pbt_margin = 0
            
            if total_equity > 0:
                roe = (net_income / total_equity) * 100
            else:
                roe = 0
            
            if total_assets > 0:
                roa = (net_income / total_assets) * 100
            else:
                roa = 0
            
            year_label = "Current Year" if year == "CY" else "Previous Year"
            print(f"==== Profitability Ratios ({year_label}) ====")
            print(f"Gross Profit Margin: {round(gross_profit_margin, 2)}%")
            print(f"Net Profit Margin: {round(net_profit_margin, 2)}%")
            print(f"Profit Before Tax Margin: {round(pbt_margin, 2)}%")
            print(f"Return on Equity (ROE): {round(roe, 2)}%")
            print(f"Return on Assets (ROA): {round(roa, 2)}%")
            print(f"Gross Profit: {gross_profit}")
            print(f"Total Revenue: {revenue}")
            print(f"Net Profit: {net_income}")
            
            return {
                "Gross Profit Margin": f"{round(gross_profit_margin, 2)}%",
                "Net Profit Margin": f"{round(net_profit_margin, 2)}%",
                "Profit Before Tax Margin": f"{round(pbt_margin, 2)}%",
                "Return on Equity (ROE)": f"{round(roe, 2)}%",
                "Return on Assets (ROA)": f"{round(roa, 2)}%",
                "Gross Profit": gross_profit,
                "Total Revenue": revenue,
                "Net Profit": net_income
            }
        except Exception as e:
            print(f"The error that you might be potentially facing right now is:({year}): {e}")
            return {
                "Gross Profit Margin": "NA",
                "Net Profit Margin": "NA",
                "Return on Equity (ROE)": "NA",
                "Return on Assets (ROA)": "NA",
            }
    
    def Leverage_Ratios(self, year="CY"):
        try:
            if year == "CY":
                bs = self.current_balance_sheet
            else:
                bs = self.previous_balance_sheet
                
            debt_row = bs[bs["Particulars"].str.lower().str.contains("total debt", case=False, na=False)]
            
            if debt_row.empty:
                long_term_debt_row = bs[bs["Particulars"].str.lower().str.contains("borrowings", case=False, na=False) & 
                                       ~bs["Particulars"].str.lower().str.contains("current", case=False, na=False)]
                if not long_term_debt_row.empty:
                    long_term_debt = long_term_debt_row[year].sum()
                else:
                    long_term_debt = 0
                
                short_term_debt_row = bs[
                    bs["Particulars"].str.lower().str.contains("current", case=False, na=False) & 
                    bs["Particulars"].str.lower().str.contains("borrowings", case=False, na=False)
                ]
                if not short_term_debt_row.empty:
                    short_term_debt = short_term_debt_row[year].sum()
                else:
                    short_term_debt = 0
                
                total_debt = long_term_debt + short_term_debt
            else:
                total_debt = float(debt_row[year].iloc[0])
            
            total_equity_row = bs[bs["Particulars"].str.lower().str.contains("total - equity", case=False, na=False)]
            if not total_equity_row.empty:
                total_equity = float(total_equity_row[year].iloc[0])
            else:
                total_equity = 0
            
            total_assets_row = bs[bs["Particulars"].str.lower().str.contains("total assets", case=False, na=False)]
            if not total_assets_row.empty:
                total_assets = float(total_assets_row[year].iloc[0])
            else:
                total_assets = 0
            
            if total_equity > 0:
                debt_to_equity = total_debt / total_equity
            else:
                debt_to_equity = 0
            
            if total_assets > 0:
                debt_to_assets = total_debt / total_assets
            else:
                debt_to_assets = 0
            
            year_label = "Current Year" if year == "CY" else "Previous Year"
            print(f"==== Leverage Ratios ({year_label}) ====")
            print(f"Debt-to-Equity Ratio: {round(debt_to_equity, 2)}")
            print(f"Debt-to-Assets Ratio: {round(debt_to_assets, 2)}")
            print(f"Total Debt: {total_debt}")
            print(f"Shareholder Equity: {total_equity}")
            print(f"Total Assets: {total_assets}")
            
            return {
                "Debt-to-Equity Ratio": round(debt_to_equity, 2),
                "Debt-to-Assets Ratio": round(debt_to_assets, 2),
                "Total Debt": total_debt,
                "Shareholder Equity": total_equity,
                "Total Assets": total_assets
            }
        except Exception as e:
            print(f"teh error that you are facing is likely to be: ({year}): {e}")
            return {
                "Debt-to-Equity Ratio": "error",
                "Debt-to-Assets Ratio": "error",
            }
    
    def Other_ratios(self, shares_outstanding=None, market_price=None, year="CY"):
        try:
            if year == "CY":
                is_df = self.current_income_statement
                cf = self.current_cash_flow
            else:
                is_df = self.previous_income_statement
                cf = self.previous_cash_flow
                
            net_income_row = is_df[is_df["Particulars"] == "PROFIT FOR THE YEAR (A)"]
            if not net_income_row.empty:
                net_income = float(net_income_row[year].iloc[0])
            else:
                net_income = 0
            
            dividend_row = cf[cf["Particulars"].str.lower().str.contains("dividend paid", case=False, na=False)]
            if not dividend_row.empty:
                dividends_paid = abs(dividend_row[year].sum())
            else:
                dividends_paid = 0
            
            if shares_outstanding is None:
                shares_outstanding = float(input(f"Please enter the number of shares outstanding for {year} year end: "))
            
            if market_price is None:
                market_price = float(input(f"Please enter market price per share for {year}: "))
            
            if net_income > 0:
                dividend_payout_ratio = (dividends_paid / net_income) * 100
                earnings_retention_ratio = 100 - dividend_payout_ratio
            else:
                dividend_payout_ratio = 0
                earnings_retention_ratio = 0
            
            if shares_outstanding > 0:
                earnings_per_share = (net_income * 10000000) / shares_outstanding
                dividend_per_share = (dividends_paid * 10000000) / shares_outstanding
            else:
                earnings_per_share = 0
                dividend_per_share = 0
            
            if market_price > 0 and dividend_per_share > 0:
                dividend_yield = (dividend_per_share / market_price) * 100
            else:
                dividend_yield = 0
            
            if earnings_per_share > 0 and market_price > 0:
                price_earnings_ratio = market_price / earnings_per_share
            else:
                price_earnings_ratio = 0
            
            year_label = "Current Year" if year == "CY" else "Previous Year"
            print(f"==== Shareholder Ratios ({year_label}) ====")
            print(f"Earnings Per Share (EPS): {round(earnings_per_share, 2)}")
            print(f"Dividend Per Share (DPS): {round(dividend_per_share, 2)}")
            print(f"Dividend Payout Ratio: {round(dividend_payout_ratio, 2)}%")
            print(f"Earnings Retention Rate: {round(earnings_retention_ratio, 2)}%")
            print(f"Dividend Yield: {round(dividend_yield, 2)}%")
            print(f"Price-to-Earnings (P/E) Ratio: {round(price_earnings_ratio, 2)}")
            print(f"Net Profit: {net_income}")
            print(f"Total Dividends Paid: {dividends_paid}")
            
            return {
                "Earnings Per Share (EPS)": round(earnings_per_share, 2),
                "Dividend Per Share": round(dividend_per_share, 2),
                "Dividend Payout Ratio": f"{round(dividend_payout_ratio, 2)}%",
                "Earnings Retention Rate": f"{round(earnings_retention_ratio, 2)}%",
                "Dividend Yield": f"{round(dividend_yield, 2)}%",
                "Price-to-Earnings (P/E) Ratio": round(price_earnings_ratio, 2),
                "Net Profit": net_income,
                "Total Dividends Paid": dividends_paid
            }
        except Exception as e:
            print(f"The error that you are likely to be facing within this function is ({year}): {e}")
            return {
                "Earnings Per Share (EPS)": "NP",
                "Dividend Per Share": "NA",
                "Dividend Yield": "NP",
                "Price-to-Earnings (P/E) Ratio": "NA",
            }
    
    def mainFunction(self, shares_outstanding_cy=None, market_price_cy=None, 
                    shares_outstanding_py=None, market_price_py=None):
        
        
        print("\n========== CURRENT YEAR ANALYSIS ==========\n")
        liquidity_results_cy = self.liquidity_ratios("CY")
        print("=" * 60)
        
        efficiency_results_cy = self.turnover_ratios("CY")
        print("=" * 60)
        
        profitability_results_cy = self.profitability_ratios("CY")
        print("=" * 60)
        
        leverage_results_cy = self.Leverage_Ratios("CY")
        print("=" * 60)
        
        shareholder_results_cy = self.Other_ratios(shares_outstanding_cy, market_price_cy, "CY")
        print("=" * 60)
        
        
        print("\n========== PREVIOUS YEAR ANALYSIS ==========\n") # this is used for printing in a neat and aligned manner
        liquidity_results_py = self.liquidity_ratios("PY")
        print("=" * 60)
        
        efficiency_results_py = self.turnover_ratios("PY")
        print("=" * 60)
        
        profitability_results_py = self.profitability_ratios("PY")
        print("=" * 60)
        
        leverage_results_py = self.Leverage_Ratios("PY")
        print("=" * 60)
        
        shareholder_results_py = self.Other_ratios(shares_outstanding_py, market_price_py, "PY")
        print("=" * 60)
        
        return {
            "Current Year": {
                "Liquidity Metrics": liquidity_results_cy,
                "Efficiency Metrics": efficiency_results_cy,
                "Profitability Metrics": profitability_results_cy,
                "Leverage Metrics": leverage_results_cy,
                "Shareholder Metrics": shareholder_results_cy
            },
            "Previous Year": {
                "Liquidity Metrics": liquidity_results_py,
                "Efficiency Metrics": efficiency_results_py,
                "Profitability Metrics": profitability_results_py,
                "Leverage Metrics": leverage_results_py,
                "Shareholder Metrics": shareholder_results_py
            }
        }




