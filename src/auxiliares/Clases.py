import os
import PySimpleGUI as sg
from random import randrange, sample
import json
from time import sleep
from pathlib import Path
import src.auxiliares.funciones_generales as funcs
import src.auxiliares.criterios as crits
import src.auxiliares.generador_palabras as genpal
import src.auxiliares.registro_eventos as reg
import src.ventanas.pantalla_puntajes as punt
import src.ventanas.pantalla_juego as juego
import time

carpeta_imagenes = os.getcwd() + os.sep + 'img' + os.sep
cpt_fondo_palabras = carpeta_imagenes + 'Palabras' + os.sep
nivel_inicial = funcs.get_info_usuario_actual()['Configuración']['Nivel_inicial']


class Ficha(sg.PySimpleGUI.Button):
    def __init__(self, nombre, ID, **extra_fields):
        """ Inicializa las propiedades del objeto, 
        presentes en su clase padre, mediante una 
        llamada a dicha clase """
        super(Ficha, self).__init__(' ', image_filename=
                                    (carpeta_imagenes + 'Back.png'),
                                    **extra_fields)
        #Valores locales
        self._ID = ID
        self._nombre = nombre
        self._boca_arriba = False
        self._dorso = carpeta_imagenes + 'Back.png'
        self._imagen = ''
        
    def darse_vuelta(self, window):
        """ Se recibe una ficha y una ventana
        y se actualiza la ventana de manera tal
        que esa ficha invierta su estado: Si estaba
        boca arriba, estará boca abajo. Y al revés """
        k = self.get_key()
        if self._boca_arriba:
            self._boca_arriba = False
            window[k].Update(image_filename = (self._dorso))
            window[k].Update(text = ' ')
        else:
            self._boca_arriba = True
            window[k].Update(image_filename = (self._imagen))
            window[k].Update(text = self._nombre)
            
    def remover(self, window):
        """ Descarta una ficha del juego, dándola por encontrada
        y desabilitándola de continuar interactuando en la partida """
        k = self.get_key()
        window[k].Update(disabled = True)
        
    def get_nombre(self):
        return self._nombre
    def get_ID(self):
        return self._ID
    def get_key(self):
        return self.Key
    
class FichaImagen(Ficha):
    def __init__(self, nombre, ID, grupo, **extra_fields):
        """ Inicializa las propiedades del objeto, 
        presentes en su clase padre, mediante una 
        llamada a dicha clase """
        super().__init__(' ', ID, **extra_fields)
        self._nombre = nombre
        self._grupo = grupo
        self._imagen = carpeta_imagenes + grupo + os.sep + nombre + '.png'
    def get_grupo(self):
        return self._grupo
    def get_imagen(self):
        return self._imagen
    def darse_vuelta(self, window):
        """ Este método sirve de switch entre los dos estados de la ficha:
        boca arriba o boca abajo, y se vale de un boolean, alojado
        en la misma ficha, para tomar la decisión de cambiar al otro estado """
        k = self.get_key()
        if self._boca_arriba:
            self._boca_arriba = False
            window[k].Update(image_filename = (self._dorso))
        else:
            self._boca_arriba = True
            window[k].Update(image_filename = (self._imagen))

class FichaPalabra(Ficha):
    def __init__(self, nombre, ID, color, **extra_fields):
        """ Inicializa las propiedades del objeto, 
        presentes en su clase padre, mediante una 
        llamada a dicha clase """
        super().__init__(nombre, ID, **extra_fields)
        self._imagen = cpt_fondo_palabras + color + '.png'


