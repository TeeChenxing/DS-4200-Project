from preprocessing import DataPreprocessor
from sankey import SPSankey
def grouping_data(df, new_column, **kwargs):
    """

    :param df: dataframe that data has been formatted
    :param new_column: the name of a new column
    :param kwargs: the different groups that you want to group by
    :return: returns a dataframe that adds that column that was grouped by
    """
    groupings = list(kwargs.values())
    combined_filter = df.groupby(groupings).size().reset_index(name=new_column)
    return combined_filter

def main():
    file_path = "data/airline_accidents.csv"
    numeric_columns = ["Total Fatal Injuries"]
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


#dropping any rows that have unknown
    df = df[~df.eq('Unknown').any(axis=1)]
    #plot 1
    Aircraft_category = grouping_data(df,'fatality_amount', group1 = "Broad Phase of Flight",group2 = "Aircraft Category")
    #print(engine_type)
    sk = SPSankey(Aircraft_category,'fatality_amount', ["Broad Phase of Flight", "Aircraft Category"], width=1000, height=1000 )
    fig = sk.make_sankey()

    fig.write_html("sankey_plot_1.html")
    


    #creating a larger group to plot 
    ["Aircraft Damage", "Broad Phase of Flight", "Aircraft Category", "Purpose of Flight", "Number of Engines"] 

    purpose_flight = grouping_data(df,'fatality_amount', group1 = "Purpose of Flight", group2 = "Broad Phase of Flight", group3 = "Aircraft Category")
    sk = SPSankey(purpose_flight, 'fatality_amount',[ "Purpose of Flight", "Broad Phase of Flight", "Aircraft Category"], width=1000, height=1000 )
    fig = sk.make_sankey()

    fig.write_html("sankey_plot_2.html") 

main()