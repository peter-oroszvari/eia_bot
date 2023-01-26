import tabulate
import pandas as pd
import dataframe_image as dfi

class RigCountView:
    def display_data(self, data):
        rigcount = tabulate.tabulate(data, headers='keys', tablefmt='fancy_grid')
        # print(rigcount)
        df = pd.DataFrame(data)
        df = df.set_index('Area')
        df.style.set_properties(align='center')
        # print(df)
        dfi.export(df, 'dataframe.png')