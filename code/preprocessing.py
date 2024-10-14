
import pandas as pd
pd.set_option('display.max_columns', None)


class DataPreprocessor:
    def __init__(self, file_path, process_columns):
        self.file_path = file_path
        self.process_columns = process_columns
        self.df = None

    def load_data(self):
        """Load the CSV file into a pandas dataframe."""
        self.df = pd.read_csv(self.file_path)
    
    def preprocess_columns(self):
        """Preprocess specified columns: remove whitespaces, fill empty rows, and convert to numeric."""
        for column in self.process_columns:
            # Replace whitespaces with nothing
            self.df[column] = self.df[column].astype(str).str.replace(" ", "")

            # Fill empty rows with 0 for non-geographical columns
            if column not in ["Latitude", "Longitude"]:
                self.df[column] = self.df[column].replace("", "0").fillna("0")

            # Convert to numeric
            self.df[column] = pd.to_numeric(self.df[column], errors='coerce')
    
    def get_dataframe(self):
        """Return the processed dataframe."""
        return self.df