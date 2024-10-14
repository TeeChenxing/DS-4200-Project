from preprocessing import DataPreprocessor
from interactive_bar import InteractiveBar


def main():
    file_path = "data/airline_accidents.csv"
    process_columns = ["Total Fatal Injuries", "Total Serious Injuries", "Total Minor Injuries", "Total Uninjured", "Latitude", "Longitude"]

    # Initialize the preprocessor
    preprocessor = DataPreprocessor(file_path, process_columns)

    # Load and preprocess the data
    preprocessor.load_data()
    preprocessor.preprocess_columns()

    # Get the processed dataframe
    df = preprocessor.get_dataframe()
    
    interactive_plot = InteractiveBar(df)
    chart = interactive_plot.create_plot()
    chart.display()
    
if __name__ == "__main__":
    main()