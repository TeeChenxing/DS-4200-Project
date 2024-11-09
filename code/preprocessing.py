import pandas as pd
pd.set_option('display.max_columns', None)

class DataPreprocessor:
    def __init__(self, file_path, numeric_columns):
        self.file_path = file_path
        self.numeric_columns = numeric_columns
        self.df = None

    def load_data(self):
        """Load the CSV file into a pandas dataframe."""
        self.df = pd.read_csv(self.file_path, low_memory=False)
    
    def preprocess_numeric_columns(self):
        """Preprocess specified columns: remove whitespaces, fill empty rows, and convert to numeric."""
        for column in self.numeric_columns:
            # Replace whitespaces with nothing
            self.df[column] = self.df[column].astype(str).str.replace(" ", "")

            # Fill empty rows with 0 for non-geographical columns
            if column not in ["Latitude", "Longitude"]:
                self.df[column] = self.df[column].replace("", "0").fillna("0")

            # Convert to numeric
            self.df[column] = pd.to_numeric(self.df[column], errors='coerce')

        # FIX THIS
        self.df = self.df[self.df['Number of Engines'] != "Unknown"]


    def preprocess_cat_columns(self, cat_columns):
        """Preprocess specified categorical columns: remove whitespaces."""
        for column in cat_columns:
            # Replace whitespaces with nothing
            self.df[column] = self.df[column].astype(str).str.replace(" ", "")
            
            if column not in ["Broad Phase of Flight"]:
                self.df[column] = self.df[column].replace("", "Unknown").fillna("Unknown")
            
            if column == "Broad Phase of Flight":
                self.df[column] = self.df[column].replace("", "UNKNOWN").fillna("UNKNOWN")

        self.df = self.df[self.df['Broad Phase of Flight'] != "UNKNOWN"]
                
    def preprocess_dateTime_columns(self, dateTime_columns):
        """Preprocess specified datetime columns: convert to datetime."""
        for column in dateTime_columns:
            self.df[column] = pd.to_datetime(self.df[column], errors='coerce')


    def get_dataframe(self):
        """Return the processed dataframe."""
        return self.df