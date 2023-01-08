#-------------------------------------------------------------------------------
# Name:        Creador de JSON Universidad Distrital
# Purpose:     Servir de recopilacion de algoritmos de creacion
#               de JSON para la Universidad Distrital. Cada
#               creador sirve de clase concreta del metodo
#               factoria selector_creador_UD y se especializa en
#               un tipo de origen de datos para la creacion del
#               JSON.
#
# Author:      Tatterdemalion
#
# Created:     19+9-1/9/2022
# Copyright:   (R) ACMUD 2022 / (k) Alta Lengua 2023 --
# Licence:     <GPLv3>
#-------------------------------------------------------------------------------

""" Modulo: Creador de JSON Universidad Distrital

Servir de recopilacion de algoritmos de creacion de JSON para la
Universidad Distrital. Cada creador sirve de clase concreta del
metodo factoria selector_creador_UD y se especializa en un tipo
de origen de datos para la creacion del JSON.

Referencia:
    crear_JSON (callable)
    almacenador (AlmacenadorJSONUD)

Recopila:
    Clase Creador de JSON por PDF
    Clase Creador de JSON por XML
"""

from ..universidad_distrital import CreadorJSONUD, AlmacenadorJSONUD
from ....config import config

class CreadorJSONUDByPDF(CreadorJSONUD):
    """ Clase: Creador de JSON por PDF
        (CreadorJSONUD)

    Objeto que sirve de clase concreta del metodo factoria
    selector_creador_UD y representa un Creador de JSON
    especializado en el tipo de origen de datos de ficheros PDF
    accesibles en el Sistema de Gestion Academica (CONDOR).
    """
    def __init__(self, almacenador: AlmacenadorJSONUD):
        CreadorJSONUD.__init__(self, almacenador)
        self.datos = {}

    def procesar_pag(self, texto: str):
        lineas = texto.splitlines()
        encabs = [] # encabezados para los datos
        ind_cargn = [True, 0] # indicador de carga
                    # [0]: bool si se estan cargando los encabezados
                    # [1]: posicion en donde insertar los (encabezados/datos)

        ind_v_h = True # indicador de proceso vertical u horizontal
                # True: almacenado horizontal; False: vertical

        for linea in lineas:
            palbrs = linea.split() # todas las palabras de la linea
            palbr_comp = '' # almacena dato palabra a palabra hasta
                            #  que deba almacenarse

            for num_palb, palb in enumerate(palbrs):

                # ind_v_h cambia unicamente con las palabras cod.,
                #  grp. o proyecto
                if palb.lower() in ["cod.","grp.","proyecto"]:
                  ind_v_h = palb.lower() != "cod." # cuando grp. pasa a horizntl

                  # se reinician los indicadores
                  encabs = []
                  ind_cargn = [True, 0]

                palbr_comp += palb + ' '

                # agrega un encabezado si lo encuentra y
                #  si esta cargando los encabezados
                if ind_cargn[0] and palbr_comp.lower()[:-1] in self.campos:
                    encabs.append(palbr_comp.lower()[:-1])
                    palbr_comp = ''

                    # si ademas esta al final de una linea o esta en
                    #  modo horizntl, deja de cargar los encabezados
                    if ind_v_h or num_palb == len(palbrs) - 1:
                        ind_cargn = [False, 0]

                # agrega datos
                # ----
                #  si esta en vertical y ya cargo los encabezados
                if not ind_v_h and not ind_cargn[0]:

                    # agrega la ultima palabra como dato si la posicion
                    #  del indicador esta en 0 o 3
                    if ind_cargn[1] in [0,3]:

                        # si una linea no inicia con un codigo numerico o
                        #  con proyecto, se la salta
                        if (ind_cargn[1] == 0 and
                            not palbr_comp[:-1].isnumeric() and
                            not palb == "proyecto"): break

                        #agrega el dato y avanza el indicador
                        self.datos[encabs[ind_cargn[1]]] = palb
                        ind_cargn[1] += 1
                        palbr_comp = ''

                    # agrega unas palabras como datos si la posicion del
                    #  indicador esta en 1 y encuentra un dia
                    elif ind_cargn[1] == 1 and palb.lower() in self.dias:

                        # agrega todo lo que no es un dia y avanza
                        palbr_comp = palbr_comp.replace(palb,"")
                        self.datos[encabs[ind_cargn[1]]] = palbr_comp[:-2]
                        ind_cargn[1] += 1
                        palbr_comp = ''

                        # agrega el dia y avanza
                        self.datos[encabs[ind_cargn[1]]] = palb
                        ind_cargn[1] += 1

                    # agrega las ultimas palabras como datos si la posicion
                    #  del indicador esta en 4 y esta al final de la linea
                    elif ind_cargn[1] == 4 and num_palb == len(palbrs) - 1:
                        self.datos[encabs[ind_cargn[1]]] = palbr_comp
                        ind_cargn = [False, 0]
                        self.almacenador.agregar(self.datos)
                # ----
                #  si esta en horizontal
                else:

                    # agrega la ultima palabra completa si ya cargo los
                    #  encabezados y esta al final de la linea
                    if not ind_cargn[0] and num_palb == len(palbrs) - 1:
                        self.datos[encabs[-1]] = palbr_comp[:-1]
                        ind_cargn = [True, 0]

    # Metodo concreto: Crear JSON
    def crear_JSON(self):
        import pdfplumber as miner
        self.almacenador.inicializar()

        #trata de alcanzar el fichero para actualizar los horarios
        try:
            with miner.open(
                    config["directorio_carga"] +
                    r'\..\ud\submission.pdf') as pdf:
                for num_pag in range(len(pdf.pages)):
                    self.procesar_pag(pdf.pages[num_pag].extract_text())

        except FileNotFoundError:
            raise FileNotFoundError #excepcion capturada y lanzada

        self.almacenador.finalizar()

# Clase: Creador de JSON por XML (CreadorJSONUD)
class CreadorJSONUDByXML(CreadorJSONUD):
    # Metodo concreto: Crear JSON
    def crear_JSON(self): pass