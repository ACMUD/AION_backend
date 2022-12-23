#-------------------------------------------------------------------------------
# Name:        Selector creador de JSON
# Purpose:     Recopilar los selectores de creadores de JSON de
#               diferentes universidades.
#
# Author:      Tatterdemalion
#
# Created:     19+9-1/9/2022
# Copyright:   (R) ACMUD 2022 / (k) Alta Lengua 2023 --
# Licence:     <GPLv3>
#-------------------------------------------------------------------------------

""" Modulo: Selector creador de JSON

Recopilar los selectores de creadores de JSON de diferentes
universidades, pertenecientes a la familia de clases de cada
universidad. Cada selector sigue el patron metodo factoria,
recibiendo un parametro que identifica el origen de los datos y
retorna un creador de JSON con inicializacion peresoza.

Referencia:
    selector_creador_* (callable -> CreadorJSONUD) -- metodo para
        obtener un creador de JSON en base a un origen de datos
"""

from .universidad_distrital import CreadorJSONUD
from .creadores_JSON.creadores_UD import *

def selector_creador_UD(origen: str) -> CreadorJSONUD:
    """ Funcion: Selector creador de JSON UD

    Funcion que retorna un creador de JSON para la universidad
    distrital con inicializacion peresoza en base a un origen de
    datos.

    Parametros:
        origen (str) -- cadena que define el creador de JSON que
            retorna el selector para instanciar

    Selectores:
        pdf -- archivo PDF accesible en el Sistema de Gestion
            Academica (CONDOR)
        xml -- archivo XML accesible a traves de endpoints del
            Sistema de Gestion Academica (CONDOR)

    Retorno:
        un creador de JSON para la universidad distrital con
            inicializacion peresoza

    Excepciones:
        RuntimeError (El selector seleccionado no corresponde con
            ningun creador de JSON valido) -- si no existe un
            creador de JSON que cumpla para el origen de datos
    """

    #inicializacion de selectores validos
    PDF = 'pdf'
    XML = 'xml'

    #condicional de factorias segun el selector
    if origen.lower() == PDF: return CreadorJSONUDByPDF
    if origen.lower() == XML: return CreadorJSONUDByXML
    raise RuntimeError("El selector seleccionado no corresponde con " +
        "ningun creador de JSON valido")