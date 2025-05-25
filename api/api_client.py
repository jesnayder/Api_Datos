import requests

class APIClient:
    def __init__(self):
        self.base_url = "https://www.datos.gov.co/resource/nrst-mwx4.json"

    def obtener_datos(self):
        
        response = requests.get(self.base_url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code}")
            return []