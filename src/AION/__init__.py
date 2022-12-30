#-------------------------------------------------------------------------------
# Name:        Blueprint de servicios de AION ("servidor de quien
#               lo use" --)
# Purpose:     Recopilar los metodos para acceder a los servicios
#               de organizacion tipo Kairos de AION.
#
# Author:      Aref
#
# Created:     1/1+9/2022
# Copyright:   (R) ACMUD 2022 / (k) Alta Lengua 2023 --
# Licence:     <GPLv3>
#-------------------------------------------------------------------------------

""" Paquete: Blueprint de servicios de AION (Bp_AION)

Recopilar los metodos para acceder a los servicios de
organizacion tipo Kairos de AION.


    Modulo: Cabecera del paquete Bp_AION

Genera el plano de aplicacion que contiene las funcionalidades
de servicios de AION.
"""

from flask import Blueprint

AION_Blp = Blueprint('AION',__name__)

#importa las rutas de trazabilidad de AION
from . import routes