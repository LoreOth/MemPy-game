import json
import os

ruta_json_usuarios = (os.getcwd() + os.sep 
                      + 'data' + os.sep + 'usuarios' + os.sep)


def actualizar_config(config):
    """ Recibe una configuración y,
    reutilizando otro método de lectura y escritura
    de usuarios en la base de datos, lo llama,
    pasandole el usuario actual, con la configuración
    recibida reemplazando la anterior """
    info = get_info_usuario_actual()
    info['Configuración'] = config
    actualizar_usuario(info)

def actualizar_usuario(info):
    """ Se recibe como parámetro información JSON de usuario y se actualizan 
    los datos del usuario en partida, tanto en el archivo con todos los usuarios
    como en el del usuario actual """
    usuario = get_nombre_usuario_actual()
    ruta_json_usuarios = os.getcwd() + os.sep + 'data' + os.sep + 'usuarios' + os.sep
    
    #modificacion en el archivo general
    with open(f"{ruta_json_usuarios}usuarios.json", "r", encoding = "utf-8") as usuarios:
        data = json.load(usuarios)
    data[f'{usuario}'] = info
    with open(f"{ruta_json_usuarios}usuarios.json", "w", encoding = "utf-8") as usuarios:
        json.dump(data, usuarios, indent = 4, ensure_ascii = False)

    #modificacion en el archivo de usuario actual
    with open(f"{ruta_json_usuarios}usuario_actual.json", "r", encoding = "utf-8") as usuario_actual:
        data = json.load(usuario_actual)   
    data[f'{usuario}'] = info
    with open(f"{ruta_json_usuarios}usuario_actual.json", "w", encoding = "utf-8") as usuario_actual:
        json.dump(data, usuario_actual, indent = 4, ensure_ascii = False)

def get_info_usuario_actual():
    """ Se cargan y retornan los datos del usuario 
    que actualmente está conectado """

    with open(f"{ruta_json_usuarios}usuario_actual.json",
              "r", encoding = "utf-8") as usuario_actual:
        user = json.load(usuario_actual)
    
    return list(user.items())[0][1]

def get_nombre_usuario_actual():
    """ Por medio de una lectura al JSON del
    usuario actualmente conectado, se recupera
    y devuelve su nick """
    with open(f"{ruta_json_usuarios}usuario_actual.json",
              "r", encoding = "utf-8") as usuario_actual:
        user = json.load(usuario_actual)

    return list(user.items())[0][0]
    
def pausar_juego(partida):
    """ Se recibe una partida, a la cual se le indica que su propiedad
    de pausado pase a ser verdadera, y se invoca un método de la misma 
    que frena el conteo de tiempo util """
    partida.cambiar_pausa()
    partida.pausar_tiempo()
    
def despausar_juego(partida):
    """ Se recibe una partida, a la cual se le indica que su propiedad
    de pausado pase a ser falsa, y se invoca un método de la misma 
    que reanuda el conteo de tiempo util """
    partida.cambiar_pausa()
    partida.reanudar_tiempo()
