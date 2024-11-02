import requests

class HttpRequests:
    @staticmethod
    def get(url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response
        except requests.exceptions.HTTPError as e:
            print("An HTTP error occurred:", e)
            return None
        except requests.exceptions.ConnectionError as e:
            print("A Connection error occurred:", e)
            return None
        except requests.exceptions.Timeout as e:
            print("The request timed out:", e)
            return None
        except requests.exceptions.RequestException as e:
            print("An error occurred:", e)
            return None