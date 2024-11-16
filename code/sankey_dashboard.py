import panel as pn
import pandas as pd
from sankey import SPSankey
from preprocessing import DataPreprocessor
from panel.widgets import Tabulator

# Load data
file_path = r"C:\Users\Souren Prakash\OneDrive\Desktop\Airplane incidents project\data\airline_accidents.csv"
numeric_columns = ["Total Fatal Injuries", "Total Serious Injuries", "Total Minor Injuries", "Total Uninjured", "Latitude", "Longitude"]
categorical_columns = ["Aircraft Damage", "Broad Phase of Flight", "Aircraft Category", "Purpose of Flight", "Number of Engines", 'Make', 'Model']
dateTime_columns = ["Event Date"]

preprocessor = DataPreprocessor(file_path, numeric_columns)
preprocessor.load_data()
preprocessor.preprocess_numeric_columns()
preprocessor.preprocess_cat_columns(categorical_columns)
preprocessor.preprocess_dateTime_columns(dateTime_columns)
df = preprocessor.get_dataframe()

# Panel extension
pn.extension()

# Widgets for filtering and visualization
Min_Total_Fatal_injuries = pn.widgets.IntSlider(name='Min Total Fatal Injuries', start=1, end=1000, value=1)
checkbox_group = pn.widgets.CheckBoxGroup(name='Checkbox categories', value = ["Number of Engines"], options=["Number of Engines"], inline=True)

# Plot widgets
width = pn.widgets.IntSlider(name="Diagram width", start=250, end=2000, step=125, value=1125)
height = pn.widgets.IntSlider(name="Diagram height", start=200, end=2500, step=100, value=600)
Dimentions = [width, height]

# Dropdown widgets for dynamic selection
columns_dropdown = pn.widgets.Select(name='Select Column', options=["Remove Filter"] + list(df.columns))
values_dropdown = pn.widgets.Select(name='Select Value', options=[])

def update_values_dropdown(selected_column):
    values_dropdown.options = df[selected_column].unique().tolist()

columns_dropdown.param.watch(lambda event: update_values_dropdown(event.new), 'value')

def update_values_dropdown(selected_column):
    if selected_column == "Remove Filter":
        values_dropdown.options = []
    else:
        values_dropdown.options = df[selected_column].unique().tolist()



print(checkbox_group)


def get_plot(df, min_total_fatal_injuries, checkbox_group, dimentions, selected_column, selected_val):
    if selected_column == "Remove Filter":
        filtered_df = df
    elif selected_column and selected_val:
        filtered_df = df[df[selected_column] == selected_val]
    else:
        filtered_df = df

    
    # Access the selected layers through checkbox_group.value
    selected_layers = ["Broad Phase of Flight"] + checkbox_group + ["Aircraft Category"]
    
    grouped_data = preprocessor.group_df(filtered_df, selected_layers, min_total_fatal_injuries)
    sky = SPSankey(grouped_data, 'Values', dimentions, selected_layers)
    fig = sky.make_sankey()
    return fig

# Bind widgets to function
plot = pn.bind(get_plot, df, Min_Total_Fatal_injuries, checkbox_group.value, Dimentions, columns_dropdown.param.value, values_dropdown.param.value)





# Layout components
search_card = pn.Card(pn.Column(Min_Total_Fatal_injuries, checkbox_group), title="Search", width=320, collapsed=True)
plot_card = pn.Card(pn.Column(width, height), title="Plot", width=320, collapsed=True)
menu_card = pn.Card(pn.Column(columns_dropdown, pn.bind(update_values_dropdown, columns_dropdown.param.value), values_dropdown), title="Dropdown", width=320, collapsed=True)

# Final layout
layout = pn.template.FastListTemplate(
    title="Airplane incidents Dashboard",
    sidebar=[search_card, plot_card, menu_card],
    theme_toggle=False,
    main=[pn.Tabs(("Network", plot), ("Data Table", Tabulator(df)), active=0)],
    header_background='#a93226'
)

layout.servable()
layout.show()
