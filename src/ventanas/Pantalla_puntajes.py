from tkinter.font import ITALIC
import PySimpleGUI as sg 
import os
import src.ventanas.menu_inicio as inicio
import pandas as pd
import src.auxiliares.funciones_generales as funcs

path_ranking = (os.getcwd() + os.sep + 'data' 
                + os.sep + 'usuarios' + os.sep + 'ranking.csv')

columnas = ['Nick','Puntaje','Dificultad','Nivel']


def existe_registro_rankings():
    """ Se comprueba que exista el archivo de rankings, en caso de no existir se crea
    vacío con los correspondientes nombres de columnas """

    #esta expresion evalua si existe el directorio que recibe como parametro y retorna un booleano
    if not os.path.isfile(path_ranking):
        datos = []
        df_registro_eventos = pd.DataFrame(datos, columns=columnas)
        df_registro_eventos.to_csv(path_ranking, index=False, encoding='UTF-8')

    
def insertar_puntaje(nick, ultimo_puntaje, dificultad, nivel):
    """ Recibe un intento de record y ve
    de insertarlo en la tabla a mostrar,
    de acuerdo a su dificultad y nivel """
    
    #se carga el csv de puntajes acumulados
    df_rankings = pd.read_csv(path_ranking, encoding='UTF-8')

    #se cargan los datos del nuevo registro
    datos = [[nick, ultimo_puntaje, dificultad, nivel]]

    #se obtienen los mejores puntajes segun los filtros y ademas los que no coincidan
    df_data = df_rankings[df_rankings['Dificultad'] == dificultad]
    df_data = df_data[df_data['Nivel'] == nivel]
    
    df_resto = df_rankings[(~(df_rankings['Nivel'] == nivel) | (df_rankings['Dificultad'] != dificultad))]
    
    #se agrega el nuevo registro a los anteriores, se ordenan y se guardan los 5 mas altos
    nueva_fila = pd.DataFrame(datos, columns=columnas)    
    df_data = df_data.append(nueva_fila, ignore_index=True).sort_values(by='Puntaje', ascending=False).head(5)
    
    #se vuelven a cargar los datos completos
    df_nuevos_rankings = df_resto.append(df_data, ignore_index=True)
    df_nuevos_rankings.to_csv(path_ranking, index=False, encoding='UTF-8')


def recuperar_top(dificultad, nivel):
    """ Por medio de una lectura a un CSV de rankings,
    recupera los datos necesarios para mostrar en
    la tabla el top 5 de la dificultad y nivel seleccionados """
    df_data = pd.read_csv(path_ranking, encoding='UTF-8')

    df_datos_filtrados = df_data[df_data['Dificultad'] == dificultad]
    df_datos_filtrados = df_datos_filtrados[df_datos_filtrados['Nivel'] == nivel]

    return df_datos_filtrados.values

def valores_iniciales(dific_act, nivel_elegido):
    recuperado = recuperar_top(dific_act, nivel_elegido)
    nicks = []
    puntos = []
    for i in recuperado:
        nicks.append(i[0])
        puntos.append(i[1])
    while len(nicks)<5:
        nicks.append('-')
        puntos.append('-')
    return nicks, puntos


def actualizar_top(window, datos):
    """ Actualiza los datos a mostrar, para cada una
    de las cinco lineas, en la tabla de rankings,
    con los datos recibidos por parámetros """
    for i in range(5):
        try:
            dato = datos[i]
        except IndexError:
            dato = ['-', '-']
        window[f'nick{i}'].Update(f"{dato[0]: ^20}")
        window[f'puntos{i}'].Update(f"{dato[1]: ^4}")

def entrada_externa(partida):
    """ Inicializa los valores de la partida,
    cuando se debe insertar en la tabla pero el
    llamado no llega desde la pantalla de puntajes.
    Esto se da ante un nivel ganado que no es el último """
    nick = partida.get_nick()
    ultimo_puntaje = partida.get_puntos()
    dificultad = partida.get_dificultad()
    nivel = partida.get_nivel()
    if ultimo_puntaje > 0:
        existe_registro_rankings()
        insertar_puntaje(nick, ultimo_puntaje, dificultad, nivel)

