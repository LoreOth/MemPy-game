import PySimpleGUI as sg
from PySimpleGUI.PySimpleGUI import DEFAULT_BUTTON_COLOR
from src.ventanas import menu_inicio as inicio
from src.auxiliares import clases as cla
from src.auxiliares import funciones_generales as funcs
from src.auxiliares import registro_eventos as reg


def evento_partida(tiempo, filas, columnas, coincidencias, nick, 
                   nivel, dificultad, nombre_evento, estado=None):
    """ Se reciben los parametros relevantes para guardar
    un registro con informacion de un evento
    al comenzar una nueva partida """

    cant_palabras = (filas * columnas) / coincidencias
    edad = funcs.get_info_usuario_actual()['Edad']
    genero = funcs.get_info_usuario_actual()['Género']
    
    evento_inicio = reg.Evento()
    evento_inicio.tiempo = tiempo
    evento_inicio.cant_palabras = cant_palabras
    evento_inicio.nick = nick
    evento_inicio.genero = genero
    evento_inicio.edad = edad
    evento_inicio.nivel = nivel
    evento_inicio.dificultad = dificultad    
    if nombre_evento == 'fin_partida':
        evento_inicio.nombre_evento = 'fin_partida'
        evento_inicio.estado = estado
        evento_inicio.partida = reg.numero_partida()
    else:
        evento_inicio.nombre_evento = 'inicio_partida'
        evento_inicio.partida = reg.numero_partida() + 1

    evento_inicio.cargar_evento()


