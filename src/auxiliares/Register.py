import PySimpleGUI as sg
import src.Icono as icono
import json
import os
from pathlib import Path

if __name__ == '__main__':
    os.chdir(Path(os.getcwd()).parent.parent)
ruta_json_usuarios = (os.getcwd() + os.sep 
                      + 'data' + os.sep + 'usuarios' + os.sep)
ICONO = icono.devolver_icono()


def cargar_layout():
    """ Declaación del layout de la ventana 
    para cargar un nuevo usuario a registrar """

    layout = [[sg.Text('Registrese para jugar', 
                       font='_ 20', 
                       justification='center')],
            [sg.Text('Usuario:      '), 
             sg.Input(key='nick', size=(34,1))],
            [sg.Text('Contraseña:'), 
             sg.Input(password_char='*', 
                      key='password', size=(34,1))],
            [sg.Text('Edad:         '), 
             sg.Input(key='age', size=(34,1))],
            [sg.Text('Genero:      '), 
             sg.Input(key='gender', size=(34,1))],
            [sg.Button('Cancelar'), 
             sg.Button('Enviar')]]
    return sg.Window('Registro de nuevo usuario',
                     layout, icon = ICONO, margins=(75,50), 
                     element_justification='c')


def enter_new_user(user, password, age, gender):
    """ Abre el archivo contenedor de datos de usuarios, 
    se posiciono al final e ingresa el nuevo usuario """

    with open(f"{ruta_json_usuarios}usuarios.json",
              "r", encoding = "utf-8") as usuarios:
        data = json.load(usuarios)

        data[f'{user}'] = {
            'Contraseña' : password,
            'Edad' : age,
            'Género' : gender,
            'Configuración' : {
                'Dificultad' : 'Fácil',
                'Nivel_estático' : False,
                'Nivel_inicial' : 1,
                'Nivel_actual' : 1,
                'Fichas' : 'Palabras',
                'Tema' : 'DarkGreen',
                'Mensajes' : {
                    'Victoria' : '¡Felicitaciones, terminaste todos los niveles!',
                    'Puntaje' : '¡Eso fue un nuevo record! :)',
                    'Derrota' : 'Perdiste :( mejor suerte la próxima'
                },
                'Record' : 0,
                'Recordar_usuarie' : False
            }
        }

    with open(f"{ruta_json_usuarios}usuarios.json", 
              "w", encoding = "utf-8") as usuarios:
        json.dump(data, usuarios, indent = 4, ensure_ascii = False)


def existe_usuario(user):
    """ Chequea si el usuario ingresado existe
    en la base de datos de usuarios del juego """

    with open(f"{ruta_json_usuarios}usuarios.json", 
              "r", encoding = "utf-8") as usuarios:
        data = json.load(usuarios)
    return data.get(f'{user}') == None


def validar_usuario(user):
    """ Recibe el usuario como parametro y comprueba 
    que sea correcto. Que tenga entre 4 y
    20 caracteres y que solo contenga determinados
    caracteres especiales"""

    caracteres_especiales = '!¡@#$%._-'

    if len(user) > 3 and len(user) < 21:
        if user.isalnum():
            return True
        else:
            for c in user:
                if not (c.isalnum() or c in caracteres_especiales):
                    sg.PopupQuick('Solo se permiten los siguientes '
                                  + 'caracteres: !¡@#$%._-',
                                  auto_close = False)
                    return False
            return True
    else:
        sg.PopupQuick('El usuario debe tener entre 4 y 20 caracteres.', 
                      auto_close = False)
        return False


def validar_campos(*args):
    """ Esta función recibe todos los campos que el usuario 
    debe ingresar para crear su usuario y
    valida que no sean campos vacíos"""

    for campo in args:
        if campo.strip() == '':
            sg.PopupQuick('Alguno de los campos no se completó correctamente, '
                          + 'asegúrese de no haber dejado espacios vacíos o '
                          + 'caracteres inválidos.', auto_close = False)
            return False
    
    try:
        int(args[1])
    except ValueError:
        sg.PopupQuick('El valor de la edad debe ser numérico.', 
                      auto_close = False)
        return False
    
    return True


def upload_nuevo_usuarie():
    """ Funcion principal para ejecutar la ventana de registro 
    y mandar a cargar el usuario nuevo """

    window = cargar_layout()

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED or event == 'Cancelar':
            break
        
        elif event == 'Enviar':
            if validar_usuario(values.get('nick')):
                if existe_usuario(values.get('nick')):
                    if validar_campos(values.get('password'), values.get('age'), 
                                      values.get('gender')):
                        enter_new_user(values.get('nick'), 
                                       values.get('password'), values.get('age'),
                                       values.get('gender'))
                        sg.PopupQuick(f"Usuario {values.get('nick')} creado!\nEdad:"
                                      + f"{values.get('age')} - Genero: "
                                      + f"{values.get('gender')}", 
                                      auto_close = False)
                        window.close()
                        break
                else:
                    sg.PopupQuick('Este nombre de usuario ya está registrado,'
                                  + 'pruebe ingresando otro.', auto_close = False)

    window.close()