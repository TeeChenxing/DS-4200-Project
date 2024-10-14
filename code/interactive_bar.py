import altair as alt
import pandas as pd

class InteractiveBar:
    def __init__(self, dataframe):
        self.df = dataframe

    def create_plot(self):
        # Define the 4 columns for the user to toggle between
        injury_columns = ["Total Fatal Injuries", "Total Serious Injuries", "Total Minor Injuries", "Total Uninjured"]

        # Create a selection dropdown that allows toggling between columns
        dropdown = alt.binding_select(options=injury_columns, name="Injury Type: ")
        selection = alt.param(bind=dropdown, value="Total Fatal Injuries")

        # Define the base chart with interactivity
        bar = alt.Chart(self.df).mark_bar().encode(
            alt.X("value:Q", title="Count"),
            alt.Y("column:N", title="Injury Type"),
            tooltip=["column:N", "value:Q"]
            ).transform_filter(
                selection
            ).properties(
                width=600,
                height=400
            )

        # Combine the chart with the interactive selection
        return bar.add_params(selection)