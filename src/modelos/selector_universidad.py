#-------------------------------------------------------------------------------
# Name:        Selector factoria universidad
# Purpose:     Selector que retorna una factoria abstracta
#               universidad.
#
# Author:      Aref
#
# Created:     19+9-1/9/2022
# Copyright:   (R) ACMUD 2022 / (k) Alta Lengua 2023 --
# Licence:     <GPLv3>
#-------------------------------------------------------------------------------

from .universidad import UniversidadFactoria
from .universidades.universidad_distrital import UniversidadDistritalFactoria

def selector_universidad(diminu: str) -> UniversidadFactoria:
    """ Funcion: Selector factoria universidad

    Funcion que retorna una factoria abstracta universidad con
    inicializacion peresoza en base a un argumento.

    El selector permite delegar la responsabilidad de creacion al
    cliente.

    Parametros:
        diminu (str) -- cadena que define la factoria que retorna
            el selector para instanciar

    Selectores:
        ud -- Universidad Distrital Francisco Jose de Caldas

    Retorno:
        una factoria abstracta universidad con inicializacion
            peresoza

    Excepciones:
        RuntimeError (El selector seleccionado no corresponde con
            ninguna factoria valida) -- si no existe una factoria
            que cumpla con la peticion
    """

    #inicializacion de selectores validos
    UD = 'ud'

    #condicional de factorias segun el selector
    if diminu.lower() == UD: return UniversidadDistritalFactoria
    raise RuntimeError("El selector seleccionado no corresponde con " +
        "ninguna factoria valida")