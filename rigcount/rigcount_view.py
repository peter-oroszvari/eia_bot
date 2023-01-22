import tabulate
from .rigcount_controller import RigCountController
import pandas as pd
import dataframe_image as dfi


def display_data():
    controller = RigCountController()
    data = controller.get_rig_count_data()
    if data:
         rigcount = tabulate.tabulate(data, headers='keys', tablefmt='fancy_grid')
         print(rigcount)
         df = pd.DataFrame(data)
         print(df)
         dfi.export(df, 'dataframe.png')

    else: 
        rigcount = 'No data to display'
    
    return rigcount

display_data()