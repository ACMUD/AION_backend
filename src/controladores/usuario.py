#-------------------------------------------------------------------------------
# Name:        Usuario
# Purpose:     Controlador Usuario.
#
# Author:      Aref
#
# Created:     9/10/2022
# Copyright:   (R) ACMUD 2022 / (k) Alta Lengua 2023 --
# Licence:     <GPLv3>
#-------------------------------------------------------------------------------

from flask.wrappers import Response
from flask_login import current_user
from sqlalchemy import exc

from .controlador import Controlador
from ..config import config
from ..entidades.autentificacion.usuario import UsuarioEntidad
from ..utilidades.utilidades_db import (
        get_one_from_table_by_filter,
        add_record)

from ..utilidades.utilidades_sesion import generar_autentificacion_simbolica
from ..utilidades.utilidades_web import get_obj_as_response

class UsuarioControlador(Controlador):
    """ Clase: Controlador Usuario
        (Controlador)

    Objeto con el patron comando que representa un controlador
    de usuario. Sirve para recopilar los metodos disponibles para
    diferentes usuarios.
    """
    # Atributo concreto: Respuesta invalida
    respuesta_invalida = {"Respuesta invalida": # Fallo general
            'Controlador de sesion rechazo',

            "Parametros incorrectos": # Fallo si parametros inmanejables
            'Parametros suministrados son insuficientes para la solicitud',

            "Existe usuario": # Fallo si no debe existir un usuario
                #  pero existe
            'Se ha encontrado un usuario que coincide con los datos ' +
                'suministrados',

            "Respuesta vacia": # Fallo si hay carencia de respuesta
            'Solicitud de sesion devolvio una respuesta vacia',

            "Credenciales invalidas": # Fallo si las credenciales no
                #  son aceptadas
            'Al validar las credenciales suministradas no se hallaron ' +
                'coincidencias'
            }

    def realizadorAcciones(
            self,
            evento: str,
            **parametros: dict
            ) -> Response:
        """ Metodo concreto: Realizador acciones

        Metodo invocador que realiza una accion en base a un
        evento solicitud.

        Redirige los parametros del evento para que el cliente
        desconozca los detalles de los comandos. Cada comando
        crea un recibidor de los detalles y lo entrega al
        cliente.

        Parametros:
            evento (str) -- cadena que determina la solicitud de
                la vista
            **parametros (dict) -- parametros especificos para
                las acciones que el metodo comando ignora

        Referencia:
            (Response) -- el recibidor de los detalles realizados
                por el comando
        """
        #condicionales comando

        if evento == '/signup':
            #condicional detalles completos de la solicitud
            if (type(parametros) != dict or
                    'postJson' not in parametros):
                #recibidor por si errores
                return get_obj_as_response(
                        self._getSubRespuestas([
                                'Parametros incorrectos',
                                'Respuesta invalida']),406)

            #recibidor del comando
            return self._doSignUp(parametros)

        if evento == '/signin':
            #condicional detalles completos de la solicitud
            if (type(parametros) != dict or
                    'postJson' not in parametros):
                #recibidor por si errores
                return get_obj_as_response(
                        self._getSubRespuestas([
                                'Parametros incorrectos',
                                'Respuesta invalida']),406)

            #recibidor del comando
            return self._doSignIn(parametros)

        if evento == '/signout': return self._doSignOut()

        #recibidor por si error del comando
        return get_obj_as_response(
                self._getSubRespuestas(['Respuesta invalida']),406)

    @staticmethod
    def _getSubRespuestas(seleccion: list) -> dict:
        """ Metodo: Obtener algunas respuestas

        Metodo que retorna un conjunto disminuido de respuestas
        seleccionadas.

        Parametros:
            seleccion (list) -- lista de nombres con las
                respuestas seleccionadas

        Retorno:
            un diccionario con las respuestas invalidas

        Excepciones:
            KeyError -- si alguna respuesta invalida solicitada
                es incorrecta
        """
        try:
            return {l: __class__.respuesta_invalida[l]
                for l in seleccion}

        except KeyError as k:
            return {"Respuesta ajena":
                    __class__.respuesta_invalida['Respuesta ajena']}

    # Metodo concreto y de clase: Obtener lista de eventos
    @staticmethod
    def getEventList() -> list:
        return ['/signup',
            '/signin',
            '/signout']

    @staticmethod
    def _checkExistence(parametros: dict) -> UsuarioEntidad:
        """ Metodo de clase: Verificar existencia usuario

        Metodo que verifica si un usuario existe en base a los
        parametros y lo retorna o retorna nulo en otro caso.
        """
        usr = None #retorno por defecto

        #condicional en los parametros hay un apodo para buscar
        if 'apodo' in parametros:
            try:
                usr = get_one_from_table_by_filter(
                        UsuarioEntidad,
                        UsuarioEntidad.usur_apodo,
                        parametros['apodo'])

            except exc.SQLAlchemyError as SQL:
                print(SQL) #excepcion capturada y depurada

        #condicional en los parametros hay un correo para buscar
        if 'correo' in parametros:
            try:
                usr = get_one_from_table_by_filter(
                        UsuarioEntidad,
                        UsuarioEntidad.usur_correo,
                        parametros['correo'])

            except exc.SQLAlchemyError as SQL:
                print(SQL) #excepcion capturada y depurada

        return usr

    @staticmethod
    def _doSignUp(parametros: dict) -> Response:
        """ Metodo de clase: Registrar usuario

        Metodo que registra un usuario si todos los parametros
        son validos.

        Parametros:
            parametros (dict) -- diccionario de parametros para
                el comando, el diccionario debe contener los
                parametros para construir un usuario [ver
                UsuarioEsquema.claves()]

        Excepciones:
            KeyError -- si una llave para crear el usuario no es
                valida
            TypeError -- si una llave para crear el usuario no es
                valida
            exc.SQLAlchemyError -- si la conexion al almacenar el
                usuario falla
        """
        #comprobar existencia
        usr = __class__._checkExistence(parametros['postJson'])

        #condicional existe el usuario
        if usr:
            return get_obj_as_response(
                    __class__._getSubRespuestas([
                        'Existe usuario',
                        'Respuesta invalida']),
                    412)

        #trata de instanciar el usuario
        try: usr = UsuarioEntidad(**parametros['postJson'])

        except (KeyError,TypeError) as kt:
            print(kt) #excepcion capturada y depurada
            return get_obj_as_response(
                    __class__._getSubRespuestas([
                        'Parametros incorrectos',
                        'Respuesta invalida']),
                    406)

        #trata de almacenar el usuario
        try: usr.crear_usuario()

        except SQLAlchemyError as SQL:
            print(SQL) #excepcion capturada y depurada
            return get_obj_as_response(
                    __class__._getSubRespuestas([
                        'Respuesta invalida']),
                    400)

        #pasa todos los pasos, entonces registra el usuario
        return get_obj_as_response(
                {"Respuesta":
                f'El usuario ha sido registrado'},
                201)

    @staticmethod
    def _doSignIn(parametros: dict) -> Response:
        """ Metodo de clase: Iniciar sesion

        Metodo que inicia sesion si todos los parametros son
        validos.

        Parametros:
            parametros (dict) -- diccionario de parametros para
                el comando, el diccionario debe contener la llave
                `clave`, que corresponde a la clave de un usuario
                para iniciar la sesion, y alguna de las llaves
                `correo` o `apodo`, que corresponden a algun
                identificador del usuario para iniciar la sesion

        Excepciones:
            exc.SQLAlchemyError -- si la conexion al actualizar
                el usuario o al buscarlo falla
            Exception -- si la conexion al actualizar el usuario
                o al buscarlo falla
            AttributeError -- si no se obtiene un usuario al
                buscarlo
            KeyError -- si los parametros suministrados no sirven
                para iniciar sesion
        """
        try:
            #comprobar existencia
            usr = __class__._checkExistence(parametros['postJson'])

            #condicional no se encuentra usuario o la clave no corresponde al
            # encontrado
            if (not usr or
                    not usr.chequear_clave(parametros['postJson']['clave'])):
                return get_obj_as_response(
                    __class__._getSubRespuestas([
                        'Credenciales invalidas']),
                    412)

            #genera el identificador simbolico
            simbolismo = generar_autentificacion_simbolica(
                    usr.usur_apodo, #codifica el apodo como sujeto simbolico
                    config['duracion_simbolismo'])

            #condicional el simbolismo fue generado
            if simbolismo:
                #inicia sesion en el usuario y lo actualiza
                usr.iniciar_sesion()
                add_record(usr)

                return get_obj_as_response(
                    {"Respuesta": 'Sesion iniciada',
                    "Simbolismo": simbolismo},
                    200)

            #opcional el simbolismo no fue generado
            else:
                return get_obj_as_response(
                    __class__._getSubRespuestas([
                        'Respuesta vacia']),
                    412)

        except (exc.SQLAlchemyError,Exception) as SQLe:
            print(SQLe) #excepcion capturada y depurada
            return get_obj_as_response(
                    __class__._getSubRespuestas([
                        'Respuesta invalida']),
                    400)

        except AttributeError as a: #excepcion capturada
            return get_obj_as_response(
                    __class__._getSubRespuestas([
                        'Respuesta vacia',
                        'Respuesta invalida']),
                    412)

        except KeyError as kt:
            print(kt) #excepcion capturada y depurada
            return get_obj_as_response(
                    __class__._getSubRespuestas([
                        'Parametros incorrectos',
                        'Respuesta invalida']),
                    406)

    @staticmethod
    def _doSignOut() -> Response:
        """ Metodo de clase: Cerrar sesion

        Metodo que cierra sesion en el usuario actual y lo
        actualiza.
        """
        #cierra sesion en el usuario actual y lo actualiza
        current_user.cerrar_sesion()
        add_record(current_user)

        return get_obj_as_response({"Respuesta": 'Sesion cerrada'},200)