import csv
import os.path
import os
import json
    
dt = "datasets"
rama_json = 'data' + os.sep + dt
path_datasets = os.path.join(os.getcwd(), dt)
path_json = os.path.join(os.getcwd(), rama_json)

def cargar_csv(nombre_arch):
    """ Carga un archivo CSV a ram 
    y lo devuelve como un diccionario """
    csv_arc = nombre_arch + '.csv'
    diccionario = []
    #Si existe la carpeta de datasets en crudo
    if os.path.exists(os.path.join(os.getcwd(), dt)):
        try:
            with open(os.path.join(path_datasets, csv_arc),
                      "r", encoding="utf-8") as arc:
                for i in csv.DictReader(arc):
                    diccionario.append(dict(i))
        #Si no encuentra el dataset
        except (FileNotFoundError):
            print('El archivo dataset (' + csv_arc + ') '
                + 'debe estar en "' + path_datasets
                + '", dentro del directorio principal')
        #Si pasa algo que no estemos contemplando
        except:
            print('Pasó algo. Fijate que los archivos estén bien, '
                  + 'haceles un tecito y no les cambies el nombre')
    #Si no encuentra la carpeta de datasets en crudo
    else: 
        print('Se necesita una carpeta "' + dt
                + '", dentro del directorio principal')
        exit()
    return diccionario

def primeros_14(entrada, casillero='username'):
    """ Recibe un diccionario y devuelve otro con solo los primeros
    14 elementos (cantidad suficiente para nuestro juego) """
    palabras = []
    unicos = set()
    while len(entrada) > 0 and len(palabras) < 14:
        siguiente = entrada.pop(0)
        if ((siguiente[casillero] == '') or
            (siguiente[casillero] == ' ') or
            (siguiente[casillero] in unicos)):
            continue
        else:
            palabras.append(siguiente)
            unicos.add(siguiente[casillero])
    return palabras

def guardar_json(nombre_arch, palabras):
    """ Recibe un diccionario 
    y lo baja a disco en un JSON """
    json_arc = nombre_arch + '.json'
    if os.path.exists(os.path.join(os.getcwd(), path_json)):
        with open(os.path.join(path_json, json_arc), 'w') as j:
            json.dump(palabras, j, indent = 4, ensure_ascii = False)
        print('Archivo JSON creado con éxito.')
    else:
        print('Se necesita una carpeta "' + rama_json
                + '", dentro del directorio principal')
        exit()


#funciones para crear los distintos json con la informacion que se obtiene de los datasets

                                                #1
def crear_archivo_campanas_verdes():
    """ Abre un CSV, procesa la información con los 
    criterios establecidos y vuelca el resultado en un JSON
    con el mismo nombre. Contenido: Listado de las campanas 
    verdes para dejar los materiales reciclables
    de la ciudad de Buenos Aires. """
    #https://data.buenosaires.gob.ar/dataset/campanas-verdes
    #Se llama a abrir el archivo
    nombre = "campanas_verdes"
    diccionario = cargar_csv(nombre)
    palabras = []
    #Se procesa el CSV
    depurado = list(sorted(map(lambda y: y, 
                               filter(lambda x: '1' in x['direccion'] 
                                      and 'Metal' in x['materiales'],
                                      diccionario)
                               ), key=lambda z: z['comuna'], reverse=True))
    palabras = primeros_14(depurado, 'barrio')
    #Se guarda en un JSON
    guardar_json(nombre, palabras)

                                                #2
def mapear(linea, clave):
    nueva_clave = clave.strip(chr(65279)).strip("\"")
    linea[nueva_clave] = linea.pop(clave)
    if nueva_clave == 'Number':
        linea[nueva_clave] = linea[nueva_clave].strip(chr(160))
    return linea

def crear_archivo_pobreza_mundial():
    """ Abre un CSV, procesa la información con los criterios 
    establecidos y vuelca el resultado en un JSON
    con el mismo nombre. Contenido: Tasa de incidencia de la pobreza, 
    sobre la base de $1,90 por día
    (2011 PPA) (% de la población) """
    #https://datos.bancomundial.org/indicador/SI.POV.GAPS
    
    #Se llama a abrir el archivo
    nombre = "pobreza_mundial"
    diccionario = cargar_csv(nombre)
    clave = list(diccionario[0].keys())[0]
    palabras = []
    #Se procesa el CSV
    depurado = list(sorted(map(lambda y: y, filter(lambda x: 'mediano bajo' 
                                                   in x['Income_Group'], 
                                                   diccionario)), 
                           key=lambda z: z['Country Code']))
    depurado = list(map(lambda x: mapear(x, clave), depurado))
    palabras = primeros_14(depurado, 'Country Code')
    #Se guarda en un JSON
    guardar_json(nombre, palabras)    

                                                #3
