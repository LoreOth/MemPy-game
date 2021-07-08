from PySimpleGUI.PySimpleGUI import DEFAULT_BUTTON_COLOR
import src.auxiliares.funciones_generales as funcs
import src.ventanas.menu_inicio as menu
import PySimpleGUI as sg
import os


def animacion_guardado ():
    """ Función invocada luego de la actualziación 
    de datos actualzados para mostrar una animación
    de barra de progreso que simula datos guardados
    en disco """
    
    layout = [[ sg.Text('Guardando cambios')],
        [sg.ProgressBar(60, orientation ='h', size=(20,20), key='progressbar')]
        ]
    window= sg.Window('Actualizando configuración', layout)
    progress_bar = window['progressbar']
    for i in range (60):
        event, values = window.read(timeout=10)
        if event == sg.WIN_CLOSED  :
            break
        progress_bar.UpdateBar(i +1)
    window.close()

def main():
    """ Ventana principal del panel de configuración, a través 
    de la cual se pueden decidir todas las variantes del juego,
    como la dificultad, el tipo de fichas, los mensajes 
    a mostrar al usuario y los colores del juego en sí. 
    Además, se puede acceder a las instrucciones del juego para 
    un encuentro más familiar incluso en el primer intento """
    config = funcs.get_info_usuario_actual()['Configuración']
    ruta_cabs = os.getcwd() + os.sep + 'img' + os.sep + 'Cabeceras' + os.sep
    ruta_instr = os.getcwd() + os.sep + 'img' + os.sep + 'Instrucciones' + os.sep
    
    tres =   [1, 2, 3]
    cuatro = [1, 2, 3, 4]
    cinco =  [1, 2, 3, 4, 5]
    dific_act =   config['Dificultad']
    nivel_estatico = config['Nivel_estático']
    mensajes = config['Mensajes']
    tema_act = config['Tema']
    fichas_act = config['Fichas']
    defecto = DEFAULT_BUTTON_COLOR
    verde = '#10ae23'
    aguamarina = '#5ae5c3'
    

    diseño=[
        [sg.Text('Configuraciones', font=('Trebuchet MS',35), size=(20,1), 
                 justification='c', background_color='#1e1e1e',
                 text_color=aguamarina)],
        [sg.Column ([
        #----------------------------Dificultad----------------------------
        [sg.Image(ruta_cabs + 'Dificultad.png')],
        [sg.Text('No a todos les gusta jugar bajo el mismo nivel de presión. '
                 + 'Algunos prefieren algo simple y relajado, mientras otros '
                 + 'querrán ponerse a prueba. MemPyG28 ofrece 3 niveles de '
                 + 'dificultad para que todos queden satisfechos. Nota: '
                 + 'Cuando decimos "difícil" lo decimos en serio. '
                 + 'Proceder bajo su propio riesgo.',    
                 font=('Trebuchet MS',11),size=(50,6), justification='c')],
        [sg.Text('Dificultad', font = ('Helvetica',13)), 
        sg.Text('Nivel inicial', font = ('Helvetica',13))],
        [sg.InputCombo(['Fácil', 'Normal', 'Difícil'], default_value = (config['Dificultad']), 
                font = ('Helvetica',12), key = 'Dificultad', size=(8,1), enable_events=True,),
        sg.InputCombo(tres, default_value = config['Nivel_inicial'] 
                      if dific_act == 'Fácil' else 1, size=(5,1), enable_events=True,
                      key = 'NivelF', visible = (dific_act=='Fácil')), 
        sg.InputCombo(cuatro, default_value = config['Nivel_inicial'] 
                      if dific_act == 'Normal' else 1, size=(5,1),enable_events=True,
                      key = 'NivelN', visible = (dific_act=='Normal')),
        sg.InputCombo(cinco, default_value = config['Nivel_inicial'] 
                      if dific_act == 'Difícil' else 1, size=(5,1),enable_events=True,
                      key = 'NivelD', visible = (dific_act=='Difícil'))],
        [sg.Checkbox('Nivel estático', default=nivel_estatico, key='estático')],
        [sg.Text('\n')],
        #----------------------------Tipo ficha----------------------------
        [sg.Image(ruta_cabs + 'Tipo ficha.png')],
        [sg.Text('MemPyG28 te permite jugar buscando coincidencias entre '
                 + 'dos grandes tipos de variantes: Palabras e Imágenes. '
                 + 'De esta decisión dependerá lo que veas dentro de cada ficha. '
                 + 'Es íntegramente estético, y ambas opciones tienen '
                 + 'múltiples variantes, dependiendo del día y horario en '
                 + 'que decidas jugar.',    
                 font=('Trebuchet MS',11),size=(50,6), justification='c')],
        [sg.Button('Palabras', font=('Helvetica',13), key='Palabras',
                   button_color=(verde if fichas_act=='Palabras' else defecto)), 
        sg.Button('Imágenes', font =('Helvetica',13), key='Imágenes',
                  button_color=(verde if fichas_act=='Imágenes' else defecto))],
        [sg.Text('\n')],
        #-----------------------------Temática-----------------------------
        [sg.Image(ruta_cabs + 'Temática.png')],
        [sg.Text('MemPyG28 te ofrece una diversa gama de colores para '
                 + 'configurar tu juego y darte así una experiencia más '
                 + 'placentera y confortable. Hay colores más suaves, '
                 + 'otros más electricos, e incluso relacionados a cosas '
                 + 'que puedas conocer. Elegí el que mejor se ajuste a vos!',    
                 font=('Trebuchet MS',11),size=(50,6), justification='c')],
        [sg.Button('Verde Oscuro', key='DarkGreen',
                font =('Helvetica',13), size=(12,1),
                button_color=(verde if tema_act=='DarkGreen' else defecto)),
        sg.Button('Púrpura Oscuro', key='DarkPurple',
                font =('Helvetica',13), size=(12,1),
                button_color=(verde if tema_act=='DarkPurple' else defecto))],
        [sg.Button('Azul Oscuro', key='DarkBlue',
                font =('Helvetica',13), size=(12,1),
                button_color=(verde if tema_act=='DarkBlue' else defecto)),
        sg.Button('Oscuro', key='Dark2',
                font =('Helvetica',13), size=(12,1),
                button_color=(verde if tema_act=='Dark2' else defecto)),
        sg.Button('Topanga', key='Topanga',
                font =('Helvetica',13), size=(12,1),
                button_color=(verde if tema_act=='Topanga' else defecto))],
        [sg.Button('Bronceado', key='Tan',
                font =('Helvetica',13), size=(12,1),
                button_color=(verde if tema_act=='Tan' else defecto)),
        sg.Button('Colores Brillantes', key='BrightColors',
                font =('Helvetica',13), size=(12,1),
                button_color=(verde if tema_act=='BrightColors' else defecto)),
        sg.Button('Bordeau', key='Reds',
                font =('Helvetica',13), size=(12,1),
                button_color=(verde if tema_act=='Reds' else defecto))],
        [sg.Button('Reddit', key='Reddit',
                font =('Helvetica',13), size=(12,1),
                button_color=(verde if tema_act=='Reddit' else defecto)),
        sg.Button('Azul y Bronceado', key='TanBlue',
                font =('Helvetica',13), size=(12,1),
                button_color=(verde if tema_act=='TanBlue' else defecto)),
        sg.Button('Marrón y Azul', key='BrownBlue',
                font =('Helvetica',13), size=(12,1),
                button_color=(verde if tema_act=='BrownBlue' else defecto))],
        [sg.Button('Azul y Púrpura', key='BluePurple',
                font =('Helvetica',13), size=(12,1),
                button_color=(verde if tema_act=='BluePurple' else defecto)),
        sg.Button('Negro', key='Black',
                font =('Helvetica',13), size=(12,1),
                button_color=(verde if tema_act=='Black' else defecto)),
        sg.Button('Playa de Arena', key='SandyBeach',
                font =('Helvetica',13), size=(12,1),
                button_color=(verde if tema_act=='SandyBeach' else defecto))],
        [sg.Text('\n')],
        #-----------------------------Mensajes-----------------------------
        [sg.Image(ruta_cabs + 'Mensajes.png')],
        [sg.Text('Ya sea al ganar, perder u otros, distintos mensajes '
                 + 'de aliento  aparecerán en pantalla. MemPyG28 te '
                 + 'ofrece los siguientes, por defecto, pero te invita '
                 + 'a cambiarlos por lo que mejor te haga sentir leer.',    
                 font=('Trebuchet MS',11),size=(50,5), justification='c')],
   
        [sg.Text('Victoria', font=('Helvetica',15), justification='center',
                 size=(30,1))],
        [sg.InputText(default_text = mensajes['Victoria'], key='Victoria')],
        
        [sg.Text('Puntaje mayor no superado', font=('Helvetica',15),
                 justification='center', size=(30,1))],
        [sg.InputText(default_text = mensajes['Puntaje'], key='Puntaje')],    
    
        [sg.Text('Derrota',font=('Helvetica',13), justification='center',
                  size=(30,1))], 
        [sg.InputText(default_text = mensajes['Derrota'], key='Derrota')],
        [sg.Text('\n')],
        #---------------------------Instrucciones---------------------------
        [sg.Image(ruta_cabs + 'Instrucciones.png')],
        [sg.Text('-Primeros pasos-',    
                 font=('Trebuchet MS',14),size=(30,1), justification='c')],
        [sg.Text('Para jugar a MempyG28, ahora que tenés una cuenta, '
                 + 'lo que tenés que hacer es regresar al menú principal '
                 + '(tocando el botón "Salir") e ingresar a la sección "Sala de Juego".'
                 + 'La partida no comenzará hasta que presiones el botón de "Comenzar".\n'
                 + 'Una vez comenzada la partida, podés pausarla cuando '
                 + 'quieras con el botón "Pausar". Esto no va a afectar '
                 + 'tu puntaje ni nada por el estilo.',    
                 font=('Trebuchet MS',11),size=(50,7), justification='c')],
        [sg.Text('')],
        [sg.Image(ruta_instr + 'Comenzar pausar.png'),
         sg.Image(ruta_instr + 'Salir.png')],
        [sg.Text('')],
        [sg.Text('-Nociones básicas-',    
                 font=('Trebuchet MS',14),size=(30,1), justification='c')],
        [sg.Text('El juego consiste en encontrar todas las fichas '
                 + 'iguales en un mismo turno.\n'
                 + 'Para esto, vas a tener tantos intentos como fichas iguales '
                 + 'debas encontrar. Si estás jugando la dificultad Fácil '
                 + '(por defecto será así), deberás encontrar 2 (dos) '
                 + 'fichas iguales; si decidiste afrontar las dificultades '
                 + 'Normal o Difícil, este número asciende a 3 (tres). '
                 + 'En cualquier caso, solo abrá un grupo de cada tipo '
                 + '(cada ficha estará a lo sumo 2 o 3 veces en el '
                 + 'tablero, no más).\n'
                 + 'En caso de encontrar todas las coincidencias de una ficha, '
                 + 'estas te darán puntos, y se retirarán del juego. '
                 + 'Si fallaras al encontrarlas, o se terminara el tiempo '
                 + 'de tu turno (3 segundos) volverán a darse vuelta.',    
                 font=('Trebuchet MS',11),size=(50,12), justification='c')],
        [sg.Text('')],
        [sg.Image(ruta_instr + 'Ficha dada vuelta.png'),
         sg.Image(ruta_instr + 'Fichas desactivadas.png')],
        [sg.Text('')],
        [sg.Text('-Objetivos-',    
                 font=('Trebuchet MS',14),size=(30,1), justification='c')],
        [sg.Text('El objetivo del juego primordial del juego es llegar '
                 + 'finalizar hasta el último nivel de la dificultad '
                 + 'que estés jugando. En cada caso, la cantidad variará.\n'
                 + 'Pero en un segundo lugar, si tu intención fuera ser '
                 + 'más competitivo, tu objetivo será entrar en la tabla '
                 + 'de rankings. Solo los mejores 5 (cinco) puntajes se '
                 + 'mostrarán en pantalla (por cada dificultad y nivel) '
                 + 'tras finalizar una partida, así que buena suerte!',    
                 font=('Trebuchet MS',11),size=(50,8), justification='c')],
        [sg.Text('')],
        [sg.Image(ruta_instr + 'Nivel completo.png'),
         sg.Image(ruta_instr + 'Ranking.png')],
        [sg.Text('')],
        [sg.Text('-Puntos-',    
                 font=('Trebuchet MS',14),size=(30,1), justification='c')],
        [sg.Text('El sistema de puntos es muy simple: Cada vez que '
                 + 'encuentres un par o terna de fichas, ganás 10 (diez) '
                 + 'puntos por ficha encontrada. También, al finalizar '
                 + 'cada nivel, cada segundo restante es 1 (un) punto '
                 + 'extra que sumás.\n'
                 + 'Ahora bien, si durante la partida fallás en encontrar '
                 + 'los pares necesarios, se te va a restar 1 (un) punto. '
                 + 'Y cuidado! Porque si dejás pasar el tiempo del turno '
                 + '(3 segundos), los puntos restados son 2 (dos), '
                 + 'así que mejor animarse a buscar que dudar y '
                 + 'perder el turno.\n'
                 + 'A lo largo de los niveles, el puntaje se acarrea, '
                 + 'así que aprovechá los iniciales -que siempre van '
                 + 'a ser más fáciles-, para juntar una buena cantidad.',    
                 font=('Trebuchet MS',11),size=(50,12), justification='c')],
        [sg.Text('')],
        [sg.Image(ruta_instr + 'Puntos acarreados.png')],
        [sg.Text('\n')]
        #Otras configuraciones de la Columna:
        ],scrollable = True, vertical_scroll_only=True, size=(490,420),
                    element_justification='c')],
        
        [sg.Column([
            [sg.Button('Aceptar', font=('Verdana',13), size=(7,1), button_color='green'),
            sg.Button('Salir', font=('Verdana',13), size=(6,1), button_color ='red' )],
            [sg.Text('', font=('Trebuchet MS',35), size=(20,1), 
                 justification='c', background_color='#1e1e1e')]
        ], element_justification='center')]
        
        ]

    window = sg.Window('MemPyG28', diseño, margins=(5,5), size=(560,610),
                        element_justification='left')
    
    while True:    
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            window.close()
            break
        if event == 'Salir':
            window.close()
            menu.main()
            break   
        #Chequeo anti-hackerz, si escriben entradas basura, se pone por defecto 'Fácil' y/o '1'
        dificultad_elegida = (values.get('Dificultad') if values.get('Dificultad')
                              in ['Fácil', 'Normal', 'Difícil'] else 'Fácil')
        if (values.get('Dificultad')=='Fácil' and (values.get('NivelF') in [1,2,3])):
            nivel_elegido = (values.get('NivelF'))
        elif (values.get('Dificultad')=='Normal' and (values.get('NivelN') in [1,2,3,4])):
            nivel_elegido = (values.get('NivelN'))
        elif (values.get('Dificultad')=='Difícil' and (values.get('NivelD') in [1,2,3,4,5])):
            nivel_elegido = (values.get('NivelD'))
        else:
            nivel_elegido = 1
                
        if (config['Dificultad'] != dificultad_elegida
            or ((config['Nivel_inicial']) != nivel_elegido)
            or ((config['Nivel_actual']) != nivel_elegido)):
            window['NivelF'].Update(visible=(dificultad_elegida=='Fácil'))
            window['NivelN'].Update(visible=(dificultad_elegida=='Normal'))
            window['NivelD'].Update(visible=(dificultad_elegida=='Difícil'))
            config['Dificultad'] = dificultad_elegida
            config['Nivel_inicial'] = nivel_elegido
            config['Nivel_actual'] = nivel_elegido

        if event in ['Palabras', 'Imágenes']:
            config['Fichas'] = event
            if event == 'Imágenes':
                window['Imágenes'].Update(button_color=verde)
                window['Palabras'].Update(button_color=defecto)
            else:
                window['Palabras'].Update(button_color=verde)
                window['Imágenes'].Update(button_color=defecto)
        elif event in ['DarkGreen','DarkPurple','DarkBlue','Dark2',
                       'Topanga','Tan','BrightColors','Reds','Reddit',
                       'TanBlue','BrownBlue','BluePurple', 'Black', 'SandyBeach']:
            window[config['Tema']].Update(button_color=defecto)
            window[event].Update(button_color=verde)
            config['Tema'] = event
        elif event in ['Victoria', 'Puntaje', 'Derrota']:
            config['Mensajes'][event] = values.get(event)
        elif event == 'Aceptar':
            config['Nivel_estático'] = values.get('estático')
            funcs.actualizar_config(config)
            animacion_guardado()
            window.close()
            menu.main()
            break


if __name__ == '__main__':
    main()