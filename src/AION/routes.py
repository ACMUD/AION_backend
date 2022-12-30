#-------------------------------------------------------------------------------
# Name:        Rutas de servicios de AION
# Purpose:     Recopilar las rutas para acceder a los servicios
#               de AION backend.
#
# Author:      Aref
#
# Created:     1/1+9/2022
# Copyright:   (R) ACMUD 2022 / (k) Alta Lengua 2023 --
# Licence:     <GPLv3>
#-------------------------------------------------------------------------------

""" Modulo: Rutas de servicios de AION

Recopilar las rutas para acceder a los servicios de AION backend.

Recopila:
    Ruta
"""

from . import AION_Blp
from ..controladores.db import DBControlador
from ..controladores.selector_universidad import selector_universidad
from ..utilidades.utilidades_web import get_obj_as_response

import json
import requests
from flask import jsonify, request, url_for, current_app

controlDB = DBControlador().realizadorAcciones

# configuracion de la ruta que devuelve todas las universidades
#  /universidades
@AION_Blp.route('/universidades')
def us():
    try: return controlDB(request.url_rule.rule)
    except RuntimeError as rt: return get_obj_as_response(str(rt), 400)

# configuracion de la ruta que devuelve una universidad por su id
#  /universidad/<idU>
@AION_Blp.route('/universidad/<idU>')
def univ(idU):
    print(request.url_rule.rule)
    try: return selector_universidad(idU)().realizadorAcciones(
            request.url_rule.rule)
    except RuntimeError as rt: return get_obj_as_response(str(rt), 406)

# configuracion de la ruta que devuelve el diminutivo de una universidad
#  por su id /universidad/<idU>/diminutivo
@AION_Blp.route('/universidad/<idU>/diminutivo')
def univ_diminu(idU):
    try: return selector_universidad(idU)().realizadorAcciones(
            request.url_rule.rule)
    except RuntimeError as rt: return get_obj_as_response(str(rt), 406)

# configuracion de la ruta que devuelve la cabecera de una universidad
#  por su id o diminutivo /universidad/<idU>/cabecera
@AION_Blp.route('/universidad/<idU>/cabecera')
def univ_cabecera(idU):
    try: return selector_universidad(idU)().realizadorAcciones(
            request.url_rule.rule)
    except RuntimeError as rt: return get_obj_as_response(str(rt), 406)

# configuracion de la ruta que devuelve una universidad como recurso
#  por su id /universidad/preview/<idU>
@AION_Blp.route('/universidad/<idU>/preview')
def univ_preview(idU):
    try: return selector_universidad(idU)().realizadorAcciones(
            request.url_rule.rule)
    except RuntimeError as rt: return get_obj_as_response(str(rt), 406)

# configuracion de la ruta que devuelve las facultades de una universidad
#  por su id /universidad/<idU>/facultades
@AION_Blp.route('/universidad/<idU>/facultades')
def univ_facultades(idU):
    try: return selector_universidad(idU)().realizadorAcciones(
            request.url_rule.rule)
    except RuntimeError as rt: return get_obj_as_response(str(rt), 406)

# configuracion de la ruta que devuelve los proyectos curriculares de una
#  universidad por su id /universidad/<idU>/proyectos
@AION_Blp.route('/universidad/<idU>/proyectos')
def univ_proyectos(idU):
    try: return selector_universidad(idU)().realizadorAcciones(
            request.url_rule.rule)
    except RuntimeError as rt: return get_obj_as_response(str(rt), 406)

def filtro_horario(idU:int, codMat:int = None, idGrup:str = None) -> dict:
    diminu = univ_diminu(idU)
    with open(f'src\\archivos\\{diminu}\\{diminu}' +
              f'{univ_cabecera_str(diminu)}.json') as horario_file:
        horario_dict = json.load(horario_file)
        if not codMat: return horario_dict
        else:
            try:
                if not idGrup: return horario_dict[codMat]
                else: return horario_dict[codMat][idGrup]
            except:
                return []

# configuracion de la ruta que devuelve todos los horarios de una
#  universidad por su id /universidad/<idU>/horarios
@AION_Blp.route('/universidad/<idU>/horarios')
def univ_horarios(idU):
    try: return selector_universidad(idU)().realizadorAcciones(
            request.url_rule.rule)
    except RuntimeError as rt: return get_obj_as_response(str(rt), 406)

# configuracion de la ruta que devuelve los horarios de una materia
#  por el id de su universidad y su codigo de materia
#  /universidad/<idU>/horarios/codigo/<codMat>
@AION_Blp.route('/universidad/<idU>/horarios/codigo/<codMat>')
def univ_materia_horarios(idU, codMat):
    try: return selector_universidad(idU)().realizadorAcciones(
            request.url_rule.rule, codMat = codMat)
    except RuntimeError as rt: return get_obj_as_response(str(rt), 406)

# configuracion de la ruta que devuelve el horario de una materia
#  por el id de su universidad, su codigo de materia y su id de grupo
#  /universidad/<idU>/horarios/codigo/<codMat>/grupo/<idGrup>
@AION_Blp.route('/universidad/<idU>/horarios/codigo/<codMat>/' +
        'grupo/<idGrup>')
def univ_materia_horario(idU, codMat, idGrup):
    try: return selector_universidad(idU)().realizadorAcciones(
            request.url_rule.rule, codMat = codMat, idGrupo = idGrup)
    except RuntimeError as rt: return get_obj_as_response(str(rt), 406)