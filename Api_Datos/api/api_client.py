import requests

class APIClient:
    def __init__(self):
        self.base_url = "https://www.datos.gov.co/resource/nrst-mwx4.json"

    def obtener_datos(self):
        response = requests.get(self.base_url)
        if response.status_code == 200:
            datos = response.json()
            datos_filtrados = [d for d in datos if int(d.get('a_o', 0)) >= 2022]
            return datos_filtrados
        else:
            print(f"Error: {response.status_code}")
            return []