from preprocessing import DataPreprocessor
from interactive_bar import InteractiveBar


def main():
    file_path = "data/airline_accidents.csv"
    numeric_columns = ["Total Fatal Injuries", "Total Serious Injuries", "Total Minor Injuries", "Total Uninjured", "Latitude", "Longitude"]
    categorical_columns = ["Event Date", "Aircraft Damage"] # adjust columns as needed if you need to preprocess that column

    # Initialize the preprocessor
    preprocessor = DataPreprocessor(file_path, numeric_columns)

    # Load and preprocess the data
    preprocessor.load_data()
    preprocessor.preprocess_numeric_columns()
    preprocessor.preprocess_cat_columns(categorical_columns)

    # Get the processed dataframe
    df = preprocessor.get_dataframe()
    
    # Generate and save bar plot
    interactive_bar_plot = InteractiveBar(df)
    interactive_bar_plot.save_plot()

if __name__ == "__main__":
    main()