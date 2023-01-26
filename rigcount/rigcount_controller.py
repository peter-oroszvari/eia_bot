from .rigcount_model import RigCountModel
from .rigcount_view import RigCountView

class RigCountController:
    def __init__(self):
        self.model = RigCountModel()
        self.view = RigCountView()

    def get_rig_count_data(self):
        try:
            data = self.model.get_data()
            cleaned_data = self.model.clean_data(data)
            return cleaned_data
        except Exception as e:
            print("An error occurred:", e)
            return None

    def display_data(self):
        data = self.get_rig_count_data()
        self.view.display_data(data)