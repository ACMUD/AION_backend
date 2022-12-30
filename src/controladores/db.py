#-------------------------------------------------------------------------------
# Name:        Conexion URI
# Purpose:     Controlador Conexion URI.
#
# Author:      Aref
#
# Created:     1/1+9/2022
# Copyright:   (R) ACMUD 2022 / (k) Alta Lengua 2023 --
# Licence:     <GPLv3>
#-------------------------------------------------------------------------------

from .controlador import Controlador
from ..entidades.horario.universidad import (
        UniversidadEntidad,
        UniversidadEsquema)
from ..utilidades.utilidades_db import (
        get_all_from_table,
        get_one_from_table_by_filter)
from ..utilidades.utilidades_web import get_obj_as_response

from flask import jsonify, make_response
from flask.wrappers import Response

class DBControlador(Controlador):
    """ Clase: Controlador Conexion URI
        (Controlador)

    Objeto con el patron comando que representa un controlador de
    los comandos realizados a la base de datos.
    """
    # Atributo concreto: Respuesta invalida
    respuesta_invalida = {"Respuesta invalida": # Fallo general
            'Conexion a base de datos rechazada',
            "Respuesta vacia": # Fallo si hay carencia de respuesta
            'Conexion a base de datos devolvio una respuesta vacia'}

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

        if evento == '/universidades': return self._getUniversidades()

        if evento == '/universidad/<idU>/diminutivo':
            return self._getDiminutivoUniversidad(parametros)

        #recibidor por si error del comando
        return get_obj_as_response(
                self._getSubRespuestas(['Respuesta invalida']),406)

    # Metodo concreto y de clase: Obtener lista de eventos
    @staticmethod
    def getEventList() -> list:
        return ['/universidades','/universidad/<idU>/diminutivo']

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
        """
        return {l: v
            for l,v in DBControlador.respuesta_invalida.items()
            if l in seleccion}

    @staticmethod
    def _getUniversidades() -> Response:
        """ Metodo de clase: Obtener datos universidades

        Metodo que retorna la informacion de las universidades
        contenida en la base de datos, convertida en una lista de
        esquemas manejables.
        """
        universidades = get_all_from_table(UniversidadEntidad,
                UniversidadEsquema)
        return get_obj_as_response(universidades,200) #recibidor del comando

    @staticmethod
    def _getDiminutivoUniversidad(parametros: dict) -> Response:
        """ Metodo de clase: Obtener diminutivo de universidad

        Metodo que retorna el diminutivo de una universidad.

        Parametros:
            parametros (dict) -- diccionario de parametros, para
                el comando el diccionario debe contener la llave
                `idU`, que corresponde al identificador de la
                universidad a buscar
        """
        universidad = get_one_from_table_by_filter(UniversidadEntidad,
            UniversidadEntidad.univ_id,
            int(parametros['idU']))

        #condicional existe registro
        if universidad:
            return get_obj_as_response(
                universidad.diminu,
                200) #recibidor del comando
        else:
            return get_obj_as_response(
                DBControlador._getSubRespuestas(
                    ['Respuesta vacia']),
                    406) #recibidor por si error del comando