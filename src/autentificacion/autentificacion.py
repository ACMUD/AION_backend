#-------------------------------------------------------------------------------
# Name:        Servicios de autentificacion de AION
# Purpose:     Recopilar los servicios del modulo interno de
#               autentificacion. Los servicios se agregan al
#               gestor de sesion para las rutas que los invoquen.
#
# Author:      Aref
#
# Created:     9/10/2022
# Copyright:   (R) ACMUD 2022 / (k) Alta Lengua 2023 --
# Licence:     <GPLv3>
#-------------------------------------------------------------------------------

""" Modulo: Servicios de autentificacion de AION

Recopilar los servicios del modulo interno de autentificacion.
Los servicios se agregan al gestor de sesion para las rutas que
los invoquen.

Recopila:
    Funcion Cargar usuario desde una peticion
    Funcion Gestor intrusiones
    Funcion Requiere ser administrador
"""

from . import gestor_sesion
from ..entidades.autentificacion.usuario import UsuarioEntidad
from ..utilidades.utilidades_db import get_one_from_table_by_filter
from ..utilidades.utilidades_sesion import chequear_autentificacion_simbolica
from ..utilidades.utilidades_web import get_obj_as_response

from flask import request
from flask.wrappers import Response
from flask_login import current_user, UserMixin
from functools import wraps

#configuracion del cargador por peticion del gestor de sesion
@gestor_sesion.request_loader
def cargar_desde_solicitud(peticion: request) -> UserMixin:
    """ Funcion: Cargar usuario desde una peticion

    Funcion que recibe una peticion y carga la sesion de
    autentificacion desde el encabezado.

    Actualmente permite:
        Desde la cabecera:
            Con un poseedor simbolico (Bearer JSON Web Token)

    Parametros:
        peticion (request) -- una peticion al servidor

    Retorno:
        un objeto usuario utilizado por la libreria flask-login
            para autenticar al usuario
    """
    #registra la cabecera en busqueda de la informacion de autorizacion
    autentificacion = peticion.headers.get('Authorization', '').split(' ')

    #extraer el simbolismo
    # condicional no hay simbolismo para extraer
    if len(autentificacion) != 2: simbolismo = ''

    # opcional hay simbolismo para extraer
    else: simbolismo = autentificacion[1]

    #condicional no se extrajo el simbolismo
    if not simbolismo:
        print('Provea datos para la autorizacion en la solicitud.')
        return None

    #verifica que el simbolismo sea legible y aun no expire
    usr_apodo = chequear_autentificacion_simbolica(simbolismo)

    #busca al usuario sujeto del simbolismo
    usr = get_one_from_table_by_filter(
            UsuarioEntidad,
            UsuarioEntidad.usur_apodo,
            usr_apodo)

    #condicional no existe el usuario o no esta registrado
    if not usr:
        print('El identificador del usuario no se encuentra registrado.')
        return None

    #condicional varifica que el usuario haya iniciado sesion
    if not usr.usur_esta_sesion:
        print('La sesion del usuario se ha cerrado.')
        return None

    return usr #carga el usuario

#configuracion del gestor de intrusiones del gestor de sesion
@gestor_sesion.unauthorized_handler
def gestor_intrusos() -> Response:
    """ Funcion: Gestor intrusiones

    Funcion que gestiona los accesos no autorizados (o
    intrusiones) en sesion.

    Retorno:
        una respuesta del servidor para informar la falta de
            autentificacion
    """
    return get_obj_as_response({"Respuesta": 'Acceso no autorizado'},401)

def requiere_admin():
    """ Funcion: Requiere ser administrador

    Funcion que decora rutas para que requieran de una sesion de
    administrador iniciada.
    """
    #En versiones posteriores el decorador puede ser despreciado, y ser
    # reemplazada por un decorador con un parametro que determine el rol
    # requerido
    def decorator(f):
        @wraps(f)
        def wrapper(**args):
            #condicional es administrador, retorna la funcion
            if current_user.usur_es_administrador: return f(**args)

            #retorno por defecto, gestor intrusiones
            return gestor_intrusos()

        return wrapper

    return decorator