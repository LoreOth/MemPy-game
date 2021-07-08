from tkinter.font import BOLD
import PySimpleGUI as sg
import src.auxiliares.register as reg
import src.auxiliares.funciones_generales as funcs
import src.auxiliares.registro_eventos as reg_eventos
import src.ventanas.pantalla_juego as juego
import src.ventanas.pantalla_puntajes as puntajes
import src.ventanas.pantalla_estadisticas as stats
import src.ventanas.pantalla_sesion as sesion
import src.ventanas.menu_configuracion as configs
import src.auxiliares.criterios as crits
import src.Icono as icono
import os


ICONO = icono.devolver_icono()
imagen_cabecera = os.getcwd() + os.sep + 'img' + os.sep + 'Mempy principal.png'

reg_eventos.existe_registro_eventos()


def load_layout(nick):
    """ Declara el layout de la ventana de inicio,
    con los botones que hacen que el jugador llegue
    a las distintas partes del juego, además de
    widgets que ofrecen información como 
    cual será la temática de la partida que se juegue,
    o quién es el usuario conectado en el momento """

    tematica = crits.main()['tematica']
    layout = [[sg.Text('¡Bienvenide a', font=('_', 30), justification='center')],
             [sg.Image(imagen_cabecera)],
             [sg.Text('La temática tu juego será:', font=('Verdana',10), justification='center')],
             [sg.Text(tematica, font=('Verdana',12), justification='center', 
                      background_color='#123456', text_color='#5ae5c3', border_width=4)],
             [sg.Text('', font=('',16))],
             [sg.Button('Sala de Juego', font=('Trebuchet MS',14), size=(16,1), key='jugar')],
             [sg.Button('Configuración', font=('Trebuchet MS',14),  size=(16,1), key='configs')],
             [sg.Button('Puntajes', font=('Trebuchet MS',14),  size=(16,1), key='puntajes')],
             [sg.Button('Estadisticas', font=('Trebuchet MS',14),  size=(16,1), key='stats')],
             [sg.Text()],
             [sg.Text('Usuario actual:', font=('Verdana',10, BOLD))],
             [sg.Text(nick, font=('Verdana',10, BOLD), background_color='#123456',
                      text_color='#5ae5c3', border_width=4)],
             [sg.Button('Cerrar Sesión', key='cerrar', font=('Verdana',12))],
             [sg.Button('Salir', size=(5,1), key='salir', font=('Verdana',10))]]
    return sg.Window('MemPyG28', 
                     layout, icon = ICONO, margins=(80,25),
                     element_justification='c').finalize()


def set_hover_event(window, *args):
    """ Se recibe la ventana que contiene los elementos a 
    los cuales se les va a asignar el hover y la clave 
    de estos mismos en una tupla"""

    for clave in args:
        window[clave].bind("<Enter>", "|HOVERED|")
        window[clave].bind("<Leave>", "|UNHOVERED|")


def main(inicio=False):
    """ Declara la ventana, se carga el layout y se 
    ejecuta el menu inicial de la aplicacion """
    nick = funcs.get_nombre_usuario_actual()
    sg.theme(funcs.get_info_usuario_actual()['Configuración']['Tema'])

    if (inicio):
        config = funcs.get_info_usuario_actual()['Configuración']
        config['Nivel_actual'] = config['Nivel_inicial']
        funcs.actualizar_config(config)
        
    window = load_layout(nick)
    set_hover_event(window, 'puntajes', 'stats', 
                    'jugar', 'configs', 'salir', 'cerrar')
    color = getattr(window, 'ButtonColor')

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED or event == 'salir':
            break

        #controlador de hover para cada boton
        elif event.endswith("|HOVERED|"):
            color = getattr(window[event[:-9]], 'ButtonColor')
            color_texto = color[0]
            color_fondo = int(color[1].replace('#', ''), 16)
            window[event[:-9]].update(button_color = 
                                      (color_texto, color_fondo - 12000))
        elif event.endswith("|UNHOVERED|"):
            window[event[:-11]].update(button_color = color)

        elif event == 'cerrar':
            window.close()
            sesion.main()
        elif event == 'puntajes':
            window.close()
            puntajes.main()
        elif event == 'stats':
            window.close()
            stats.main()
        elif event == 'jugar':
            window.close()
            juego.main()
        elif event == 'configs':
            window.close()
            configs.main()

    window.close()


if __name__ == '__main__':
    main()