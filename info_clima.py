#! python3
# info_clima.py 
# Script que descarga la info desde la web del Servicio Meteorológico Nacional (SMN)
# Toda la información en: https://thenerdyapprentice.blogspot.com/

# Importamos las librerías
from urllib import request
import zipfile
from os import remove

URL = "https://ssl.smn.gob.ar/dpd/zipopendata.php?dato=tiepre"

def descargar_y_extraer(url_smn):
    '''Función para descargar el archivo del SMN y descomprimirlo. Toma como argumento la URL del SMN. 
    Retorna el nombre del archivo'''
    copia_local = 'copia_local.zip'
    # Descargamos el archivo .zip
    try:
        request.urlretrieve(URL, copia_local)
    except:
        print(f"Error al descargar el archivo. Chequee su conexión de internet o espere un rato y vuelva a intentarlo.")
        return None
    else:
        # Descomprimimos el archivo y guardamos el nombre del archivo en una variable
        try:
            with zipfile.ZipFile(copia_local, "r") as archivo_zip:
                archivo_zip.extractall()
        except:
            print(f"Error al descomprimir el archivo descargado.")
            return None
        else:
            nombre_archivo = archivo_zip.namelist() # Devuelve una lista con el nombre del archivo dentro del .zip
            nombre_archivo = nombre_archivo[0]
            remove(copia_local) # Borramos el archivo .zip
            print("La información se descargó y descomprimió con éxito.")
            return nombre_archivo

def procesar_datos(archivo):
    '''Función para procesar los datos del archivo con la información de los distintos observatorios.
    Requiere el nombre del archivo como argumento. Devuelve una lista de listas con la información de 
    cada observatorio''' 
    # Abrimos el archivo y leemos su contenido
    with open(archivo, 'r', encoding='latin-1') as archivo_datos:
        datos = archivo_datos.readlines()
    '''Convertimos la información de la variable 'datos' en una 'lista de listas'
    Cada elemento de la lista es un ubicación con los datos correspondientes
    Los datos vienen separados por ";" (ver archivo txt descargado)'''
    lista_info_observatorios = []  
    for lineas in datos:
        lista_info_observatorios.append(lineas.strip().split(";"))
    remove(archivo) # Borramos el archivo descomprimido
    return lista_info_observatorios

def mostrar_informacion(lista, ind):
    '''Función para mostrar la información en consola. Toma como arugmento una "lista de listas" [lista]
    y el índice [ind] de la ubicación a mostrar'''
    #print(lista[ind]) # Así se ve el primer elemento de la lista
    # Resultado del print:
    # ['Azul', '20-Octubre-2024', '16:00', 'Despejado', '15 km', '29.5', 'No se calcula', ' 30', 'Norte  27', '988 /']
    #      0       1     2      3            4             5             6               7        8         9      
    # -->LUGAR, FECHA, HORA, CONDICION, VISISIBILIDAD, TEMPERATURA, SENSACION TERMICA, HUMEDAD, VIENTO, PRESION
    lugar = lista[ind][0]
    fecha = lista[ind][1]
    hora = lista[ind][2]
    condicion = lista[ind][3]
    temperatura = lista[ind][5]
    sensacion_termica = lista[ind][6]
    humedad = lista[ind][7]
    print(f"Información del clima para {lugar}")
    print(f"Fecha: {fecha} / Hora: {hora}hs")
    print(f"Condición: {condicion}")
    print(f"Temperatura: {temperatura}° / Humedad:{humedad}%")     
    # A veces no hay información de la sensación térmica. Si hay la mostramos      
    if sensacion_termica != "No se calcula":
        print(f"Sensación térmica: {sensacion_termica}°")

def crear_lugares(lista_info_observatorios):
    '''Función que crea un archivo 'lugares.txt' con los nombres de las ubicaciones disponibles
    en el archivo del observatorio. Toma como parámetro 'lista_info_observatorios' '''
    try:
        with open("lugares.txt", 'w') as archivo_ubicaciones:
            for nombre in lista_info_observatorios:
                archivo_ubicaciones.write(nombre[0])
                archivo_ubicaciones.write("\n")
    except Exception as e:
        print(f"Error al crear el archivo 'lugares.txt'. Descripción {e}")

def chequear_existencia(lista_info_observatorios, lugar):
    '''Función para chequear que exista la ubicación ingresada en la lista. Toma como argumento 
    la lista procesada de datos con la información de los observatorios y el lugar a buscar. 
    Retorna el índice si encuentra la ubicación o 'None' si no'''
    for ind, nombre in enumerate(lista_info_observatorios):
        if lugar == nombre[0]:
            return ind

# Lógica principal
archivo_info_observatorios = descargar_y_extraer(URL)

if archivo_info_observatorios != None: # Si no devuelve 'None' el archivo se descargó con éxito
    #Solicitamos la ubicación a buscar, si no se introduce nada por defecto asignamos 'Buenos Aires'
    ubicacion_a_consultar = input("Ingrese su ubicación o presione 'enter' para ubicacion por defecto: 'Buenos Aires':\n> ").title()    
    if ubicacion_a_consultar == "": # Se busca por defecto Buenos Aires
        ubicacion_a_consultar = "Buenos Aires"
    lista_datos = procesar_datos(archivo_info_observatorios)
    ind = chequear_existencia(lista_datos, ubicacion_a_consultar)
    if ind == None: # Si no se encuentra la ubicación
        print(f"No se encuentra la ubicación <{ubicacion_a_consultar}>, chequee en el archivo 'lugares.txt' las opciones posibles.")
        crear_lugares(lista_datos) # Creamos el archivo lugares para el usuario
    else:
        mostrar_informacion(lista_datos,ind)











