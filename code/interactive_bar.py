import altair as alt

class InteractiveBar:
    def __init__(self, dataframe):
        self.df = dataframe

    def create_plot(self):

        # Remove unknown number of engines just for this bar chart
        self.df = self.df[self.df['Number of Engines'] != "Unknown"]

        # Create a selection by Number of Engines
        input_radio = alt.binding_radio(options=['0', '1', '2', '3', '4', None],
                                        labels=['0', '1', '2', '3', '4', 'All'],
                                        name="Number of Engines:")
        selection = alt.selection_point(fields=['Number of Engines'], bind=input_radio)
        #color=alt.condition(selection, 'region:N', alt.value('grey'), scale=alt.Scale(domain=domain, scheme='category10')
        # Define the base chart with interactivity (tooltip and selection by # of engine)
        domain = ['0', '1', '2', '3', '4']
        bar = alt.Chart(self.df).mark_bar().encode(
            alt.X("Broad Phase of Flight:N", title="Phase of Flight",
                  sort=alt.EncodingSortField(field="Total Fatal Injuries", op="sum", order="descending")),
            alt.Y("sum(Total Fatal Injuries):Q", title="Fatalities"),
            color=alt.condition(selection, 'Number of Engines:N', alt.value('lightgrey'), scale=alt.Scale(domain=domain, scheme='oranges')),
            tooltip=["sum(Total Fatal Injuries):Q", "sum(Total Serious Injuries):Q", "sum(Total Minor Injuries):Q", "sum(Total Uninjured):Q"]
        ).properties(
            title='Total Fatal Injuries During Phase of Flight',
            width=600,
            height=400
        ).add_params(selection).transform_filter(selection)
        return bar
    
    def save_plot(self, filename="/Users/andreakeiper/Documents/fall24/ds4200/DS-4200-Project/assets/interactive_bar_chart.html"):
        plot = self.create_plot()

        # Save the plot to the specified filename
        plot.save(filename)
        print(f"Successfully saved interactive bar plot to {filename}!")
