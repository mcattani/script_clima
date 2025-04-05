#! python3
# info_clima.py (v2)
# Script que utiliza la API de https://www.weatherapi.com/ para descargar la información meteorológica.
# Toda la información en: https://thenerdyapprentice.blogspot.com/

# Importamos las librerías
import urllib.request
import urllib.parse
import json

class Clima:
    def __init__(self, ciudad: str):
        self.ciudad = ciudad
        self.ciudad_url = urllib.parse.quote(ciudad) # Convertimos la variable para que sea compatible con la URL (reemplaza espacios)
        self.API_KEY = "435082c056b34774af2145854253003" # Insertar tu propia API key
        self.URL = f"https://api.weatherapi.com/v1/current.json?key={self.API_KEY}&q={self.ciudad_url}&aqi=no&lang=es" # URL de la API 
        self.datos_obtenidos = None # Variable para almacenar la información obtenida
    
    def obtener_datos(self) -> None:
        """
        Obtiene la información climática de la ciudad desde la API de
        weatherapi.com. La información se almacena en la variable
        self.datos_obtenidos en formato de diccionario. Si no se puede
        obtener la información, muestra un mensaje de error.
        """
        try:
            with urllib.request.urlopen(self.URL) as response: # Descargamos la información
                html = response.read()
                self.datos_obtenidos = json.loads(html) # Convertimos la información a un diccionario
        except urllib.error.HTTPError as e:
            print(f"Error al conectarse con el sitio: {e}")
        except urllib.error.URLError as e:
            print(f"Error de conexión: {e}")

    def mostrar_datos(self) -> None:
        """
        Muestra la información del clima de la ciudad, incluyendo su nombre,
        la fecha de la última actualización, la condición climática,
        la temperatura en grados Celsius y la humedad en porcentaje.
        Si no se pudo obtener la información, muestra un mensaje de error.
        """
        if self.datos_obtenidos:
            print(f"Información del clima para: {self.datos_obtenidos['location']['name']}")
            print(f"Última actualización: {self.datos_obtenidos['current']['last_updated']}")
            print(f"Condición: {self.datos_obtenidos['current']['condition']['text']}")
            print(f"Temperatura: {self.datos_obtenidos['current']['temp_c']}°C / Humedad: {self.datos_obtenidos['current']['humidity']}%")
            print(f"Sensación térmica: {self.datos_obtenidos['current']['feelslike_c']}°C")
        else:
            print("No se pudo obtener la información del clima.")

if __name__ == "__main__":
    ciudad = input("Ingrese una ciudad (deje vacío para Buenos Aires): ").strip() 
    if ciudad == "": # Si no se ingresa ninguna ciudad en el input por defecto se usa Buenos Aires
        ciudad = "Buenos Aires"
    clima = Clima(ciudad) # Creamos un objeto de la clase Clima
    clima.obtener_datos() 
    clima.mostrar_datos() 









