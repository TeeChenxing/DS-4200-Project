import pandas as pd
import plotly.graph_objects as go


class SPSankey:
    def __init__(self, df, val_col, *arg, **kwargs):
        """
        Initialize the Sankey class with a dataframe, value column, and other column names.
        """
        self.df = df
        self.val_col = val_col
        self.columns = list(kwargs.values())  # Get the list of column names from kwargs
        self.arg = arg

    def code_mapping(self):
        """
        Create a mapping of unique values in 'src' and 'targ' to integer codes.
        """
        sources = {}
        i = 0
        for name in pd.concat([self.df['src'], self.df['targ']]).unique():
            sources[name] = i
            i += 1
        self.df = self.df.replace({'src': sources, 'targ': sources})
        self.labels = list(sources.keys())
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
        Create and display the Sankey diagram.
        """
        self.stacking()
        self.code_mapping()

        values = self.df[self.val_col] if self.val_col else [1] * len(self.df)
        link = {'source': self.df['src'], 'target': self.df['targ'], 'value': values}
        node = {'label': self.labels}

        sk = go.Sankey(link=link, node=node)
        fig = go.Figure(sk)
        width = self.arg[0]
        height = self.arg[1]

        fig.update_layout(autosize=False, width=width, height=height)
        fig.show()
        return fig


def main():
    # Sample data
    data = {'A': ['u', 'u', 'u', 'v'],
            'B': ['x', 'y', 'y', 'x'],
            'C': ['p', 'p', 'q', 'p'],
            'Values': [10, 20, 15, 15]}
    df = pd.DataFrame(data)

    # Initialize Sankey class and generate Sankey diagram
    sankey_obj = SPSankey(df, 'Values', width=600, height=400, col1='A', col2='B', col3='C')
    sankey_obj.make_sankey()

    # Initialize df_adjustments class and group data
    df_adj = df_adjustments()
    grouped_df = df_adj.grouping(df, ['A', 'B'])
    print(grouped_df)


if __name__ == '__main__':
    main()
