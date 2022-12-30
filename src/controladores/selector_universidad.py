#-------------------------------------------------------------------------------
# Name:        Selector controlador universidad
# Purpose:     Selector que retorna uncontrolador universidad.
#
# Author:      Aref
#
# Created:     19+9-1/9/2022
# Copyright:   (R) ACMUD 2022 / (k) Alta Lengua 2023 --
# Licence:     <GPLv3>
#-------------------------------------------------------------------------------

from .db import DBControlador
from .universidad import UniversidadControlador
from .universidades.universidad_distrital import UniversidadDistritalControlador

from typing import Union

def selector_universidad(criterio: str) -> UniversidadControlador:
    """ Funcion: Selector controlador universidad

    Funcion que retorna un controlador de universidad con
    inicializacion peresoza en base a un argumento.

    El selector permite delegar la responsabilidad de creacion al
    cliente.

    Parametros:
        criterio (str) -- cadena que define el controlador que
            retorna el selector para instanciar

    Selectores:
        <id> -- identificador del registro de la universidad en
            la base de datos
        ud -- Universidad Distrital Francisco Jose de Caldas

    Retorno:
        un controlador universidad con inicializacion peresoza

    Excepciones:
        RuntimeError (El criterio seleccionado no corresponde con
            ningun controlador valido) -- si no existe un
            controlador que cumpla con la peticion
    """
    #condicional reconocer un id
    if criterio.isnumeric():
        #obtener el diminutivo para el id
        # no informa si el id no existe
        diminu = DBControlador().realizadorAcciones(
                '/universidad/<idU>/diminutivo',
                idU = criterio).json

    #opcional no es un id
    else: diminu = criterio.lower()

    #inicializacion de selectores validos
    UD = 'ud'

    #condicional de controladores segun el selector
    if diminu == UD: return UniversidadDistritalControlador
    raise RuntimeError("El criterio seleccionado no corresponde con " +
        "ningun controlador valido")