def main(partida = None):
    """ Inicializa la pantalla de puntajes, 
    con un top 5 de los mejores puntajes registrados
    para esa dificultad y nivel. Estas opciones
    son elegibles a través de listas desplegables """
    tabla_visible = True
    if partida == None:
        nick = ''
        ultimo_puntaje = 0
        tiempo = ''
        tabla_visible = False
    else:
        nick = partida.get_nick()
        ultimo_puntaje = partida.get_puntos()
        tiempo = partida.get_tiempo_string()
        dificultad = partida.get_dificultad()
        nivel = partida.get_nivel()
        if ultimo_puntaje > 0:
            existe_registro_rankings()
            insertar_puntaje(nick, ultimo_puntaje, dificultad, nivel)
        
    config = funcs.get_info_usuario_actual()['Configuración']   
    nuevo_record = False
    if (ultimo_puntaje > config['Record']):
        config['Record'] = ultimo_puntaje
        funcs.actualizar_config(config)
        nuevo_record = True
    mensaje_nuevo_record = config['Mensajes']['Puntaje']
    gris = '#1e1e1e'
    rojo = '#d91644'
    aguamarina = '#5ae5c3'
    beige = '#e0a889'
    beige_oscuro = '#a77d66'
    arena = '#e0c489'
    negro = '#000000'

    tres =   [1, 2, 3]
    cuatro = [1, 2, 3, 4]
    cinco =  [1, 2, 3, 4, 5]
    dific_act = config['Dificultad']
    if partida != None:
        nivel_elegido = partida.get_nivel()
    else:
        nivel_elegido = 1
    dific_key = ''
    dificultad_anterior = ''
    
    #- - - - - - - - - - Partes del Layout - - - - - - - - - -
    encabezado = [sg.Text("Puntajes:", justification='center', 
                        font=('Trebuchet MS',35), size=(18,1), 
                        background_color=gris, text_color=aguamarina)]
    
    tip = [sg.Text('Elegí de qué dificultad y nivel querés '
                   + 'ver los mejores puntajes:', font=('Verdana',11,ITALIC), 
                   justification='center', size=(40,3))]
    
    opciones = [
                [sg.Text('Dificultad', font = ('Helvetica',15), justification='right'), 
                sg.Text('Nivel', font = ('Helvetica',15), justification='left')],
                [sg.InputCombo(['Fácil', 'Normal', 'Difícil'], enable_events=True,
                               default_value = (config['Dificultad']), 
                               font = ('Helvetica',12), key = 'Dificultad', size=(8,1)),
                sg.InputCombo(tres, default_value = nivel_elegido
                              if dific_act == 'Fácil' else 1, size=(5,1), enable_events=True,
                              key = 'NivelF', visible = (dific_act=='Fácil')), 
                sg.InputCombo(cuatro, default_value = nivel_elegido
                              if dific_act == 'Normal' else 1, size=(5,1), enable_events=True,
                              key = 'NivelN', visible = (dific_act=='Normal')),
                sg.InputCombo(cinco, default_value = nivel_elegido
                              if dific_act == 'Difícil' else 1, size=(5,1), enable_events=True,
                              key = 'NivelD', visible = (dific_act=='Difícil'))]
                ]
    
    titulos = [sg.Text((f"{'Nick': ^30}{' ':5}{'Puntaje': >8}"),
                       background_color=arena, text_color='#000000', 
                       font=('Arial', 14), size=(24,1), justification='c')]
    
    nicks, puntos = valores_iniciales(dific_act, nivel_elegido)
    columna_nicks = [
        [sg.Text((nicks[i]),
                background_color = beige_oscuro, key=(f'nick{i}'), size=(15,1),
                text_color='#FFFFFF', font=('Arial',14), justification='c')]
                    for i in range(5)
    ]
    columna_puntos = [
         [sg.Text((puntos[i]),
                background_color = beige_oscuro, key=(f'puntos{i}'), size=(6,1),
                text_color='#FFFFFF', font=('Arial',14), justification='c')]
                    for i in range(5)  
    ]
    
    top_5 = [sg.Column(columna_nicks, background_color=beige, element_justification='c'), 
            sg.Column(columna_puntos, background_color=beige, element_justification='c')]   

    ultimo_resultado =  [[sg.Text(mensaje_nuevo_record, 
                                 font=('Arial', 14), justification='center',
                                border_width=3, visible=(tabla_visible and nuevo_record))],
                        [sg.Text('')],
                        [sg.Text((f'{nick}, hiciste {ultimo_puntaje} puntos, sobrando {tiempo}'),
                                font=('Arial', 14), justification='center',
                                border_width=3, visible=tabla_visible)]
                        ]
    
    botones = [sg.Button('Salir', key='Salir', mouseover_colors=rojo,
                        font=('Verdana', 20), button_color=(negro,arena),
                        size=(10,1))]
    
    barra_abajo = [sg.Text("", justification='center', 
                        font=('Trebuchet MS',20), size=(32,1), 
                        background_color=gris, text_color=aguamarina)]
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    
    layout = [encabezado, tip, opciones, titulos, top_5, 
              ultimo_resultado, botones, barra_abajo]
    window = sg.Window('MemPyG28', layout, element_justification='c', 
                        margins=(20,10))
    
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        elif event == 'Salir':
            window.close()
            inicio.main()
        else:
            dificultad_elegida = (values.get('Dificultad') if values.get('Dificultad')
                                in ['Fácil', 'Normal', 'Difícil'] else 'Fácil')
            if (dificultad_elegida=='Fácil' and (values.get('NivelF') in [1,2,3])):
                nivel_elegido = (values.get('NivelF'))
                dific_key = 'NivelF'
            elif (dificultad_elegida=='Normal' and (values.get('NivelN') in [1,2,3,4])):
                nivel_elegido = (values.get('NivelN'))
                dific_key = 'NivelN'
            elif (dificultad_elegida=='Difícil' and (values.get('NivelD') in [1,2,3,4,5])):
                nivel_elegido = (values.get('NivelD'))
                dific_key = 'NivelD'
            else:
                nivel_elegido = 1
            
            if ((event in ['Dificultad','NivelF','NivelN','NivelD']) and
                (values.get('Dificultad') != dificultad_anterior
                or (values.get(dific_key)) != nivel_elegido)):
                window['NivelF'].Update(visible=(dificultad_elegida=='Fácil'))
                window['NivelN'].Update(visible=(dificultad_elegida=='Normal'))
                window['NivelD'].Update(visible=(dificultad_elegida=='Difícil'))
                dificultad_anterior = dificultad_elegida

            datos = recuperar_top(dificultad_elegida, nivel_elegido)
            actualizar_top(window,datos)

    window.close()

if __name__ == '__main__':
    main()