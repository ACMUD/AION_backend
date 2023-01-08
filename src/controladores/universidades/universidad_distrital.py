#-------------------------------------------------------------------------------
# Name:        Universidad Distrital Francisco Jose de Caldas
# Purpose:     Controlador Universidad Distrital Francisco Jose
#               de Caldas de la jerarquia de modelos universidad.
#
# Author:      Aref
#
# Created:     1/1+9/2022
# Copyright:   (R) ACMUD 2022 / (k) Alta Lengua 2023 --
# Licence:     <GPLv3>
#-------------------------------------------------------------------------------

from ..universidad import UniversidadControlador
from ...config import config
from ...entidades.horario.universidad import (
        UniversidadEntidad,
        UniversidadEsquema)

from ...modelos.universidades.universidad_distrital import\
        UniversidadDistritalFactoria

from ...utilidades.utilidades_db import (
        get_one_from_table_by_filter)

from ...utilidades.utilidades_JSON import get_JSON_as_obj
from ...utilidades.utilidades_web import get_obj_as_response

from flask import jsonify, make_response
from flask.wrappers import Response
import json

class UniversidadDistritalControlador(UniversidadControlador):
    """ Clase: Controlador Universidad Distrital
        (UniversidadControlador)

    Objeto con el patron comando de la jerarquia de modelos
    universidad que representa un controlador para la Universidad
    Distrital Francisco Jose de Caldas. Sirve para recopilar los
    metodos disponibles para controlar las solicitudes de las
    vistas y las respuestas de los modelos.
    """
    # Atributo concreto: Respuesta invalida
    respuesta_invalida = {"Respuesta invalida": # Fallo general
            'Universidad Distrital Francisco Jose de Caldas rechazo',

            "Parametros incorrectos": # Fallo si parametros inmanejables
            'Parametros suministrados son insuficientes para la solicitud',

            "Respuesta vacia": # Fallo si hay carencia de respuesta
            'Solicitud a Universidad Distrital Francisco Jose de Caldas ' +
                'devolvio una respuesta vacia',

            "Fichero inexistente": # Fallo si no existe un fichero valido
            'Fichero utilizado para la solicitud es inexistente o no pudo' +
                'ser alcanzado',

            "Respuesta ajena": # Fallo si no hay respuesta programada
            'Error de programacion en las respuestas'
            }

    diminu = 'ud' #diminutivo
    directorio = config["directorio_carga"] + r'\..\ud' #directorio especifico

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

        if evento == '/universidad/<idU>': return self._getUniversidad()

        if evento == '/universidad/<idU>/diminutivo':
            return self._getDiminutivo()

        if evento == '/universidad/<idU>/cabecera': return self._getCabecera()

        if evento == '/universidad/<idU>/preview': return self._getPreview()

        if evento == '/universidad/<idU>/facultades':
            return self._getFacultades()

        if evento == '/universidad/<idU>/proyectos':
            return self._getProyectos()

        if evento == '/universidad/<idU>/horarios': return self._getHorarios()

        if evento == '/universidad/<idU>/horarios/codigo/<codMat>':
            #condicional detalles completos de la solicitud
            if (type(parametros) != dict or
                    'codMat' not in parametros):
                #recibidor por si errores
                return get_obj_as_response(
                        self._getSubRespuestas([
                                'Parametros incorrectos',
                                'Respuesta invalida']),406)

            #recibidor del comando
            return self._getMateriaHorarios(parametros)

        if evento == '/universidad/<idU>/horarios/codigo/<codMat>/' +\
                'grupo/<idGrup>':
            #condicional detalles completos de la solicitud
            if (type(parametros) != dict or
                    'codMat' not in parametros or
                    'idGrupo' not in parametros):
                #recibidor por si errores
                return get_obj_as_response(
                        self._getSubRespuestas([
                                'Parametros incorrectos',
                                'Respuesta invalida']),406)

            #recibidor por si error
            return self._getMateriaHorario(parametros)

        if evento == '/universidad/<idU>/cargar_archivo':
            #condicional detalles completos de la solicitud
            if (type(parametros) != dict or
                    'postFile' not in parametros):
                #recibidor por si errores
                return get_obj_as_response(
                        self._getSubRespuestas([
                                'Parametros incorrectos',
                                'Respuesta invalida']),406)

            #recibidor por si error
            return self._setHorarios(parametros)

        if evento == '/universidad/<idU>/horarios/actualizar/<tipo>':
            #condicional detalles completos de la solicitud
            if (type(parametros) != dict or
                    'extension' not in parametros):
                #recibidor por si errores
                return get_obj_as_response(
                        self._getSubRespuestas([
                                'Parametros incorrectos',
                                'Respuesta invalida']),406)

            #recibidor por si error
            return self._updateHorarios(parametros)

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
        return ['/universidad/<idU>',
            '/universidad/<idU>/diminutivo',
            '/universidad/<idU>/cabecera',
            '/universidad/<idU>/preview',
            '/universidad/<idU>/facultades',
            '/universidad/<idU>/proyectos',
            '/universidad/<idU>/horarios',
            '/universidad/<idU>/horarios/codigo/<codMat>',
            '/universidad/<idU>/horarios/codigo/<codMat>/grupo/<idGrup>']

    @staticmethod
    def _getUniversidad() -> Response:
        """ Metodo de clase: Obtener datos universidad

        Metodo que retorna la informacion de la universidad
        contenida en la base de datos.
        """
        #usa utilidades
        universidad = get_one_from_table_by_filter(
            UniversidadEntidad,
            UniversidadEntidad.diminu,
            __class__.diminu)

        #condicional existe registro
        if universidad:
            #transforma a datos manejables
            esquema = UniversidadEsquema().dump(universidad, many=False)

            return get_obj_as_response(esquema,200) #recibidor del comando

        #opcional fichero no existe
        return get_obj_as_response(__class__._getSubRespuestas(
            ['Respuesta vacia']),406) #recibidor por si error del comando

    # Metodo de clase: Obtener diminutivo
    @staticmethod
    def _getDiminutivo() -> Response:
        return get_obj_as_response(__class__.diminu,200) #recibidor del comando

    @staticmethod
    def _getCabecera() -> Response:
        """ Metodo de clase: Obtener cabecera

        Metodo que retorna el periodo actual de los datos de la
        universidad que se utilizaran.
        """
        try:
            with open(__class__.directorio + r'\cabecera') as archivo:
                cabecera = archivo.read() #lectura de la cabecera
                return get_obj_as_response(cabecera,200) #recibidor del comando

        #opcional fichero no existe
        except FileNotFoundError:
            return get_obj_as_response(
                __class__._getSubRespuestas(
                    ['Fichero inexistente']),
                    406) #recibidor por si error del comando

    @staticmethod
    def _getPreview() -> Response:
        """ Metodo de clase: Obtener previsualizacion de la
            universidad

        Metodo que retorna la informacion util para el cliente de
        la universidad.
        """
        u = dict(__class__._getUniversidad().json)
        u["periodo_actual"] = __class__._getCabecera().json
        return get_obj_as_response(u,200) #recibidor del comando

    @staticmethod
    def _getFacultades() -> Response:
        """ Metodo de clase: Obtener datos de facultades

        Metodo que retorna la informacion de las materias por
        facultad.
        """
        ruta_archivo = __class__.directorio + '\\' + __class__.diminu +\
                __class__._getCabecera().json + '-facultades.json'
        facultad_dict = get_JSON_as_obj(ruta_archivo)

        #condicional existe fichero
        if facultad_dict:
            facultad_list = [{"nombre": n, "par_grupos": pg}
                    for n,pg in facultad_dict.items()]
            return get_obj_as_response(
                    facultad_list,
                    200) #recibidor del comando

        #opcional fichero no existe
        return get_obj_as_response(
            __class__._getSubRespuestas(
                ['Respuesta vacia','Fichero inexistente']),
                406) #recibidor por si error del comando

    @staticmethod
    def _getProyectos() -> Response:
        """ Metodo de clase: Obtener datos de proyectos

        Metodo que retorna la informacion de las materias por
        proyecto curricular.
        """
        ruta_archivo = __class__.directorio + '\\' + __class__.diminu +\
                __class__._getCabecera().json + '-proyectos.json'
        proyecto_dict = get_JSON_as_obj(ruta_archivo)

        #condicional existe fichero
        if proyecto_dict:
            proyecto_list = [{"nombre": n, "par_grupos": pg}
                    for n,pg in proyecto_dict.items()]
            return get_obj_as_response(
                    proyecto_list,
                    200) #recibidor del comando

        #opcional fichero no existe
        return get_obj_as_response(
            __class__._getSubRespuestas(
                ['Respuesta vacia','Fichero inexistente']),
                406) #recibidor por si error del comando

    @staticmethod
    def _getHorarios() -> Response:
        """ Metodo de clase: Obtener horarios

        Metodo que retorna la informacion de los horarios
        completos.
        """
        ruta_archivo = __class__.directorio + '\\' + __class__.diminu +\
                __class__._getCabecera().json + '.json'
        horario_dict = get_JSON_as_obj(ruta_archivo)

        #condicional existe fichero
        if horario_dict:
            return get_obj_as_response(horario_dict,200) #recibidor del comando

        #opcional fichero no existe
        return get_obj_as_response(
            __class__._getSubRespuestas(
                ['Respuesta vacia','Fichero inexistente']),
                406) #recibidor por si error del comando

    @staticmethod
    def _getMateriaHorarios(parametros: dict) -> Response:
        """ Metodo de clase: Obtener horarios de una materia

        Metodo que retorna la informacion de los horarios de una
        materia.

        Parametros:
            parametros (dict) -- diccionario de parametros para
                el comando, el diccionario debe contener la llave
                `codMat`, que corresponde al codigo de la materia
                a buscar
        """
        ruta_archivo = __class__.directorio + '\\' + __class__.diminu +\
                __class__._getCabecera().json + '.json'
        horario_dict = get_JSON_as_obj(ruta_archivo)

        #condicional no existe fichero
        if not horario_dict:
            return get_obj_as_response(
                __class__._getSubRespuestas(
                    ['Respuesta vacia','Fichero inexistente']),
                    406) #recibidor por si error del comando

        #trata de encontrar los horarios de la materia
        try: materia_dict = horario_dict[parametros['codMat']]
        except KeyError as k:
            return get_obj_as_response(
                __class__._getSubRespuestas(
                    ['Respuesta vacia','Parametros incorrectos']),
                    406) #recibidor por si error del comando

        #condicional existe fichero
        if materia_dict != []:
            materia_dict2 = {
                    "nombre": materia_dict["espacio academico"],
                    "grupos": []} #estandarizar el diccionario

            del(materia_dict["espacio academico"])

            for l,v in materia_dict.items():
                materia_dict2["grupos"].append({"id": l, "horarios": v})

            return get_obj_as_response(
                materia_dict2,
                200) #recibidor del comando

        #opcional fichero no existe
        return get_obj_as_response(
            __class__._getSubRespuestas(
                ['Respuesta vacia','Respuesta invalida']),
                406) #recibidor por si error del comando

    @staticmethod
    def _getMateriaHorario(parametros: dict) -> Response:
        """ Metodo de clase: Obtener horarios de un grupo de una
            materia

        Metodo que retorna la informacion del horario de un grupo
        de una materia.

        Parametros:
            parametros (dict) -- diccionario de parametros para
                el comando, el diccionario debe contener la llave
                `codMat`, que corresponde al codigo de la materia
                a buscar y la llave `idGrupo`, que corresponde al
                identificador del grupo a buscar
        """
        ruta_archivo = __class__.directorio + '\\' + __class__.diminu +\
                __class__._getCabecera().json + '.json'
        horario_dict = get_JSON_as_obj(ruta_archivo)

        #condicional no existe fichero
        if not horario_dict:
            return get_obj_as_response(
                __class__._getSubRespuestas(
                    ['Respuesta vacia','Fichero inexistente']),
                    406) #recibidor por si error del comando

        #trata de encontrar el horario del grupo de la materia
        try:
            materia_dict =\
                    horario_dict[parametros['codMat']][parametros['idGrupo']]
        except KeyError as k:
            return get_obj_as_response(__class__._getSubRespuestas(
                ['Respuesta vacia','Parametros incorrectos']),
                406) #recibidor por si error del comando

        #condicional existe fichero
        if materia_dict != []:
            return get_obj_as_response(
                materia_dict,
                200) #recibidor del comando

        #opcional fichero no existe
        return get_obj_as_response(__class__._getSubRespuestas(
                ['Respuesta vacia','Respuesta invalida']),
                406) #recibidor por si error del comando

    @staticmethod
    def _setHorarios(parametros: dict) -> Response:
        """ Metodo de clase: Ajustar horarios

        Metodo que ajusta el archivo de los horarios de la
        Universidad Distrital Francisco Jose de Caldas.

        Parametros:
            parametros (dict) -- diccionario de parametros para
                el comando, el diccionario debe contener la llave
                `postFile`, que corresponde con la ruta del
                archivo con los nuevos horarios
        """
        #opcional fichero no enviado
        if parametros['postFile'].filename == '':
            return get_obj_as_response(__class__._getSubRespuestas(
                    ['Respuesta vacia','Respuesta invalida']),
                    406) #recibidor por si error del comando

        #opcional fichero no existe
        if not parametros['postFile']:
            return get_obj_as_response(__class__._getSubRespuestas(
                    ['Fichero inexistente','Respuesta invalida']),
                    406) #recibidor por si error del comando

        #asigna la extension solo si es valida
        extension = UniversidadDistritalFactoria.extension_permitida(
                parametros['postFile'].filename)

        #condicional no se asigno extension
        if not extension:
            return get_obj_as_response(__class__._getSubRespuestas(
                    ['Parametros incorrectos','Respuesta invalida']),
                    406) #recibidor por si error del comando

        #fuerza la creacion del directorio si no existe
        UniversidadDistritalFactoria().getAlmacenadorJSON().inicializar()


        #carga el archivo
        archivo = f'submission.{extension}'
        parametros['postFile'].save(__class__.directorio + '\\' + archivo)

        return get_obj_as_response(
                {'Respuesta': 'Archivo cargado',
                'Extension': extension},
                201) #recibidor del comando

    @staticmethod
    def _updateHorarios(parametros: dict) -> Response:
        """ Metodo de clase: Actualizar horarios

        Metodo que actualiza los horarios de la Universidad
        Distrital Francisco Jose de Caldas.

        Parametros:
            parametros (dict) -- diccionario de parametros para
                el comando, el diccionario debe contener la llave
                `extension`, que corresponde a la extension del
                archivo con los nuevos horarios
        """
        #trata de crear el json
        try:
            UniversidadDistritalFactoria().\
                getCreadorJSON(parametros['extension']).\
                crear_JSON()

        #opcional si el fichero para actualizar los horarios no existe
        except FileNotFoundError:
            return get_obj_as_response(__class__._getSubRespuestas(
                    ['Fichero inexistente','Respuesta invalida']),
                    406) #recibidor por si error del comando

        return get_obj_as_response(
                {'Respuesta':
                'Horarios actualizados'},
                200) #recibidor del comando