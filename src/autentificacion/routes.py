#-------------------------------------------------------------------------------
# Name:        Rutas de autentificacion de AION
# Purpose:     Recopilar las rutas para acceder a los servicios
#               de autentificacion de AION.
#
# Author:      Aref
#
# Created:     9/10/2022
# Copyright:   (R) ACMUD 2022 / (k) Alta Lengua 2023 --
# Licence:     <GPLv3>
#-------------------------------------------------------------------------------

from . import Autentificacion_Blp
from ..controladores.usuario import UsuarioControlador
from ..utilidades.utilidades_web import get_obj_as_response

from flask import request
from flask_login import login_required

controlSesion = UsuarioControlador().realizadorAcciones

#configuracion de la ruta de registro /signup
@Autentificacion_Blp.route('/signup', methods=["POST"])
def signup():
    try:
        post = request.get_json()
        return controlSesion(request.url_rule.rule, postJson = post)
    except RuntimeError as rt: return get_obj_as_response(str(rt), 400)

#configuracion de la ruta de inicio de sesion /signin
@Autentificacion_Blp.route('/signin', methods=["POST"])
def signin():
    try:
        post = request.get_json()
        return controlSesion(request.url_rule.rule, postJson = post)
    except RuntimeError as rt: return get_obj_as_response(str(rt), 400)

#configuracion de la ruta de cierre de sesion /signout
@Autentificacion_Blp.route('/signout')
@login_required
def signout():
    try: return controlSesion(request.url_rule.rule)
    except RuntimeError as rt: return get_obj_as_response(str(rt), 400)