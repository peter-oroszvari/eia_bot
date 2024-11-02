from .ttf_model import TTFModel
from .ttf_view import View

class TTFController:
    def __init__(self):
        self.model = TTFModel() # import and instantiate the TTFModel class
        self.view = View()

    def get_formatted_data(self):
        try:
            data = self.model.fetch_ttf_data()
            return self.view.display_data(data)
        except Exception as e:
            print("An error occurred:", e)
            return None