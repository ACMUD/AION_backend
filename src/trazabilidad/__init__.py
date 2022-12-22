#-------------------------------------------------------------------------------
# Name:        Blueprint de trazabilidad
# Purpose:     Recopilar los metodos para acceder a la
#               trazabilidad de AION, ACMUD y Alta Lengua.
#
# Author:      Aref
#
# Created:     9-1/9/2022
# Copyright:   (R) ACMUD 2022 / (k) Alta Lengua 2023 --
# Licence:     <GPLv3>
#-------------------------------------------------------------------------------

""" Paquete: Blueprint de trazabilidad (Bp_Trazabilidad)

Recopilar los metodos para acceder a la trazabilidad de AION,
ACMUD, Alta Lengua, y demás colaboradores o servicios.


    Modulo: Cabecera del paquete Bp_Trazabilidad

Genera el plano de aplicacion que contiene las funcionalidades
de trazabilidad.
"""

from flask import Blueprint

Trazabilidad_Blp = Blueprint('trazabilidad',__name__)

#importa las rutas de trazabilidad de AION
from . import routes