def crear_archivo_areas_protegidas():
    """ Abre un CSV, procesa la información con los criterios 
    establecidos y vuelca el resultado en un JSON
    con el mismo nombre. Contenido: Indice de terreno por país
    destinado a areas terrenales protegidas """
    #https://ourworldindata.org/protected-areas-and-conservation

    #Se llama a abrir el archivo
    nombre = "areas_protegidas"
    diccionario = cargar_csv(nombre)
    palabras = []
    #Se procesa el CSV
    depurado = list(sorted(map(lambda y: y, filter(lambda x: x['Year'] == '2017', 
                                                   diccionario)), 
                           key=lambda z: z['Terrestrial protected areas'],
                           reverse=True))
    palabras = primeros_14(depurado, 'Entity')
    #Se guarda en un JSON
    guardar_json(nombre, palabras)

                                                #4
def crear_archivo_fuentes():
    """ Abre un CSV, procesa la información con los criterios 
    establecidos y vuelca el resultado en un JSON
    con el mismo nombre. Contenido: Detalle de las fuentes 
    ubicadas en espacios verdes de la ciudad. """
    #https://data.buenosaires.gob.ar/dataset/fuentes
    
    #Se llama a abrir el archivo
    nombre = "fuentes"
    diccionario = cargar_csv(nombre)
    palabras = []
    #Se procesa el CSV
    depurado = list(sorted(map(lambda y: y, filter(lambda x: x['COMUNA'] == '1', 
                                                   diccionario)), 
                           key=lambda z: z['DIRECCION NORMALIZADA']))
    palabras = primeros_14(depurado, 'NOMBRE')
    #Se guarda en un JSON
    guardar_json(nombre, palabras)

                                                #5
def crear_archivo_monumentos():
    """ Abre un CSV, procesa la información con los criterios 
    establecidos y vuelca el resultado en un JSON
    con el mismo nombre. Contenido: Monumentos de la 
    Ciudad de Buenos Aires en plazas o paseos. """
    #https://data.buenosaires.gob.ar/dataset/monumentos

    #Se llama a abrir el archivo
    nombre = "monumentos"
    diccionario = cargar_csv(nombre)
    palabras = []
    #Se procesa el CSV
    depurado = list(sorted(map(lambda y: y, filter(lambda x: 'GRANITO' 
                                                   in x['MATERIAL'], 
                                                   diccionario)), 
                           key=lambda z: z['AUTORES']))
    palabras = primeros_14(depurado, 'AUTORES')
    #Se guarda en un JSON
    guardar_json(nombre, palabras)

                                                #6
def crear_archivo_productoras_eventos():
    """ Abre un CSV, procesa la información con los criterios 
    establecidos y vuelca el resultado en un JSON
    con el mismo nombre. Contenido: Registro Público de 
    Productoras de Eventos Masivos en la Ciudad de Buenos Aires """
    #https://data.buenosaires.gob.ar/dataset/productoras-eventos-masivos/archivo/juqdkmgo-1681-resource

    #Se llama a abrir el archivo
    nombre = "productoras_eventos"
    diccionario = cargar_csv(nombre)
    palabras = []
    #Se procesa el CSV
    depurado = list(sorted(map(lambda y: y, filter(lambda x: x['comuna'] == 'Comuna 1', 
                                                   diccionario)), 
                           key=lambda z: z['nombre']))
    palabras = primeros_14(depurado, 'nombre')
    #Se guarda en un JSON
    guardar_json(nombre, palabras)

                                                #7
def crear_archivo_parroquias():
    """ Abre un CSV, procesa la información con los criterios 
    establecidos y vuelca el resultado en un JSON
    con el mismo nombre. Contenido: Listado y ubicación 
    geográfica de las parroquias situadas
    en la Ciudad de Buenos Aires """
    #https://data.buenosaires.gob.ar/dataset/parroquias

    #Se llama a abrir el archivo
    nombre = "parroquias"
    diccionario = cargar_csv(nombre)
    palabras = []
    #Se procesa el CSV
    depurado = list(sorted(map(lambda y: y, filter(lambda x: x['comuna'] >= 'Comuna 5',
                                                   diccionario)), 
                           key=lambda z: z['altura']))
    palabras = primeros_14(depurado, 'nombre')
    #Se guarda en un JSON
    guardar_json(nombre, palabras)

                                                #8
def crear_archivo_ks_projects():
    """ Abre un CSV, procesa la información con los criterios 
    establecidos y vuelca el resultado en un JSON
    con el mismo nombre. Contenido: Proyectos de 
    Kick Starter año 2018 """
    #https://www.kaggle.com/kemical/kickstarter-projects?select=ks-projects-201801.csv

    #Se llama a abrir el archivo
    nombre = "ks_projects"
    diccionario = cargar_csv(nombre)
    palabras = []
    #Se procesa el CSV
    depurado = list(sorted(map(lambda y: y, filter(lambda x: float(x['pledged']) > 100.0, 
                                                   diccionario)), 
                           key=lambda z: z['pledged']))
    palabras = primeros_14(depurado, 'category')
    #Se guarda en un JSON
    guardar_json(nombre, palabras)

                                                #9
