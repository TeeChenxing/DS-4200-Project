import altair as alt

class InteractiveBar:
    def __init__(self, dataframe):
        self.df = dataframe

    def create_plot(self):
        # Define the base chart with interactivity
        bar = alt.Chart(self.df).mark_bar().encode(
            alt.X("Broad Phase of Flight:N", title="Phase of Flight"),
            alt.Y("sum(Total Fatal Injuries):Q", title="Fatalities"),
            alt.Color("Number of Engines:N"),
            tooltip=["sum(Total Fatal Injuries):Q", "sum(Total Serious Injuries):Q", "sum(Total Minor Injuries):Q", "sum(Total Uninjured):Q"]
        ).properties(
            title='Total Fatal Injuries During Phase of Flight',
            width=600,
            height=400
        )
        return bar
    
    def save_plot(self, filename="assets/interactive_bar_chart.html"):
        plot = self.create_plot()

        # Save the plot to the specified filename
        plot.save(filename) 
        print(f"Successfully saved interactive bar plot to {filename}!")
