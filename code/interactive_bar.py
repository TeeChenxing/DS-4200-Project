import altair as alt

class InteractiveBar:
    def __init__(self, dataframe):
        self.df = dataframe

    def create_plot(self):
        # Filter out unknown number of engines for this visualization
        self.df = self.df[self.df['Number of Engines'] != "Unknown"]

        # Create a selection by Number of Engines
        input_radio = alt.binding_radio(options=['0', '1', '2', '3', '4'],
                                        labels=['0', '1', '2', '3', '4'],
                                        name="Number of Engines:")
        selection = alt.selection_point(fields=['Number of Engines'], bind=input_radio)

        # Define color domain and scale
        domain = ['0', '1', '2', '3', '4']
        color_scale = alt.Scale(domain=domain, scheme='oranges')

        # Chart 1: Bar chart showing all engines
        bar_all = alt.Chart(self.df).mark_bar().encode(
            alt.X("Broad Phase of Flight:N", title="Phase of Flight",
                  sort=alt.EncodingSortField(field="Total Fatal Injuries", op="sum", order="descending")),
            alt.Y("sum(Total Fatal Injuries):Q", title="Fatalities"),
            color=alt.Color('Number of Engines:N', scale=color_scale),
            tooltip=["sum(Total Fatal Injuries):Q", "sum(Total Serious Injuries):Q", 
                     "sum(Total Minor Injuries):Q", "sum(Total Uninjured):Q"]
        ).properties(
            title='Total Injuries During Phase of Flight (All Engines)',
            width=600,
            height=300
        )

        # Chart 2: Bar chart filtered by selected engine number
        bar_filtered = alt.Chart(self.df).mark_bar().encode(
            alt.X("Broad Phase of Flight:N", title="Phase of Flight",
                  sort=alt.EncodingSortField(field="Total Fatal Injuries", op="sum", order="descending")),
            alt.Y("sum(Total Fatal Injuries):Q", title="Fatalities"),
            color=alt.condition(selection, 'Number of Engines:N', alt.value('lightgrey'), scale=color_scale),
            tooltip=["sum(Total Fatal Injuries):Q", "sum(Total Serious Injuries):Q", 
                     "sum(Total Minor Injuries):Q", "sum(Total Uninjured):Q"]
        ).properties(
            title='Total Injuries During Phase of Flight (Filtered by Engine #)',
            width=600,
            height=300
        ).add_params(selection).transform_filter(selection)

        # Combine the two charts vertically
        combined_chart = alt.vconcat(bar_all, bar_filtered).resolve_scale(
            color='independent'
        )

        return combined_chart

    def save_plot(self, filename="/assets/interactive_bar_chart.html"):
        plot = self.create_plot()

        # Save the plot to the specified filename
        plot.save(filename)
        print(f"Successfully saved interactive bar plot to {filename}!")