def crear_archivo_locales_bailables():
    """ Abre un CSV, procesa la información con los criterios 
    establecidos y vuelca el resultado en un JSON
    con el mismo nombre. Contenido: Locales inscriptos y 
    re-inscriptos de la Ciudad de Buenos Aires,
    incluyéndose la capacidad de los mismos """
    #https://data.buenosaires.gob.ar/dataset/locales-bailables/archivo/juqdkmgo-1351-resource
    
    #Se llama a abrir el archivo
    nombre = "locales_bailables"
    diccionario = cargar_csv(nombre)
    palabras = []
    #Se procesa el CSV
    depurado = list(sorted(map(lambda y: y, filter(lambda x: 'RENOVADO' 
                                                   in x['estado'], 
                                                   diccionario)), 
                           key=lambda z: z['barrio']))
    palabras = primeros_14(depurado, 'nombre')
    #Se guarda en un JSON
    guardar_json(nombre, palabras)

                                                #10
def crear_archivo_juegos_2():
    """ Abre un CSV, procesa la información con los criterios 
    establecidos y vuelca el resultado en un JSON
    con el mismo nombre. Contenido: Mejores juegos de Playstore"""
    #https://www.kaggle.com/dhruvildave/top-play-store-games
    nombre = "android_games_2"
    diccionario = cargar_csv(nombre)
    #Se procesa el CSV
    depurado = list(filter(lambda game: 'ACTION' 
                           in game['category'] 
                           and game['average rating'] > str(4.10), diccionario))
    palabras = primeros_14(depurado, 'title')
    #Se guarda en un JSON
    guardar_json(nombre, palabras)

                                                #11
def crear_archivo_pokemon():
    """ Abre un CSV, procesa la información con los criterios 
    establecidos y vuelca el resultado en un JSON
    con el mismo nombre. Contenido: Lista de Pokemon, sus stats,
    tipos y otra información """
    #https://www.kaggle.com/brendan45774/pokmon-index-database
    
    #Se llama a abrir el archivo
    nombre = "pokemon"
    diccionario = cargar_csv(nombre)
    palabras = []
    clave = list(diccionario[0].keys())[0]
    #Se procesa el CSV
    depurado = list(sorted(map(lambda y: y, filter(lambda x: x['Type'] == 'FIRE', 
                                                   diccionario)),
                           key=lambda z: z['Total']))
    depurado = list(map(lambda x: mapear(x, clave), depurado))
    palabras = primeros_14(depurado, 'Name')
    #Se guarda en un JSON
    guardar_json(nombre, palabras)

                                                #12
def crear_archivo_LOL():
    """ Abre un CSV, procesa la información con los criterios
    establecidos y vuelca el resultado en un JSON
    con el mismo nombre. Contenido: Lista de campeones del 
    League of Legends, sus stats y otra información """
    #https://www.kaggle.com/barthetur/league-of-legends-champions-items-stats
    
    #Se llama a abrir el archivo
    nombre = "LOL_champions_stats"
    diccionario = cargar_csv(nombre)
    clave = list(diccionario[0].keys())[0]
    palabras = []
    #Se procesa el CSV
    depurado = list(sorted(map(lambda y: y, filter(lambda x: x['class'] == 'Slayer', 
                                                   diccionario)), 
                           key=lambda z: z[clave]))
    depurado = list(map(lambda x: mapear(x, clave), depurado))
    palabras = primeros_14(depurado, 'champion_name')
    #Se guarda en un JSON
    guardar_json(nombre, palabras)

                                                #13
def crear_archivo_juegos_1():
    """ Abre un CSV, procesa la información con los criterios 
    establecidos y vuelca el resultado en un JSON
    con el mismo nombre. Contenido: Mejores juegos de Playstore"""
    #https://www.kaggle.com/dhruvildave/top-play-store-games

    #Se llama a abrir el archivo
    nombre = "android_games_1"
    diccionario = cargar_csv(nombre)
    palabras = []
    #Se procesa el CSV
    depurado = list(sorted(map(lambda y: y, filter(lambda x: 'BOARD' 
                                                   in x['category'], 
                                                   diccionario)),
                           key=lambda z: z['total ratings']))
    palabras = primeros_14(depurado, 'title')
    #Se guarda en un JSON
    guardar_json(nombre, palabras)

                                                #14
def crear_archivo_NBA():
    """ Abre un CSV, procesa la información con los criterios 
    establecidos y vuelca el resultado en un JSON
    con el mismo nombre. Contenido: Más de 400 jugadores 
    de la NBA entre el 2000 y el 2016 """
    #https://www.kaggle.com/rishidamarla/nba-allstars-20002016

    #Se llama a abrir el archivo
    nombre = "NBA_All_Star_Games"
    diccionario = cargar_csv(nombre)
    
    #Se procesa el CSV
    depurado = list(sorted(map(lambda y: y, filter(lambda x: x['WT'] > str(200), 
                                                   diccionario)),
                           key=lambda z: z['WT']))
    palabras = primeros_14(depurado, 'Player')

    #Se guarda en un JSON
    guardar_json(nombre, palabras)
    

def main(funcion = crear_archivo_areas_protegidas):
    """ Inicializa el programa y llama al metodo recibido 
    por parámetro (que corresponde al dia y rango
    horario en que se ejecuta), del cual se sacarán las 
    palabras a mostrar en las fichas del MemPy."""
    funcion()
    

if __name__ == '__main__':
    main(crear_archivo_NBA)