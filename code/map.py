import geopandas as gpd
import plotly.express as px
from shapely.geometry import Point


class Map:
    def __init__(self, dataframe):
        self.df = dataframe

    def create_map(self):
        # Filter for U.S. incidents
        us_df = self.df[self.df['Country'] == " United States "]

        us_df.dropna(subset=["Latitude"], inplace=True)
        us_df.dropna(subset=["Latitude"], inplace=True)

        us_df1 = us_df.copy()
        us_df1["Injury Incidents"] = (
                us_df["Total Fatal Injuries"] +
                us_df["Total Serious Injuries"] +
                us_df["Total Minor Injuries"]
        )

        # Create a geometry column with Point data type for GeoPandas
        us_df2 = us_df1.copy()
        us_df2['geometry'] = [Point(xy) for xy in zip(us_df2['Longitude'], us_df2['Latitude'])]

        # Convert to a GeoDataFrame
        gdf = gpd.GeoDataFrame(us_df2, geometry='geometry')

        # Plot the map using Plotly Express with the U.S. boundary as background
        fig = px.density_mapbox(
            gdf,
            lat=gdf.geometry.y,
            lon=gdf.geometry.x,
            z="Injury Incidents",
            hover_name="Broad Phase of Flight",
            hover_data={
                "Total Fatal Injuries": True,
                "Total Serious Injuries": True,
                "Total Minor Injuries": True,
                "Total Uninjured": True
            },
            color_continuous_scale="Reds",
            range_color=(0, gdf["Total Fatal Injuries"].max()+10),
            title="Aviation Incidents in the US",
            mapbox_style="carto-positron",
            zoom=3,
            center={"lat": 37.0902, "lon": -95.7129}
        )

        fig.update_layout(margin={"r":0,"t":50,"l":0,"b":0})

        return fig

    def save_map(self, filename="/assets/incident_map.html"):
        fig = self.create_map()
        fig.write_html(filename)
        #print(f"Map saved as {filename}!")