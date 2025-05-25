import requests

class APIClient:
    def __init__(self):
        self.base_url = "https://www.datos.gov.co/resource/nrst-mwx4.json"

    def obtener_datos(self, limite=100):
        params = {"$limit": limite}
        response = requests.get(self.base_url, params=params)

        if response.status_code == 200:
            print("Datos obtenidos exitosamente")
            return response.json()
        else:
            print(f"Error: Código de estado {response.status_code}")
            return []

# Crear una instancia de la clase y llamar el método
cliente = APIClient()
datos = cliente.obtener_datos(5)

# Mostrar los datos si hay alguno
if datos:
    for item in datos:
        print(item)
else:
    print("No se obtuvieron datos.")
