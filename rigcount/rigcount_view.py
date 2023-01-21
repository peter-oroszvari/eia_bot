import tabulate
from rigcount_controller import RigCountController

def display_data():
    controller = RigCountController()
    data = controller.get_rig_count_data()
    if data:
        print(tabulate.tabulate(data, headers='keys', tablefmt='fancy_grid', maxheadercolwidths=15))
    else: 
        print('No data to display')

display_data()