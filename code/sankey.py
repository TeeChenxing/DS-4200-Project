import pandas as pd
import plotly.graph_objects as go

class SPSankey:
    def __init__(self, df, val_col, columns, width=600, height=400):
        """
        Initialize the Sankey class with a dataframe, value column, other column names,
        and optional width and height for the figure.
        """
        self.df = df
        self.val_col = val_col
        self.columns = columns  # List of columns
        self.width = width      # Width of the Sankey diagram (default: 600)
        self.height = height    # Height of the Sankey diagram (default: 400)
        self.labels = []        # Node labels will be created later

    def code_mapping(self):
        """
        Create a mapping of unique values in 'src' and 'targ' to integer codes.
        """
        sources = {}
        i = 0
        # Combine the unique values from both 'src' and 'targ' columns
        for name in pd.concat([self.df['src'], self.df['targ']]).unique():
            sources[name] = i
            i += 1
        # Replace the source and target columns with their integer codes
        self.df = self.df.replace({'src': sources, 'targ': sources})
        self.labels = list(sources.keys())  # The unique values will be the labels for nodes
        return self.df, self.labels

    def stacking(self):
        """
        Stack the dataframe by creating 'src' and 'targ' columns for the Sankey diagram.
        """
        stacked_data = pd.DataFrame()
        for i in range(len(self.columns) - 1):
            src_col = self.columns[i]
            targ_col = self.columns[i + 1]
            temp_df = self.df[[src_col, targ_col, self.val_col]]
            temp_df = temp_df.rename(columns={src_col: 'src', targ_col: 'targ'})
            temp_df = temp_df.groupby(['src', 'targ'])[self.val_col].sum().reset_index()
            stacked_data = pd.concat([stacked_data, temp_df], ignore_index=True)
        stacked_data = stacked_data.dropna()
        self.df = stacked_data
        return self.df

    def make_sankey(self):
        """
        Create and display the Sankey diagram with labels on nodes.
        """
        self.stacking()
        self.code_mapping()

        values = self.df[self.val_col] if self.val_col else [1] * len(self.df)
        link = {'source': self.df['src'], 'target': self.df['targ'], 'value': values}
        
        # Create the node dictionary with the 'label' being the node labels
        node = {'label': self.labels}

        # Generate Sankey diagram
        sk = go.Sankey(link=link, node=node)
        fig = go.Figure(sk)

        # Set the figure size using class variables
        fig.update_layout(
            autosize=True,
            title_text=f"Sankey Diagram for {', '.join(self.columns)}",
            width=self.width,
            height=self.height
        )
        fig.show()
        return fig

def main():
    # Sample data
    data = {'A': ['u', 'u', 'u', 'v'],
            'B': ['x', 'y', 'y', 'x'],
            'C': ['p', 'p', 'q', 'p'],
            'Values': [10, 20, 15, 15]}
    df = pd.DataFrame(data)

    # Initialize Sankey class and generate Sankey diagram with specified width and height
    sankey_obj = SPSankey(df, 'Values', ['A', 'B', 'C'], width=800, height=600)
    sankey_obj.make_sankey()

if __name__ == '__main__':
    main()
