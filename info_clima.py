#! python3
# info_clima.py 
# Script que descarga la info desde la web del Servicio Meteorológico Nacional (SMN)
# Toda la información en: https://thenerdyapprentice.blogspot.com/

# Importamos las librerías
from urllib import request
import zipfile
import tempfile
import os

# Código de colores código ANSI
VERDE = "\033[32m"
ROJO = "\033[31m" 
RESET = "\033[0m" # Devuelve el color por defecto a la terminal

URL = "https://ssl.smn.gob.ar/dpd/zipopendata.php?dato=tiepre" 

# Creamos un archivo temporal para almacenar el archivo a descargar del SMN
temp_zip_file = tempfile.NamedTemporaryFile(suffix=".zip", delete=False)

# Descargamos el archivo .zip
try:
    request.urlretrieve(URL, temp_zip_file.name)
except Exception as error:
    print(f"""{ROJO}Error al descargar el archivo: {error} 
Chequee su conexión a internet y/o que el archivo esté disponible en la web.{RESET}""")
    exit()

print(f"{VERDE}Información descargada con éxito.{RESET}")

# Creamos una carpeta temporal para extraer el archivo
temp_path = tempfile.TemporaryDirectory()

# Descomprimimos el archivo y guardamos el nombre del archivo en una variable
archivo_zip = zipfile.ZipFile(temp_zip_file.name)
archivo_zip.extractall(path=temp_path.name) 
archivo_zip.close() # Cerramos el archivo 

nombre_archivo = archivo_zip.namelist() # Devuelve una cadena con el nombre del archivo dentro del .zip

# Creamos el path y convertimos la cadena en un string así tenemos el nombre del archivo
nombre_archivo = os.path.join(temp_path.name,"".join(nombre_archivo)) 

#Abrimos el archivo y leemos su contenido
archivo_datos = open(nombre_archivo, 'r', encoding='latin-1')
datos = archivo_datos.readlines()
archivo_datos.close() # Cerramos el archivo

'''Convertimos la información de la variable 'datos' en una 'lista de listas'
Cada elemento de la lista es un ubicación con los datos correspondientes
Los datos vienen separados por ";" (ver archivo txt descargado)'''

ind=0
lista_info = []
while ind < len(datos):
    lista_info.append(datos[ind].strip().split(";"))
    ind += 1

# El resultado es una 'lista de listas' almacenadas en la variable 'lista'
#print(lista_info[0]) # Así se ve el primer elemento de la lista
# Resultado del print:
# ['Azul', '20-Octubre-2024', '16:00', 'Despejado', '15 km', '29.5', 'No se calcula', ' 30', 'Norte  27', '988 /']
#      0       1     2      3            4             5             6               7        8         9      
# -->LUGAR, FECHA, HORA, CONDICION, VISISIBILIDAD, TEMPERATURA, SENSACION TERMICA, HUMEDAD, VIENTO, PRESION

# Creamos un archivo con las ubicaciones para ver los lugares diponibles
ind=0
archivo_lugares = open("lugares.txt", "w")
while ind < len(lista_info):
    archivo_lugares.write(lista_info[ind][0])
    archivo_lugares.write("\n")
    ind += 1
archivo_lugares.close()

def chequear_existencia(ubicacion):
    '''Función para chequear que exista la ubicación ingresada en la lista. Si encuentra -> retorna el índice o None si no existe'''
    for ind, elemento in enumerate(lista_info):
        lugar_a_buscar = elemento[0]
        if lugar_a_buscar == ubicacion:
            return ind
    return None

# Solicitamos la ubicación a buscar, si no se introduce nada por defecto asignamos 'Buenos Aires'
ubicacion_a_consultar = input("Ingrese su ubicación o presione 'enter' para ubicacion por defecto: 'Buenos Aires'):\n> ").title()
if ubicacion_a_consultar == "":
    ubicacion_a_consultar="Buenos Aires"

ind = chequear_existencia(ubicacion_a_consultar)
if ind == None:
    # Si no existe la ubicacón
    print(f"{ROJO}Ubicación no encontradada. Consulte el archivo 'lugares.txt'.{RESET}")
else:
    # Existe la ubicación
    # Asignamos los datos a variables 
    lugar = lista_info[ind][0]
    fecha = lista_info[ind][1]
    hora = lista_info[ind][2]
    condicion = lista_info[ind][3]
    temperatura = lista_info[ind][5]
    sensacion_termica = lista_info[ind][6]
    humedad = lista_info[ind][7]
    # Mostramos los datos
    print("Información del clima para:",lugar)
    print(fecha, "/", hora,"hs")
    print(condicion)
    print(f"Temperatura: {temperatura}° / S/T: {sensacion_termica}° / Humedad:{humedad}%")









