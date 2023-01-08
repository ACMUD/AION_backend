#-------------------------------------------------------------------------------
# Name:        Utilidades Sesion
# Purpose:     Presentar metodos comunes para la gestion de
#               sesiones con identificacion simbolica a traves de
#               cabeceras.
#
# Author:      Aref
#
# Created:     9/10/2022
# Copyright:   (R) ACMUD 2022 / (k) Alta Lengua 2023 --
# Licence:     <GPLv3>
#-------------------------------------------------------------------------------

""" Modulo: Utilidades Sesion

Presentar metodos comunes para la gestion de sesiones con
identificacion simbolica a traves de cabeceras.

Recopila:
    Funcion Trocear clave
    Funcion Chequear clave
    Funcion Generar simbolismo
    Funcion Chequear simbolismo
"""

from flask_bcrypt import Bcrypt
from typing import Union
import datetime
import jwt

from ..config import config

def trocear_clave(clave: str) -> str:
    """ Funcion: Trocear clave

    Funcion que retorna una clave encriptada con un algoritmo
    picadillo.

    Parametros:
        clave (str) -- una clave desencriptada

    Retorno:
        una clave encriptada
    """
    return Bcrypt().generate_password_hash(
            clave,config['iteraciones']).decode()

def chequear_clave(clave: str, clave_troceada: str) -> bool:
    """ Funcion: Chequear clave

    Funcion que verifica que una clave encriptada pueda ser
    generada por una clave desencriptada.

    Parametros:
        clave (str) -- una clave desencriptada
        clave_troceada (str) -- una clave encriptada

    Retorno:
        valor de verdad si la clave desencriptada puede generar
            la clave encriptada
    """
    return Bcrypt().check_password_hash(clave_troceada,clave)

def generar_autentificacion_simbolica(
            apodo: str,
            vencimiento_en: dict = {'minutes': 1}
            ) -> str:
    """ Funcion: Generar simbolismo

    Funcion que retorna un simbolismo de autentificacion en base
    a un apodo y con un tiempo de expirado.

    Parametros:
        apodo (str) -- un apodo que permita la identificacion
            posterior de un usuario
        vencimiento_en (dict) [{'minutes': 1}] -- diccionario con
            datos de tiempo de vencimiento

    Retorno:
        simbolismo de autentificacion
    """
    cartucho = {
        'exp': datetime.datetime.utcnow() +
            datetime.timedelta(**vencimiento_en),
        'iat': datetime.datetime.utcnow(),
        'sub': apodo
    }

    return jwt.encode(
        cartucho,
        config['clave_secreta'],
        algorithm='HS256')

def chequear_autentificacion_simbolica(simbolismo: str) -> Union[str,None]:
    """ Funcion: Chequear simbolismo

    Funcion que recibe un simbolismo de autentificacion y si es
    valido retorna el sujeto asociado al simbolismo, de lo
    contrario retorna un valor nulo.

    El simbolismo es invalido si no es decodificable o si el
    tiempo de expirado ha caducado.

    Parametros:
        simbolismo (str) -- un simbolismo de autentificacion

    Retorno:
        el sujeto asociado al simbolismo si este es valido o nulo
            de otro modo

    Excepciones:
        jwt.ExpiredSignatureError -- si el tiempo de expirado del
            simbolismo ha caducado
        jwt.InvalidTokenError -- si el simbolismo no se puede
            decodificar
    """
    try:
        cartucho = jwt.decode(
                simbolismo,
                config['clave_secreta'],
                algorithms='HS256')

        return cartucho['sub']

    except jwt.ExpiredSignatureError as JWTes:
        print(JWTes)

    except jwt.InvalidTokenError as JWTit:
        print(JWTit)