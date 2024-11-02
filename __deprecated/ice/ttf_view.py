
class View:
    def __init__(self):
        pass
    
    def display_data(self, data):
        message = "Dutch TTF Natural Gas Futures:\n"
        for item in data:
            futures = item['Futures: ']
            last_price = item['Last Price: ']
            message += f"{futures}: {last_price}\n"
        return message