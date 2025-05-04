import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
import FinancialRatios as FR # this module seeks to provide a dynamic code to prepare a dashboard.

class FinBoard:
    def __init__(self, file_name): # uses a typical constructor type method
        self.analyzer = FR.FinancialRatios(file_name) # this particualr part calls on the class FinancialRatios from the respective module
        self.results = self.analyzer.mainFunction() # it runs the main function and calculates financial ratios and gets a dictionary
        self.app = dash.Dash(__name__) # this creates a dash application instance

    def create_dashboard(self):
        categories = ["Liquidity Ratios", "Turnover Ratios", "Profitability Ratios", "Leverage Ratios", "Shareholder Ratios"]

        plots = [] # used for storing the plots

        for category in categories:
            current_year_metrics = self.results["Current Year"].get(category, {}) # this code and the following gets current and previous ratio data for each cat
            previous_year_metrics = self.results["Previous Year"].get(category, {}) # the .get(category) makes usre that the missing categories dont cause any errors

            for metric in current_year_metrics.keys(): # This is used for looping each ratio within the selected category
                try:
                    curr_value = float(str(current_year_metrics[metric]).replace('%', '')) # converts string to float and removes the % sybol
                    prev_value = float(str(previous_year_metrics[metric]).replace('%', ''))

                    data = pd.DataFrame({  # this makes a dataframe in order to store the ratio values for the two years
                        "Year": ["Current Year", "Previous Year"],
                        "Value": [curr_value, prev_value]
                    })

                    fig_bar = px.bar( # This is used for making a bar chart and comparing the ratio between the two years
                        data, x="Year", y="Value", 
                        title=f"{metric} ({category}): Bar Chart", 
                        labels={"Value": metric}, 
                        text_auto=True
                    )

                    fig_line = px.line(
                        data, x="Year", y="Value", 
                        title=f"{metric} ({category}): Yearly Trend", 
                        markers=True, labels={"Value": metric}
                    )

                    plots.append(html.H3(f"{metric} ({category})")) # it adds a title and the visualization to the particular plots list
                    plots.append(dcc.Graph(figure=fig_bar))
                    plots.append(dcc.Graph(figure=fig_line))

                except ValueError: # if at all the conversion fails it skips it
                    continue

        self.app.layout = html.Div(children=[html.H1("Financial Ratios Dashboard")] + plots) # it makes a dashboard layout with a key heading and the plots that are stored within the list

    def run_dashboard(self):
        self.create_dashboard() # this command is used for setting up the layout
        self.app.run(debug=True) # this starts the web application

