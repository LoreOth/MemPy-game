import src.auxiliares.funciones_generales as funcs
import src.ventanas.menu_inicio as menu
import PySimpleGUI as sg
import src.auxiliares.register as reg
import json
import time
import os


imagen_cabecera = os.getcwd() + os.sep + 'img' + os.sep + 'Mempy sesion.png'
ruta_json = os.getcwd() + os.sep + 'data' + os.sep + 'usuarios' + os.sep
ruta_json_usuarios = ruta_json


def buscar_contrasena(nick):
    """ Se busca la contraseña del usuario ingresado """

    with open(f"{ruta_json_usuarios}usuarios.json", "r", encoding = "utf-8") as usuarios:
        data = json.load(usuarios)

    return data.get(f'{nick}').get('Contraseña')


def cargar_datos_ultimo_usuario():
    """Se cargan los ultimos datos del usuario que se conecto, 
    para saber si queria que se recuerden sus datos """
    nombre_ultimo_usuario = funcs.get_nombre_usuario_actual()
    psw_ultimo_usuario = funcs.get_info_usuario_actual()['Contraseña']
    info_ultimo_usuario = funcs.get_info_usuario_actual()

    return nombre_ultimo_usuario, psw_ultimo_usuario, info_ultimo_usuario


def set_usuario_actual(user, recordar_usuarie):
    with open(f"{ruta_json}usuarios.json", "r", encoding = "utf-8") as usuarios:
        data = json.load(usuarios)

    usuario_actual = {}
    usuario_actual[f'{user}'] = data[f'{user}']
    usuario_actual[f'{user}']['Configuración']['Recordar_usuarie'] = recordar_usuarie

    with open(f"{ruta_json}usuario_actual.json", "w", encoding = "utf-8") as file:
        json.dump(usuario_actual, file, indent = 4, ensure_ascii = False)
        

def validar_usuario(user):
    """ Chequea si el usuario ingresado existe
    por medio de comparasiones de los datos ingresados
    con los de la base de datos """
    with open(f"{ruta_json}usuarios.json", "r", encoding = "utf-8") as usuarios:
        data = json.load(usuarios)
    return data.get(f'{user}') == None


def load_layout(nombre_ultimo_usuario, psw_ultimo_usuario, info_ultimo_usuario):
    """ Declara el layout de la ventana de inicio
    con sus respectivos campos de ingreso de datos,
    más los botones de ingreso, entre otros elementos """
    recordar = info_ultimo_usuario['Configuración']['Recordar_usuarie']

    layout = [[sg.Image(imagen_cabecera)],
             [sg.Text('Login', size=(14,1), font=('_', 20), justification='left')],
             [sg.InputText(nombre_ultimo_usuario if recordar else '', tooltip = 'Ingresá tu usuario',
                          key = 'nick', size=(20,1), font=('Arial', 14))],
             [sg.InputText(psw_ultimo_usuario if recordar else '',tooltip = 'Ingresá tu contraseña',
                          password_char = '*', key = 'password', size=(20,1), font=('Arial', 14))],
             [sg.Button('Ingresar', font=('Arial Black',12), size=(20,1), key='enter', bind_return_key=True)],
             [sg.Checkbox('Recordar usuarie.', default = recordar, key = 'recordar_usuarie')],
             [sg.Text()],
             [sg.Text('Si no tenés usuario, creá uno!')],
             [sg.Button('Crear Usuario', font=('Arial Black',12),  size=(20,1), key='nuevo_usuarie')]
             ]

    return sg.Window('MemPyG28', layout, 
                     grab_anywhere = True, margins=(25,25), 
                     element_justification='c').finalize()


def set_hover_event(window, *args):
    """ Se recibe, en una tupla, la ventana que 
    contiene los elementos a los cuales se les 
    va a asignar el hover y la clave de los mismos """

    for clave in args:
        window[clave].bind("<Enter>", "|HOVERED|")
        window[clave].bind("<Leave>", "|UNHOVERED|")


def main():
    """ Organiza y administra el layout
    para instanciar la ventana y chequear
    el ingreso y egreso de datos a la ventana,
    concediendo o no el acceso al juego """

    sg.theme('DarkBlue')
    nombre_ultimo_usuario, psw_ultimo_usuario, info_ultimo_usuario = cargar_datos_ultimo_usuario()
    window_sesion = load_layout(nombre_ultimo_usuario, psw_ultimo_usuario, info_ultimo_usuario)
    set_hover_event(window_sesion, 'enter', 'nuevo_usuarie')

    while True:
        event, values = window_sesion.read()    
        
        if event == sg.WIN_CLOSED or event == 'Salir':
            break

        #controlador de hover para cada boton
        elif event.endswith("|HOVERED|"):
            color = getattr(window_sesion[event[:-9]], 'ButtonColor')
            color_texto = color[0]
            color_fondo = int(color[1].replace('#', ''), 16)
            window_sesion[event[:-9]].update(button_color = 
                                             (color_texto, color_fondo - 20000))
        elif event.endswith("|UNHOVERED|"):
            window_sesion[event[:-11]].update(button_color = color)

        elif event == 'enter':
            window_sesion['enter'].update(button_color = color)
            nick = values.get('nick')
            if (not validar_usuario(nick)):
                contrasena = buscar_contrasena(nick)
                if contrasena == values.get('password'):
                    sg.PopupQuick('Login correcto!', auto_close=True,
                                  auto_close_duration=0.2)
                    time.sleep(0.25)

                    window_sesion.close()
                    set_usuario_actual(values.get('nick'), values.get('recordar_usuarie'))
                    menu.main(inicio=True)

                    break

                else:
                    sg.PopupQuick('Login incorrecto!')
            else:
                sg.PopupQuick('Login incorrecto!')
  
        elif event == 'nuevo_usuarie':
            window_sesion['nuevo_usuarie'].update(button_color = color)
            reg.upload_nuevo_usuarie()

    window_sesion.close()


if __name__ == '__main__':
    main()