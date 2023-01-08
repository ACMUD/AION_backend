#-------------------------------------------------------------------------------
# Name:        Rutas de trazabilidad de AION
# Purpose:     Recopilar las rutas para acceder a los servicios
#               de trazabilidad de AION.
#
# Author:      Aref
#
# Created:     9-1/9/2022
# Copyright:   (R) ACMUD 2022 / (k) Alta Lengua 2023 --
# Licence:     <GPLv3>
#-------------------------------------------------------------------------------

""" Modulo: Rutas de trazabilidad de AION

Recopilar las rutas para acceder a los servicios de
trazabilidad de AION.

Recopila:
    Ruta Trazabilidad completa
    Ruta Trazabilidad colaboradores
"""

from flask import jsonify

from . import Trazabilidad_Blp
from .trazabilidad import obtener_trazabilidad

# Ruta: Trazabilidad completa
#configuracion de la ruta para ver el acerca de AION /about
@Trazabilidad_Blp.route('/about')
def about():
    retrum = {}
    retrum.update(obtener_trazabilidad("AION"))

    retrum["descriptores"] = []
    for descriptor in ["MAION", "VAION"]:
        retrum["descriptores"].append(obtener_trazabilidad(descriptor))

    retrum["colaboradores"] = about_us()[0].json
    return jsonify(retrum), 200

@Trazabilidad_Blp.route('/about/colaboradores')
def about_us():
    """ Ruta: Trazabilidad colaboradores

    Configuracion de la ruta para ver el acerca de los
    colaboradores de AION /about/colaboradores
    """
    retrum = []
    for colaborador in ["ACMUD", "AL", "Kairos", "IAN"]:
        retrum.append(obtener_trazabilidad(colaborador))

    return jsonify(retrum), 200