class Timer():
    """ Esta clase sirve de padre a otra, e implementa
    metodos y variables que permiten el conteo y
    manipulación de relojes para el correcto conteo
    del tiempo transcurrido en distintos eventos """
    
    def __init__(self, tiempo):
        """ Inicializa las propiedades del objeto, 
        presentes en su clase padre, mediante una 
        llamada a dicha clase """
        self._paused = False
        self._tiempo_actual = 0
        self._tiempo_max = tiempo
        self._tiempo_pausado= 0
        self._tiempo_comienzo = self.tiempo_entero()
    
    def tiempo_entero(self):
        """ Retorna, en formato util, el tiempo
        actual obtenido de time.time """
        return int(round(time.time() * 100))

    def actualizar_tiempo (self):
        """ Actualiza el valor de la variable
        de partida '_tiempo_actual' mediante la resta
        de valores pertinentes"""
        self._tiempo_actual = self.tiempo_entero() - self._tiempo_comienzo

    def pausar_tiempo(self):
        """ Comienza el conteo del lapso
        de tiempo que el juego permanece pausado """
        self._tiempo_pausado = self.tiempo_entero()

    def reanudar_tiempo(self): 
        """ Toma el tiempo pausado y se lo resta al total
        de tiempo transcurrido para, de esa manera,
        constar correctamente el tiempo jugado """
        self._tiempo_comienzo = (self._tiempo_comienzo 
                                + self.tiempo_entero() ) - self._tiempo_pausado   
                           
    def get_tiempo_string(self):
        """ Devuelve, en formato String, dividido
        por : (dos puntos) el tiempo restante 
        de la partida """
        ahora = self.get_tiempo_actual()
        max = self.get_tiempo_max()
        minutos = str((max - ahora//100)//60)
        segundos = str((max - ahora//100)%60)
        segundos = ('0' + segundos) if len(segundos) == 1 else segundos
        if (int(minutos) < 0):
            return ('0:00')
        return (minutos + ':' + segundos)
    
    def cambiar_pausa(self):
        """ Switch de estados de la propiedad
        '_paused' de la partida, entre pausado
        y no pausado"""
        self._paused = not self._paused

    def resetear_tiempo(self):
        """ Vuelve los contadores de tiempo
        a 0, o similares, de manera tal de 
        resetear los conteos """
        self._tiempo_actual = 0
        self._tiempo_pausado = self.tiempo_entero() 
        self._tiempo_comienzo = self.tiempo_entero()

    def tiempo_restante(self):
        """ Devuelve un valor en segundos del
        tiempo restante de partida antes de
        finalizar por Timeout """
        ahora = self.get_tiempo_actual()
        max = self.get_tiempo_max()
        return int(max - ahora//100)
        
    def get_tiempo_max(self):
        return self._tiempo_max
    def get_tiempo_actual(self):
        return self._tiempo_actual
    def paused(self):
        """ Devuelve el estado de la propiedad '_paused' """
        return self._paused
    

class Partida(Timer):
    """ La clase Partida define todo lo que se muestra en la
    sección de fichas de la pantalla de juego, y guarda
    toda la información pertinente de la partida en juego.
    Al finalizar una partida, este objeto es tomado por
    otro módulo, como un gran paquete, de donde se extrae información
    para dar resultados sobre rankings """
    def __init__(self, dificultad, nivel, nivel_inicial, nivel_estatico, coincidencias, 
                 filas, columnas, tipo_ficha, tiempo, nick, siguiente): 
        """ Inicializa las propiedades del objeto, 
        presentes en su clase padre, mediante una 
        llamada a dicha clase """
        #Constantes
        super(Partida,self).__init__(tiempo)  #inicializo clase tiempo
        self._nick = nick
        self._tipo_ficha = tipo_ficha
        self._filas = filas
        self._columnas = columnas
        self._nivel = nivel
        self._nivel_inicial = nivel_inicial
        self._nivel_estatico = nivel_estatico
        self._coincidencias = coincidencias
        self._dificultad = dificultad
        self._siguiente = siguiente
        self.window = None #Se le asigna después de instanciada.
        #Variables
        self._puntos = 0
        self._turnos = 0
        self._intento = 0
        self._dadas_vuelta = {}
        self._dadas_vuelta_nombres = []
        self._elegidas = []
        self._encontradas = []
        self._lista_fichas = []
        self._grupos = int(int(filas * columnas) / coincidencias)
        self._info_fichas = crits.main()
        self._grupo_imagenes = ''
        if tipo_ficha == 'Imágenes':
            self._grupo_imagenes = self._info_fichas['tematica']
        self._palabras = self._obtener_palabras()
        self._fichas = self._de_lista_a_matriz(filas, columnas)
        self._tiempo_comienzo_turno = 0
        self._turno_empezado = False
        self._partida_terminada = False
        self._tiempo_final=True
        
    def _elegir_fichas(self):
        """ Mediante un set, se toman pruebas al azar de un pool
        de 14 elementos (en cualquier circunstancia son 14),
        hasta tener la cantidad necesaria para el nivel y
        dificultad actual, para la partida """
        elegidas_set = set()
        while len(elegidas_set) < self._grupos:
            elegidas_set.add(self._palabras[randrange(len(self._palabras))])
        for p in elegidas_set:
            self._elegidas.append(p)
        
    def _verificar_pares(self, nombre):
        """ Devuelve True si toda las fichas dadas
        vuelta son iguales, False de caso contrario """
        if self._lista_fichas.count(nombre[0]) < self._coincidencias:
            return True
        else:
            return False
    
    def _armar_tablero(self):
        """ Mediante diversos llamados, contruye
        la parte central de una partida, que es el
        tablero, el cuadrilátero donde se albergan
        las fichas. Construye una matriz de objetos
        de clase Ficha que es devuelta para su
        implementación en la ventana """
        tablero = []
        self._elegir_fichas()
        cant_fichas = (self._grupos * self._coincidencias)
        while (len(self._lista_fichas) < cant_fichas):
            nombre = sample(self._elegidas, 1)
            if self._verificar_pares(nombre):
                self._lista_fichas.append(nombre[0])
        col = self._columnas
        y, x = 0, 0
        ID = 0
        if self._tipo_ficha == 'Palabras':
            color = self._info_fichas['fondo']
            while len(self._lista_fichas) > 0:
                ficha = FichaPalabra(self._lista_fichas.pop(0), ID, color,
                                            key=(y, x), 
                                            button_color=('Black', 'Black'),
                                            border_width=3,
                                            size=(10,5))
                tablero.append(ficha)
                ID += 1
                x += 1
                if x >= col:
                    x = 0
                    y += 1
        else:                   #Imagenes
            grupo = self._grupo_imagenes
            while len(self._lista_fichas) > 0:
                ficha = FichaImagen(self._lista_fichas.pop(0), ID, grupo, 
                                            key=(y, x), 
                                            button_color=('Black', 'Black'),
                                            border_width=3,
                                            size=(10,5))
                tablero.append(ficha)
                ID += 1
                x += 1
                if x >= col:
                    x = 0
                    y += 1
        return tablero
                
    def _de_lista_a_matriz(self, alto, ancho):    
        """ Una vez elegidas las fichas y distribuidas de 
        manera aleatoria en el tablero, son guardadas en una lista.
        Este método recibe dicha lista y la transforma
        en una matriz, lista para insertar en la ventana """
        tablero = self._armar_tablero()
        
        fichas = [ [tablero.pop(0) for col in range (ancho) 
                    ] for row in range(alto)
                 ]
        return fichas
            
    def _obtener_palabras(self):
        """ Lee y procesa los archivos JSON necesarios
        para obtener la información acerca de qué juego
        de palabras o imagenes habrán de ser usadas
        para jugar, y devuelve dicho conjunto 
        de 14 elementos """
        palabras = []
        #Palabras
        if self._tipo_ficha == 'Palabras':
            path_json = (os.getcwd() + os.sep + 'data' + os.sep 
                         + 'datasets' + os.sep 
                         + self._info_fichas['archivo'] + '.json')
            #Si no existe el json, se manda a crear con el dataset 
            #(esto se hace solo si es necesario porque hay datasets muy pesados)
            if not os.path.isfile(path_json):
                genpal.main(self._info_fichas['funcion'])
            with open(f"{path_json}", "r", encoding = "latin-1") as archivo_palabras:
                data_json = json.load(archivo_palabras)    
            for i in data_json:
                palabras.append(i.get(self._info_fichas['palabra']))
        #Imágenes
        else:
            try:
                s = os.sep
                archivos = (os.listdir(os.getcwd() +s+ 'img' +s+ self._info_fichas['tematica'] +s))
                for a in archivos:
                    palabras.append(Path(a).stem)
            except(FileNotFoundError):
                print('Se deberán respetar los nombres de las '
                      + 'carpetas de imagenes tal cual estaban.')

        return palabras
       
    def terminar_partida(self):
        """ Finaliza el estado de la partida,
        para que ya no se ejecuten eventos
        de actualización """
        self._partida_terminada = True
    
    def partida_terminada(self):
        """ Devuelve el estado de la partida,
        True es que aún sigue en juego,
        False que ya no """
        return self._partida_terminada
    
    def actualizar_puntos(self):
        """ Actualiza la cantidad de puntos
        a mostrar en la ventana con el valor
        actual, modificado, de puntos """
        puntos = str(self.get_puntos())
        self.window['puntos'].Update("Puntos: " + puntos)
        self.window.refresh()
    
    def agregar_encontrada(self, nombre):
        """ Hace append a una lista con un nombre 
        recibido por parametro """
        self._encontradas.append(nombre)    
    def get_nick(self):
        return self._nick
    def set_tiempo(self, tiempo):
        self._tiempo = tiempo
    def get_puntos(self):
        return self._puntos
    def get_fichas(self):
        return self._fichas
    def get_columnas(self):
        return self._columnas
    def get_filas(self):
        return self._filas
    def get_intento(self):
        return self._intento
    def get_encontradas(self):
        return self._encontradas
    def get_dificultad(self):
        return self._dificultad
    def get_nivel(self):
        return self._nivel
    
    def inc_puntos(self, suma):
        """ Recibe una cantidad de puntos (puede ser negativa)
        y la aplica al total de puntos actuales de la partida.
        Si la suma redujera los puntos a menos de 0, en vez
        de tal, permanecen en 0 """
        if (self._puntos + suma) > 0:
            self._puntos += suma
        else:
            self._puntos = 0
        if ((not self.partida_terminada()) and (self.window != None)):
            self.actualizar_puntos()
    
    def desde_el_principio(self):
        """ Reinicia el nivel actual al nivel inicial
        decidido por el usuario en sus configuraciones """
        self._nivel = self._nivel_inicial
            
    def check_tiempo_turno(self):
        """ Verifica si hay fichas dadas vuelta, y si las hay
        (aunque sea una), comienza a contar un tiempo de time-out.
        En este caso, está seteado en 3. Si esos 3 segundos se
        terminan y el turno aún no, se termina abruptamente el turno
        con lo que eso implica """
        if ((len(self._dadas_vuelta) > 0) and (not self._turno_empezado)):
            self._tiempo_comienzo_turno = self._tiempo_actual
            self._turno_empezado = True
        elif ((self._turno_empezado)
              and ((self._tiempo_actual 
                   - self._tiempo_comienzo_turno) > 300)
              or (self._turno_empezado and len(self._dadas_vuelta)==0)):
            self.time_out_turno()
    
    def inc_intento(self, ficha):
        """ Chequea que la ficha clickeada no esté ya dada vuelta.
        De ser así, incrementa los intentos actuales (siendo el máximo
        equivalente a la cantidad de coincidencias del juego) y
        agrega el nombre de la nueva ficha a la una lista de
        'dadas vuelta' """
        if (ficha.get_ID() not in self._dadas_vuelta):
            self._intento += 1
            ficha.darse_vuelta(self.window)
            self._dadas_vuelta[ficha.get_ID()] = ficha
            self._dadas_vuelta_nombres.append(ficha.get_nombre())

    def time_out_turno(self):
        """ Resetea los valores del turno actual 
        a 0 o vacíos, para, de esa manera, finalizar
        el turno activo hasta el momento. """
        self._turno_empezado = False
        for objeto in self._dadas_vuelta.values():
            objeto.darse_vuelta(self.window)
        self._dadas_vuelta = {}
        self._dadas_vuelta_nombres = []
        self._turnos += 1
        self._intento = 0
        self.inc_puntos(-2)

    def fin_turno(self):
        """ Chequea si el turno se termina porque la cantidad de fichas
        es igual a la cantidad de coincidencias a encontrar.
        De ser así, devuelve True. Sino, si son menos, devuelve False """
        if self._intento == self._coincidencias:
            self._turnos += 1
            self._intento = 0
            self._turno_empezado = False
            return True
        else:
            return False
                
    def turno(self, fichas, y, x):
        """ Maneja llamados a metodos y toma decisiones
        para determinar el fin o continuidad del turno actual """
        ficha = fichas[y][x]
        self.inc_intento(ficha)
        if self.fin_turno():
            evento_intento = reg.Evento()
            evento_intento.tiempo = self.get_tiempo_string()
            evento_intento.cant_palabras = ((self._filas * self._columnas) 
                                            / self._coincidencias)
            evento_intento.nombre_evento = 'intento'
            evento_intento.nick = self._nick
            evento_intento.nivel = self._nivel
            evento_intento.dificultad = self._dificultad

            if (self._dadas_vuelta_nombres.count(ficha.get_nombre()) 
                                                == self._coincidencias):
                evento_intento.estado = 'correcto'
                evento_intento.palabra = ficha.get_nombre()

                for objeto in self._dadas_vuelta.values():
                    objeto.remover(self.window)
                self._encontradas.append(ficha.get_nombre())
                self.inc_puntos(10*self._coincidencias)
            else:
                evento_intento.estado = 'error'
                evento_intento.palabra = self._dadas_vuelta_nombres[0]

                self.inc_puntos(-1)
                sleep(0.4)
                for objeto in self._dadas_vuelta.values():
                    objeto.darse_vuelta(self.window)
            reg.evento_intento(evento_intento)
            self._dadas_vuelta = {}
            self._dadas_vuelta_nombres = []      
        
    def terminar_juego(self, mensaje = None, victoria=None):
        """ Da por finalizado el juego, luego de que se gane
        o pierda (esto es, tras pasar todos los niveles,
        o perder por tiempo), mostrando los mensajes
        adecuados y dirigiendo al usuario a la 
        ventana de puntajes, para ver su último resultado """
        config = funcs.get_info_usuario_actual()
        config['Configuración']['Nivel_actual'] = self._nivel_inicial
        funcs.actualizar_usuario(config)
        if mensaje != None:
            rojo = '#d91644'
            verde = '#10ae23'
            gris = '#343434'
            gris_verdoso = '#2d332d'
            gris_rojizo = '#332d2d'
            if victoria == True:
                sg.popup(mensaje, auto_close=True, auto_close_duration=4, 
                        line_width=50, no_titlebar=True, background_color=gris, 
                        text_color=verde, font=('Verdana', 14), button_type=5,
                        button_color=gris_verdoso, custom_text='Bien ahí :>')
            elif victoria == False:
                sg.popup(mensaje, auto_close=True, auto_close_duration=4, 
                        line_width=50, no_titlebar=True, background_color=gris, 
                        text_color=rojo, font=('Verdana', 14), button_type=5,
                        button_color=gris_rojizo, custom_text='Mal ahí :<')
        self.window.close()
        punt.main(self)

    def reiniciar_juego(self):
        """ Llamado por el botón en la Pantalla de Juego, este
        método vuelve a iniciar una partida desde cero y
        la deja a disposición del usuario para ser comenzada """
        self.window.close()
        sg.popup('Vamos de nuevo!', button_type=5, font=('Times New Roman', 20),
                 auto_close=True, auto_close_duration=1, no_titlebar=True,
                 background_color='Black', text_color='White')
        juego.main()
        
    def pasar_de_nivel(self):
        """ Carga la información del usuario
        actual y actualiza el valor de su nivel actual
        en 1 """
        if not self._nivel_estatico:
            info = funcs.get_info_usuario_actual()
            info['Configuración']['Nivel_actual'] += 1
            funcs.actualizar_usuario(info)
        punt.entrada_externa(self)
    
    def progreso_partida(self, y, x):
        """ Método principal al interactuar con fichas
        en el tablero. Chequea el fin de turno, de partida
        e incluso de juego, y toma las decisiones necesarias
        para que el juego haga lo esperado. Es un administrador
        de otros metodos más pequeños """
        fichas = self._fichas
        self.turno(fichas, y, x)
        config = funcs.get_info_usuario_actual()['Configuración']
        mensajes = config['Mensajes']
        dificultad  = config['Dificultad']
        nivel  = config['Nivel_actual']
        
        if len(self._encontradas) == self._grupos:
            puntos_extra = int(self.tiempo_restante())
            self.terminar_partida()
            self.inc_puntos(puntos_extra)
            sg.popup('Nivel completo')
            juego.evento_partida(self.get_tiempo_string(), self._filas, 
                                 self._columnas, self._coincidencias,
                                 self._nick, self._nivel, self._dificultad,
                                 'fin_partida', 'nivel_ganado')

            if ((dificultad == 'Fácil') and (int(nivel) < 3)
                or (dificultad == 'Normal') and (int(nivel) < 4)
                or (dificultad == 'Difícil') and (int(nivel) < 5)):
                    self.pasar_de_nivel()
                    self.window.close()
                    juego.main(True, self.get_puntos())
            else:
                juego.evento_partida(self.get_tiempo_string(), self._filas, 
                                     self._columnas, self._coincidencias,
                                     self._nick, self._nivel, self._dificultad,
                                     'fin_partida', 'partida_ganada')
                self.terminar_juego(mensajes['Victoria'], True)
    
    @staticmethod
    def mise_en_place():
        """ Este metodo llama a una función "get_info_usuario_actual" 
        que le devuelve la configuración del usuario actual, 
        y con dichos datos, se setean las variables locales de la partida,
        según los criterios elegidos por el jugador, 
        o bien los cargados por defecto """
        nick = funcs.get_nombre_usuario_actual()
        info = funcs.get_info_usuario_actual()['Configuración']
        tipo_ficha =        info['Fichas']
        dificultad =        info['Dificultad']
        nivel_inicial =     info['Nivel_inicial']
        nivel_estatico =    info['Nivel_estático']
        nivel =             info['Nivel_actual']

        if dificultad == 'Fácil':
            coincidencias = 2
            if nivel == 1:
                filas, columnas, tiempo = 3, 4, 120
            elif nivel == 2:
                filas, columnas, tiempo = 4, 4, 140
            else:
                filas, columnas, tiempo = 4, 5, 160

        elif dificultad == 'Normal':
            coincidencias = 3
            if nivel == 1:
                filas, columnas, tiempo = 3, 4, 100
            elif nivel == 2:
                filas, columnas, tiempo = 3, 5, 120
            elif nivel == 3:
                filas, columnas, tiempo = 4, 6, 140
            else:
                filas, columnas, tiempo = 5, 6, 180

        else:              #Difícil
            coincidencias = 3
            if nivel == 1:
                filas, columnas, tiempo = 3, 4, 80
            elif nivel == 2:
                filas, columnas, tiempo = 3, 5, 100
            elif nivel == 3:
                filas, columnas, tiempo = 3, 6, 140
            elif nivel == 4:
                filas, columnas, tiempo = 4, 6, 180
            else:
                filas, columnas, tiempo = 5, 6, 200

        return dificultad, nivel, nivel_inicial, nivel_estatico, coincidencias, filas, columnas, tipo_ficha, tiempo, nick
