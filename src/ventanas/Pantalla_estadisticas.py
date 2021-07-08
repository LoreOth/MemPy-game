import PySimpleGUI as sg
import os
import pandas as pd
import src.ventanas.menu_inicio as inicio
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import*
from collections import Counter as cs

ruta_data = os.getcwd() + os.sep + 'data' + os.sep + 'usuarios' + os.sep 

def main():
    """  Función que genera para cada tipo de estadistica, 
    según sus valores gráficos, un grafico y lo vincula a 
    su respectiva pestaña dentro de un misma ventana  """
    
    def getPandasData():
        """ Función que retorna en datos_mempy la estructura de 
        datos en las columnas definidas en datos_mempy.columns """

        datos_mempy = pd.read_csv(f'{ruta_data}registro_eventos.csv', encoding='latin-1')
        return datos_mempy

    """ Diccionario el cual define para cada clave 
    (los tres gráficos), sus respectivos campos  """
    valores_graficos = {

        'Partidas finalizadas por género': {"campo_a_filtrar": 'usuarie-genero', 
                                            'campo_agrupar': 'usuarie-genero', 
                                            "filtro": "binarie"},
        'Partidas por estado de finalización': {"campo_a_filtrar": 'nombre_evento', 
                                            'campo_agrupar': 'estado', 
                                            "filtro": "fin_partida"},
        'Top 10 palabras mas usadas': {"campo_a_filtrar": None, 
                                        'campo_agrupar': 'estado',
                                        'filtro' : 'top'},
    }

    def layout(x):
        """ Función que retorna un canvas para cada gráfico de la pestaña """

        return [[sg.Text('Estadísticas Mempy', size=(40, 1),
                                    justification='center', font='Helvetica 20')],
                        [sg.Canvas(size=(640, 480),
                                    key='{}'.format(x))],
                        ]

    def mostrar_grafico(plt, data):
        """ Esta función recibe los datos a graficar, y genera una gráfico de torta"""

        datos_mempy = getPandasData()
        campo_a_filtrar = data['campo_a_filtrar']
        campo_agrupar = data['campo_agrupar']
        filtro = data['filtro'] if 'filtro' in data.keys() else 'sin datos'

        if not campo_a_filtrar:
            a = datos_mempy[datos_mempy["nombre_evento"]=="intento"]
            b = a[datos_mempy["estado"]=="correcto"]
            l = [ list((datos.head(1)["palabra"]))[0] for _partida,datos in b.groupby(["partida"])]

            
            resultado = cs(l).most_common(10)
            etiquetas = list(map(lambda x:x[0],resultado))
            datos = list(map(lambda x:x[1],resultado))
            explode = [0]*len(etiquetas)


        elif filtro == 'fin_partida':
            datos = datos_mempy[datos_mempy[campo_a_filtrar] == filtro].groupby([campo_agrupar])[campo_agrupar].count()
            explode = [0]*len(datos.values)
            etiquetas = datos.keys()
        
        else:
            datos = datos_mempy[datos_mempy[campo_a_filtrar] != filtro].groupby([campo_agrupar])[campo_agrupar].count()
            explode = [0]*len(datos.values)
            etiquetas = datos.keys()
        
        
        plt.pie(datos, explode=explode, labels=etiquetas,
                autopct='%1.1f%%', shadow=True, startangle=90, labeldistance=1.1,pctdistance=0.9) 
        plt.axis('equal')
        plt.legend(bbox_to_anchor=(0.85, 0.15), loc='upper left')

    def dibujar_figura(canvas, figure):
        """ Función que dibuja la figura en pantalla """
        figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
        figure_canvas_agg.draw()
        figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
        

    keysCanvas = list(valores_graficos.keys()) 
    layoutTabs = [layout(i) for i in keysCanvas] # Asocio a cada pestaña su respectivo canvas

    """ Tabgrp se corresponde a las 3 pestañas asociadas 
    a sus respectivos layoutTabs[0],layoutTabs[1],layoutTabs[2] """

    tabgrp = [[sg.TabGroup([[sg.Tab('Finalizadas por género', layoutTabs[0], 
                                    title_color='Red', border_width=10, 
                                    background_color='Green',
                                    tooltip='Personal details', 
                                    element_justification='center'),
                            sg.Tab('Estado de finalización', 
                                    layoutTabs[1], title_color='Blue', border_width=10,
                                    background_color='Yellow'),
                            sg.Tab('Top 10 palabras', layoutTabs[2], border_width=10,
                                    title_color='Black', background_color='Pink')]], 
                            tab_location='centertop', title_color='Red', 
                            tab_background_color='Purple', selected_title_color='Green',
                            selected_background_color='Gray', border_width=5)],
              [sg.Text('')],
              [sg.Button('Salir',size=(14, 1), pad=((280, 0), 3), font='Helvetica 14')]
            ]

    window = sg.Window(
        'Elija la estadística que desea visualizar', tabgrp, finalize=True)

    for canva in keysCanvas:
        canvas_elem = window[canva]
        canvas = canvas_elem.TKCanvas

        fig, (ax1) = plt.subplots(1, 1)
        fig.suptitle(canva)

        mostrar_grafico(ax1, valores_graficos[canva])

        dibujar_figura(canvas, fig)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        if event == None or event == "Salir":   
            window.close()
            inicio.main()
            break
    window.close()

if __name__ == '__main__':
    main()

    