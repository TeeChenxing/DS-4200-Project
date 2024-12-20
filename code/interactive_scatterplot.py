import altair as alt
import pandas as pd

class InteractiveScatterplot:
    def __init__(self, dataframe):
        self.df = dataframe
        
        # Filter the dataframe to only include events with at least one fatality and valid engine counts (1, 2, 3, or 4)
        self.df_fatalities = self.df[(self.df['Total Fatal Injuries'] > 0) & (self.df['Number of Engines'].isin([1, 2, 3, 4])) & (self.df['Event Date'] >= '1980-01-01')]


    def create_plot(self):
        # Define the scatter plot with interactivity
        # This scatter plot looks at fatal injuries over time
        # With an interactive aspect which shows you incident data when you hover over a point, as well as moving and zooming capabilities
        # Enable CSV transformer for handling large datasets
        alt.data_transformers.enable('csv')

        # Filter the dataframe to only include events with at least one fatality
        df_fatalities = self.df_fatalities

        # Define a slider for filtering by the minimum number of fatalities
        slider_cutoff = alt.binding_range(min=0, max=df_fatalities['Total Fatal Injuries'].max(), step=1, name="Min Fatalities: ")
        slider_selection = alt.param(bind=slider_cutoff, value=0)  # Default slider value is 0

        # Define an interactive selection for aircraft damage
        input_radio = alt.binding_radio(
            options=['Destroyed','Substantial' , 'Minor', 'Unknown', None],
            labels=['Destroyed','Substantial' , 'Minor', 'Unknown', 'All'],
            name="Aircraft Damage: "
        )
        damage_filter = alt.selection_point(fields=['Aircraft Damage'], bind=input_radio)

        # Define a zoom selection
        zoom = alt.selection_interval(bind='scales')

        # Define the base chart with square root scale, conditional opacity, and filters
        scatter = alt.Chart(df_fatalities).mark_circle().encode(
            alt.X('Event Date:T', title='Date'),
            alt.Y('Total Fatal Injuries:Q', title='Fatal Injuries', scale=alt.Scale(type='sqrt')),
            alt.Color('Aircraft Damage:N', title='Aircraft Damage',
                    scale=alt.Scale(domain=['Destroyed','Substantial', 'Minor', 'Unknown'],
                                    range=['red', '#FF8C00', '#FFBF00', 'grey'])),
            tooltip=['Event Date:T', 'Total Fatal Injuries:Q', 'Aircraft Damage:N', 'Location:O',
                    'Total Serious Injuries:Q', 'Total Minor Injuries:Q', 'Total Uninjured:Q']
        ).add_params(
            slider_selection,
            damage_filter,
            zoom
        ).transform_filter(
            (alt.datum['Total Fatal Injuries'] >= slider_selection)  # Filter based on slider
        ).transform_filter(
            damage_filter  # Filter based on damage selection
        ).properties(
            title='Total Fatal Aircraft Injuries Over Time (Starting from 1980)',
            height=500,
            width=600
        )
        return scatter
    
    def create_sum_plot(self):
        
         # Enable CSV transformer for handling large datasets
        alt.data_transformers.enable('csv')
        
        df_fatalities = self.df_fatalities
        
        # Convert 'Event Date' to datetime if it's not already
        df_fatalities['Event Date'] = pd.to_datetime(df_fatalities['Event Date'])

        # Create a new 'Event Month' column and aggregate fatalities by month and number of engines since 1980
        df_fatalities['Event Month'] = df_fatalities['Event Date'].dt.strftime('%B %Y')# Add month name with year for display
        df_fatalities_sum = (df_fatalities[df_fatalities['Event Date'] >= '1980-01-01']
                            .groupby(['Event Month', 'Number of Engines'])
                            .agg({'Total Fatal Injuries': 'sum'})
                            .reset_index()
                            .rename(columns={'Total Fatal Injuries': 'Total Fatalities'}))

        # Define an interactive selection for the number of engines with options as strings
        engine_filter = alt.selection_point(fields=['Number of Engines'], 
                                            bind=alt.binding_radio(name='Filter by Number of Engines', options=['1', '2', '3', '4']),
                                            name='EngineFilter')

        # Define base chart with square root scale on the y-axis, color by engine type, and conditional opacity based on filter
        sumPlot = alt.Chart(df_fatalities_sum).mark_circle().encode(
            alt.X('Event Month:T', title='Date'),
            alt.Y('Total Fatalities:Q', title='Total Fatalities per Month', scale=alt.Scale(type='sqrt')),  # Square root scale applied here
            alt.Color('Number of Engines:N', title='Number of Engines'),  # Color points by number of engines
            opacity=alt.condition(engine_filter, alt.value(1), alt.value(0.1)),  # Full opacity for selected points, reduced for others
            tooltip=[alt.Tooltip('Event Month:T', format='%B, %Y'),
                    alt.Tooltip('Total Fatalities:Q'),
                    alt.Tooltip('Number of Engines:N')]
        ).add_params(
            engine_filter
        ).properties(
            title='Sum of Fatal Aircraft Fatalities per Month Since 1980, by Number of Engines',
            height=500,
            width=600
        )
        
        return sumPlot
    
    def save_plot(self):
        plot = self.create_plot()
        sum_plot = self.create_sum_plot()

        # Save the plot to the specified filename
        plot.save("assets/interactive_scatterplot.html") 
        print(f"Successfully saved interactive scatter plot to assets/interactive_scatterplot.html!")
        
        sum_plot.save("assets/summed_interactive_scatterplot.html")
        print(f"Successfully saved summed interactive scatter plot to assets/summed_interactive_scatterplot.html!")