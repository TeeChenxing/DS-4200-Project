from preprocessing import DataPreprocessor
from interactive_bar import InteractiveBar
#from new_int_bar import InterativeBar
from interactive_scatterplot import InteractiveScatterplot
from map import Map

def main():
    file_path = "/data/airline_accidents.csv"
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

    # Generate and save bar plot
    interactive_bar_plot = InteractiveBar(df)
    interactive_bar_plot.save_plot()

    # Generate and save scatter plot
    interactive_scatter_plot = InteractiveScatterplot(df)
    interactive_scatter_plot.save_plot()

    # Generate and save map
    map = Map(df)
    map.save_map()


if __name__ == "__main__":
    main()