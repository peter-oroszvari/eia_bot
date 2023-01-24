from .ng_storage_report_model import NGModel
from .ng_storage_report_view import View

class NGController:
    def __init__(self):
        self.model = NGModel() # import and instantiate the TTFModel class
        self.view = View()
    def get_formatted_data(self):
        try:
            data = self.model.fetch_nagtas_storage_data()
            return self.view.format_ng_storage_data(data)
        except Exception as e:
            print("An error occurred:", e)
            return None

