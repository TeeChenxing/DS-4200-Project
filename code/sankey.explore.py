from sankey import SPSankey
import panel as pn
from panel.widgets import Tabulator
from preprocessing import DataPreprocessor
from interactive_bar import InteractiveBar
from interactive_scatterplot import InteractiveScatterplot
from map import Map

file_path = r"C:\Users\Souren Prakash\OneDrive\Desktop\Airplane incidents project\data\airline_accidents.csv"
numeric_columns = ["Total Fatal Injuries", "Total Serious Injuries", "Total Minor Injuries", "Total Uninjured", "Latitude", "Longitude"]
categorical_columns = ["Aircraft Damage", "Broad Phase of Flight", "Aircraft Category", "Purpose of Flight", "Number of Engines"] # adjust columns as needed if you need to preprocess that column
dateTime_columns = ["Event Date"]

# Initialize the preprocessor
preprocessor = DataPreprocessor(file_path, numeric_columns)

# Load and preprocess the data
preprocessor.load_data()
preprocessor.preprocess_numeric_columns()
preprocessor.preprocess_cat_columns(categorical_columns)
preprocessor.preprocess_dateTime_columns(dateTime_columns)

# Get the processed dataframe
df = preprocessor.get_dataframe()   

print(df.columns)


pn.extension()


#search widgets 

pn.widgets.IntSlider(name='Min Total Fatal Injuries', start = 1, end = 100000, value = 10 )
checkbox_group = pn.widgets.Checkbox(name = 'Checkbox categories', value = ['Make', 'Model', 'Broad Phase of Flight'], 
                                     option=['Make', 'Model', 'Broad Phase of Flight'], inline = True


#plot widgets
width = pn.widgets.IntSlider(name="Diagram width", start=250, end=2000, step=125, value=1125)
height = pn.widgets.IntSlider(name="Diagram height", start=200, end=2500, step=100, value=600)

def grab_selection(df, selected_val = None):
   
    if selected_val:
        val_lst = list(df[selected_col].unique())

        return val_lst
        

def update_values_dropdown(selected_column = None):
    """
    Purpose: Update the selected dropdown values based on the user input of selected column from the dashboard
    Parameter: selected_column (panel widget), the selected column name from the menu widget, the default value is None
    Return: N/A
    Contributor: Souren Prakash
    """
    if selected_column == "Remove Filter":
        values_dropdown.options = []
    else:
        options = grab_selection(selected_column)  # Get unique values from the selected column
        values_dropdown.options = options


columns_dropdown = pn.widgets.Select(name='Select Column', options=["Remove Filter"] + list(can_df.columns))
values_dropdown = pn.widgets.Select(name = 'Select Value', options = [])