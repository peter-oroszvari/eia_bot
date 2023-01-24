class View:
    def __init__(self):
        pass
    
    def format_ng_storage_data(self, data):

        # Format the data as a message
        release_date = data['release_date']
        message = f"Natural Gas Storage Report for {release_date}\n\n"
        for series in data['series']:
            name = series['name']
            net_change = series['calculated']['net_change']
            message += f"{name}: {net_change}\n"
        
        return message