def main(siguiente=False, otros_puntos=0):
    """ Inicializa la ventana de juego. Se llaman a diversos métodos
    para lectura de json de usuario actual, fecha y hora, entre otros,
    y así se recopilan los datos necesarios para instanciar una partida,
    con sus fichas, y cargarlas en una ventana implementada en este módulo,
    donde se desarrolla la jugada en sí """

    (dificultad, nivel, nivel_inicial, nivel_estatico, coincidencias, 
     filas, columnas, tipo_ficha, tiempo, nick) = cla.Partida.mise_en_place()
    
    partida = cla.Partida(dificultad, nivel, nivel_inicial, nivel_estatico, coincidencias,
                          filas, columnas, tipo_ficha, tiempo, nick, siguiente)
    
    verde = '#10ae23'
    verde_claro = '#11da29'
    amarillo = '#f1e910'
    gris = '#343434'
    rojo = '#d91644'
    blanco = '#FFFFFF'   
    defecto = DEFAULT_BUTTON_COLOR
    pausa_momentanea = False

    if otros_puntos > 0 and not nivel_estatico:
        partida.inc_puntos(otros_puntos)
    color_dific = [rojo if dificultad == 'Difícil' 
                   else amarillo if dificultad == 'Normal'
                   else verde_claro]
    
    top_windows = [sg.Column([
                    [sg.Text(nick, text_color='#4185e1', background_color='#173155',
                             font=('Arial', 14), size=(12,1), justification='c')],
                    [sg.Text(dificultad + '  -  ' + str(nivel), text_color=color_dific,
                             background_color='#173155',
                             font=('Arial', 14), size=(12,1), justification='c')]]),
                    sg.Column([[sg.Text('')]]),
                    sg.Column([
                    [sg.Text(('Tiempo: ' + partida.get_tiempo_string()),
                            justification='left', size=(13,1),
                            key='reloj', font=('Verdana', 12)), 
                    sg.Text('Puntos: ' + str(partida.get_puntos()),
                            key='puntos', size=(13,1),
                            justification='left', font=('Verdana', 12))],
                    [sg.Text('Encontrada: ', key='encontrada', size=(26,1),
                            justification='left', font=('Verdana', 12))]])
                  ]
    bottom_window = [
                    [sg.Button('Comenzar', key='comenzar', size=(14,1),
                                font=('Times New Roman', 20), mouseover_colors=(blanco, verde)),
                    sg.Button('Pausar', key='pausar', size=(14,1), mouseover_colors=(blanco, amarillo),
                              font=('Times New Roman', 20), visible=False)], 
                    [sg.Button('Reiniciar', key = 'reiniciar', mouseover_colors=(blanco, amarillo),
                               size= (11,1), font=('', 12)), 
                    sg.Button('Salir', key='salir', mouseover_colors=(blanco, rojo),
                              size= (11,1), font=('', 12))]
                    ]
    layout = [top_windows, partida.get_fichas(), bottom_window]

    window = sg.Window('MemPyG28', 
                       layout, element_justification='c', margins=(30,5))
    partida.window = window
    mensajes = funcs.get_info_usuario_actual()['Configuración']['Mensajes']
    comenzado = False
    
    while True:
        if siguiente and not partida._nivel_estatico:
            sg.popup('Siguiente nivel', auto_close=True, auto_close_duration=2, 
                     line_width=50, no_titlebar=True, background_color=gris, 
                     text_color=amarillo, font=('Verdana', 14), button_type=5,
                     button_color=gris, custom_text='Vamos')
            siguiente = False        
               
        event, values = window.read(timeout=10)
        
        if event == sg.WINDOW_CLOSED:
            break
        if event == 'salir':
            if comenzado and not partida._paused:
                funcs.pausar_juego(partida)
                pausa_momentanea = True
            salir = sg.popup('Salir al menu inicio?', 
                             custom_text=('Salir', 'Cancelar'), no_titlebar=True,
                             background_color='Black', text_color='White')
            if salir == 'Salir':
                if comenzado:
                    evento_partida(partida.get_tiempo_string(), filas, columnas, coincidencias,
                                   nick, nivel, dificultad, 'fin_partida', 'abandonada')
                window.close()
                inicio.main()
            elif comenzado and pausa_momentanea:
                funcs.despausar_juego(partida)
                pausa_momentanea = False

        elif event == 'reiniciar':
            if comenzado and not partida._paused:
                funcs.pausar_juego(partida)
                pausa_momentanea = True
            reiniciar = sg.Popup('Si reiniciás la partida\n' 
                        + 'vas a perder los puntos\n' + '¿Está seguro?', 
                        custom_text=('Reiniciar', 'Cancelar'), no_titlebar=True,
                        background_color='Black', text_color='White')
            if reiniciar == 'Reiniciar':
                partida.reiniciar_juego()
            elif comenzado and pausa_momentanea:
                funcs.despausar_juego(partida)
                pausa_momentanea = False
        
        if not comenzado:
            if event == 'comenzar':
                evento_partida(partida.get_tiempo_string(), filas, columnas, coincidencias,
                               nick, nivel, dificultad, 'inicio_partida')
                comenzado = True
                window['comenzar'].Update(visible = False)
                window['pausar'].Update(visible = True)
                partida.resetear_tiempo()
        else:
            if (not partida.paused()):
                if event == 'pausar':
                    funcs.pausar_juego(partida)
                    defecto = sg.theme_button_color()
                    window['pausar'].Update(text='Despausar', button_color=rojo)

                event = event.replace('__TIMEOUT__', '') if type(event) == str else event

                partida.check_tiempo_turno()
                partida.actualizar_tiempo()
                if partida.tiempo_restante() < 0:
                    mensajes = funcs.get_info_usuario_actual()['Configuración']['Mensajes']
                    partida.terminar_juego(mensajes['Derrota'], False)
                    evento_partida(partida.get_tiempo_string(), filas, columnas, coincidencias,
                                      nick, nivel, dificultad, 'fin_partida', 'timeout')
                window.FindElement('reloj').Update('Tiempo: ' + partida.get_tiempo_string())

                if partida._tiempo_final and partida.tiempo_restante()<=10:
                    partida._tiempo_final=False
                    window.FindElement('reloj').Update(font=('Verdana', 12),
                                                       text_color= rojo)

                if type(event) == tuple:
                    y, x = event
                    partida.progreso_partida(y, x)
                    partida.actualizar_puntos()    
                if len(partida.get_encontradas()) > 0:
                    ultima = partida.get_encontradas()[-1]
                    if (window['encontrada'].DisplayText != ('Encontrada: ' + ultima)):
                        window.FindElement('encontrada').Update('Encontrada: ' + ultima)
            else:   
                if event == 'pausar':
                    funcs.despausar_juego(partida)
                    window['pausar'].Update(text='Pausar', button_color=defecto)
                    

    window.close()

if __name__ == '__main__':
    
    main() 