import datetime as dt
import src.auxiliares.generador_palabras as genp
import src.auxiliares.funciones_generales as funcs

def main():
    """ Declara manualmente los valores de los distintos 
    diccionarios que establecen qué fichas usar
    en cada dia y rango horario, y dependiendo si se juega 
    con palabras o imagenes, devuelve un diccionario con:
    Para palabras: 'palabra', 'archivo', 'tematica', 'fondo' y 'funcion'. 
    Para imagenes: 'tematica'.  """
    #Constantes
    dias_semana = ['lunes', 'martes', 'miercoles', 'jueves', 'viernes', 'sabado', 'domingo']
    mañana, tarde =  [(0, 12), (13, 23)]

    #Variables
    tipo_fichas = funcs.get_info_usuario_actual()['Configuración']['Fichas']
    hora = dt.datetime.now().hour
    hoy =  dias_semana[dt.datetime.today().weekday()]
    rango = mañana if hora in mañana else tarde
    grupo_p = {}
    grupo_i = {}
    
    #Información para jugar con Imagenes
    grupo_i['lunes'] =      {mañana :   {'tematica': 'Animales'       },
                            tarde :     {'tematica': 'Harry Potter'   }}
    grupo_i['martes'] =     {mañana :   {'tematica': 'Emojis'         },
                            tarde :     {'tematica': 'Lenguajes'      }}
    grupo_i['miercoles'] =  {mañana :   {'tematica': 'Eco Friendly'   },
                            tarde :     {'tematica': 'Navidad'        }}
    grupo_i['jueves'] =     {mañana :   {'tematica': 'San Patricio'   },
                            tarde :     {'tematica': 'Verano'         }}
    grupo_i['viernes'] =    {mañana :   {'tematica': 'Media'          },
                            tarde :     {'tematica': 'Banderas'       }}
    grupo_i['sabado'] =     {mañana :   {'tematica': 'Memes'          },
                            tarde :     {'tematica': 'Fantasia'       }}
    grupo_i['domingo'] =    {mañana :   {'tematica': 'Educación'      },
                            tarde :     {'tematica': 'Frutas'         }}
    
    #Información para jugar con Palabras
    grupo_p['lunes'] = {mañana :    {'palabra'  : 'nombre' ,
                                     'archivo'  : 'parroquias',
                                     'tematica' : 'Parroquias en CABA',
                                     'fondo'    : 'Azul',
                                     'funcion'  : genp.crear_archivo_parroquias },
                        tarde :     {'palabra'  : 'Name',
                                     'archivo'  : 'pokemon',
                                     'tematica' : 'Pokemon tipo fuego',
                                     'fondo'    : 'Violeta',
                                     'funcion'  : genp.crear_archivo_pokemon }}
    grupo_p['martes'] = {mañana :   {'palabra'  : 'title',
                                     'archivo'  : 'android_games_2',
                                     'tematica' : 'Juegos de acción en Playstore',
                                     'fondo'    : 'Rosa',
                                     'funcion'  : genp.crear_archivo_juegos_2 },
                        tarde :     {'palabra'  : 'nombre',
                                     'archivo'  : 'productoras_eventos',
                                     'tematica' : 'Productores de eventos en CABA',
                                     'fondo'    : 'Rojo',
                                     'funcion'  : genp.crear_archivo_productoras_eventos }}
    grupo_p['miercoles'] = {mañana :{'palabra'  : 'NOMBRE',
                                     'archivo'  : 'fuentes',
                                     'tematica' : 'Fuentes en CABA',
                                     'fondo'    : 'Amarillo',
                                     'funcion'  : genp.crear_archivo_fuentes },
                        tarde :     {'palabra'  : 'Country Code',
                                     'archivo'  : 'pobreza_mundial',
                                     'tematica' : 'Paises más pobres en 2011',
                                     'fondo'    : 'Rojo',
                                     'funcion'  : genp.crear_archivo_pobreza_mundial }}
    grupo_p['jueves'] = {mañana :   {'palabra'  : 'category',
                                     'archivo'  : 'ks_projects',
                                     'tematica' : 'Proyectos de KickStarter',
                                     'fondo'    : 'Rosa',
                                     'funcion'  : genp.crear_archivo_ks_projects },
                        tarde :     {'palabra'  : 'champion_name',
                                     'archivo'  : 'LOL_champions_stats',
                                     'tematica' : 'Champions tipo Slayer del LoL',
                                     'fondo'    : 'Amarillo',
                                     'funcion'  : genp.crear_archivo_LOL }}
    grupo_p['viernes'] = {mañana :  {'palabra'  : 'title',
                                     'archivo'  : 'android_games_1',
                                     'tematica' : 'Juegos de mesa en Playstore',
                                     'fondo'    : 'Blanco',
                                     'funcion'  : genp.crear_archivo_juegos_1 },
                        tarde :     {'palabra'  : 'Entity',
                                     'archivo'  : 'areas_protegidas',
                                     'tematica' : 'Mayores areas protegidas en 2017',
                                     'fondo'    : 'Azul',
                                     'funcion'  : genp.crear_archivo_areas_protegidas }}
    grupo_p['sabado'] = {mañana :   {'palabra'  : 'Player',
                                     'archivo'  : 'NBA_All_Star_Games',
                                     'tematica' : 'Jugadores NBA 2000-2016',
                                     'fondo'    : 'Verde',
                                     'funcion'  : genp.crear_archivo_NBA },
                        tarde :     {'palabra'  : 'AUTORES',
                                     'archivo'  : 'monumentos',
                                     'tematica' : 'Monumentos en CABA',
                                     'fondo'    : 'Violeta',
                                     'funcion'  : genp.crear_archivo_monumentos }}
    grupo_p['domingo'] = {mañana :  {'palabra'  : 'nombre',
                                     'archivo'  : 'locales_bailables',
                                     'tematica' : 'Locales bailables en CABA',
                                     'fondo'    : 'Blanco',
                                     'funcion'  : genp.crear_archivo_locales_bailables },
                        tarde :     {'palabra'  : 'barrio',
                                     'archivo'  : 'campanas_verdes',
                                     'tematica' : 'Campanas verdes en CABA',
                                     'fondo'    : 'Verde',
                                     'funcion'  : genp.crear_archivo_campanas_verdes }}

    if __name__ != '__main__':
        if tipo_fichas == 'Palabras':
            return (grupo_p[hoy][rango])
        else:
            return (grupo_i[hoy][rango])

if __name__ == '__main__':
    main() 
