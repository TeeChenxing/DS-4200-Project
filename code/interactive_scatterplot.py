import altair as alt

class InteractiveScatterplot:
    def __init__(self, dataframe):
        self.df = dataframe

    def create_plot(self):
        # Define the scatter plot with interactivity
        # This scatter plot looks at fatal injuries over time
        # With an interactive aspect which shows you incident data when you hover over a point, as well as moving and zooming capabilities
        
        # Enable CSV transformer for handling large datasets
        alt.data_transformers.enable('csv')
        
        # Filter the dataframe to only include rows with at least 1 fatal injury
        mod_df = self.df[self.df['Total Fatal Injuries'] > 0]
        
        scatter = alt.Chart(mod_df).mark_circle(opacity=0.5).encode(
            alt.X('Event Date:T', title='Date', scale=alt.Scale(type='utc')),
            alt.Y('Total Fatal Injuries:Q', title='Fatal Injuries'), 
            alt.Color('Aircraft Damage:N', title='Aircraft Damage', scale = alt.Scale(domain=['Destroyed', 'Minor', 'Substantial', 'Unknown'], 
                                                                                      range=['red', 'orange', 'yellow', 'grey'])),
            tooltip=['Event Date:T', 'Total Fatal Injuries:Q', 'Aircraft Damage:N', 'Location:O', 'Total Serious Injuries:Q', 'Total Minor Injuries:Q', 'Total Uninjured:Q']
            ).properties(
                title='Total Fatal Aircraft Injuries Over Time (Starting from 1980)',
                height=500,
                width=600
            ).interactive()
            
        return scatter
    
    def save_plot(self, filename="assets/interactive_scatterplot.html"):
        plot = self.create_plot()

        # Save the plot to the specified filename
        plot.save(filename) 
        print(f"Successfully saved interactive scatter plot to {filename}!")