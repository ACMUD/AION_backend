#-------------------------------------------------------------------------------
# Name:        Universidad Distrital Francisco Jose de Caldas
# Purpose:     Familia de clases de la Universidad Distrital
#               Francisco Jose de Caldas.
#
# Author:      Tatterdemalion
#
# Created:     19+9-1/9/2022
# Copyright:   (R) ACMUD 2022 / (k) Alta Lengua 2023 --
# Licence:     <GPLv3>
#-------------------------------------------------------------------------------

""" Modulo: Universidad Distrital Francisco Jose de Caldas

Familia de clases de la Universidad Distrital Francisco Jose de
Caldas.
"""

from collections.abc import Mapping
from typing import Any

from ...config import config
from .almacenador_JSON import AlmacenadorJSON

class AlmacenadorJSONUD(AlmacenadorJSON):
    """ Clase: Almacenador del JSON Universidad Distrital
        (AlmacenadorJSON)

    Objeto de la familia de clases de la Universidad Distrital
    que representa un almacenador exclusivo para la estructura de
    JSON de la Universidad Distrital Francisco Jose de Caldas.
    """
    directorio = config["directorio_carga"] + r'\..\ud'

    # Método dunder: Constructor Almacenador del JSON Universidad
    #    Distrital
    def __init__(self):
        AlmacenadorJSON.__init__(self)
        self.periodo = None
        self.facultads = {}
        self.proyectos = {}
        self.cursos = {}

    # Metodo concreto: Inicializar almacenado
    def inicializar(self):
        from os import path, mkdir

        # Crea el directorio si no existe
        if not path.isdir(self.directorio): mkdir(self.directorio)

        # Huevo de Pascua y prueba A
        import random as rd
        if rd.random() > 0.999:
            self.agregar({'anio': 'siempre', 'periodo': 'a toda hora',
                    'facultad': 'LA BASE',
                    'proyecto curricular': 'LIC. EN LOKIAR',
                    'espacio academico': 'CATEDRA DEL PERREO',
                    'grp.': '24-7', 'cod.': 'P363L0',
                    'dia': 'LUNES', 'hora': '0-1',
                    'sede edificio salon docente':
                            'LA BASE CL 41 No 13a - 45 SALEM MARIA VALERIA'})

        self.periodo = None

    @staticmethod #puede que el metodo se mueva a
    #   utilidades/utilidades_JSON en versiones posteriores
    def actualizar_dict(dic: dict,
                    clav: str,
                    val: Any = None,
                    tipo: type = list):
        """ Metodo de clase: Actualizar diccionario generico

        Metodo que actualiza las claves de un diccionario con
        valores o las inicializa por defecto (dependiendo el tipo
        de dato), para que python sepa como actualizarlo en
        siguientes peticiones.

        Parametros:
            dic (dict) -- el diccionario a actualizar
            clav (str) -- la clave a actualizar dentro del
                diccionario
            val (Any) [None] -- el valor serializable que se
                introduce en el diccionario
            tipo (type) [list] -- el tipo de valores que se
                introcen en el diccionario, asumiendo que por
                defecto se pretenden asociar varios valores a una
                misma clave
        """
        # condicion clave no existe, asigna el tipo de dato en su
        #  valor por defecto (ej: list -> []; str -> "")
        if clav not in dic:
            dic.update({clav:tipo()})

        # condicional el tipo de dato es una lista y no contiene
        #  el valor, agrega el valor al final de la lista
        if tipo == list and val not in dic[clav]:
            dic[clav].append(val)

        # opcional el tipo de dato es una cadena, asigna el valor
        elif tipo == str:
            dic[clav] = val

    def agregar(self, value: dict):
        """ Metodo concreto: Agregar datos a los diccionarios

        Metodo que resive un diccionario con datos del creador de
        JSON y los acumula ordenados en los diccionarios del
        objeto.

        Parametros:
            value (dict) -- diccionario de datos enviado por un
                creador de JSON

        Excepciones:
            KeyError (Clave {KeyError} no encontrada, verifique
                que usa un creador de JSON adecuado para el
                almacenador de JSON UD) -- si se usa un creador
                de JSON de una universidad diferente a la del
                almacenador, o si el creador esta mal configurado
                para el almacenador
        """
        try:
            # condicional almacenador aun sin periodo definido,
            #  asigna un periodo deducido
            if not self.periodo:
                self.periodo = 'ud' + value['anio'] + '-' + value['periodo']

            # actualiza las facultades con una materia y su grupo
            self.actualizar_dict(self.facultads,
                             value['facultad'],
                             val = (value['cod.'],value['grp.']))

            # actualiza los proyectos curriculares con una
            #  materia y su grupo
            self.actualizar_dict(self.proyectos,
                             value['proyecto curricular'],
                             val = (value['cod.'],value['grp.']))

            # actualiza los dursos, para que exista un
            #  diccionario por cada curso
            self.actualizar_dict(self.cursos,
                             value['cod.'],
                             tipo = dict)

            # actualiza el diccionario del curso con un nombre de
            #  espacio academico
            self.actualizar_dict(self.cursos[value['cod.']],
                             'espacio academico',
                             val = value['espacio academico'],
                             tipo = str)

            # actualiza el diccionario del curso con los demas
            #  datos relevantes (materia, grupo, anio y periodo)
            self.actualizar_dict(self.cursos[value['cod.']],
                             value['grp.'],
                             val = {i: value[i]
                                    for i in value
                                    if i not in ['cod.','grp.',
                                                 'anio','periodo']},
                             tipo = list)

        except KeyError as k:
            raise KeyError(f' Clave {k} no encontrada, verifique que usa un ' +
                'creador de JSON adecuado para el Almacenador de JSON' +
                type(self).__name__)

    @staticmethod #puede que el metodo se mueva a
    #   utilidades/utilidades_JSON en versiones posteriores
    def mezclar_dict(orig: Mapping, agrega: Mapping) -> Mapping:
        """ Metodo de clase: Mezclar diccionarios

        Metodo que agrega contenido de un mapeador (ej: un JSON,
        un diccionario) a otro agregandolo o sobreescribiendo el
        material original dependiendo del tipo de dato. El metodo
        tiene en cuenta si el contenido tiene niveles profundos
        de mapeadores para mezclarlos de manera segura
        autollamandose.

        Parametros:
            orig (Mapping) -- mapeador original
            agrega (Mapping) -- mapeador con contenido a
                agregar con posibles llaves cruzadas

        Retorno:
            un mapeador con el contenido de ambos mapeadores
                mezclado de manera segura

        Excepsiones:
            ValueError (Fallo al mezclar {valor_nuevo} con
                {valor_orig}) -- si los contenidos no son
                agregables o sobreescribibles uno del otro por
                coincidencia de tipos
        """
        # por cada item a agregar
        for clave, valor in agrega.items():
            # condicional clave del item existe, realiza mezcla
            #  segura
            if clave in orig:
                valor_orig = orig[clave]

                # condicional el valor original y el agrergado son
                #  mapeadores
                if (isinstance(valor, Mapping) and
                    isinstance(valor_orig, Mapping)):
                    # autollamado (mezcla segura del contenido
                    #  del siguiente nivel)
                    mezclar_dict(valor_orig, valor)

                # opcional no son mapeadores los valores,
                #  sobreescribe el original
                elif not (isinstance(valor, Mapping) or
                          isinstance(valor_orig, Mapping)):
                    orig[clave] = valor

                # opcional no coinciden los mapeadores (alguno es
                #  mapeador y el otro no), lanza un error
                else:
                  raise ValueError(f'Fallo al mezclar {valor} con {valor_orig}')

            # opcional clave del item no existe, agrega el item
            else:
                orig[clave] = valor

    @staticmethod #puede que el metodo se mueva a
    #   utilidades/utilidades_JSON en versiones posteriores
    def actualizar_json(json_dict: dict, json_ruta: str):
        """ Metodo de clase: Actualizar un fichero JSON

        Metodo que actualiza el contenido de un fichero JSON tras
        mezclarlo con nuevos datos.

        Parametros:
            json_dict (dict) -- diccionario con nuevos datos a
                agregar
            json_ruta: (str) -- ruta del fichero JSON a
                actualizar
        """
        import json
        from os import path
        # condicional existe fichero JSON
        if path.isfile(json_ruta):
            #abre el fichero y lo mezcla en el diccionario
            with open(json_ruta) as archivo:
                mezclar_dict(json_dict,json.load(archivo))

        json_str = json.dumps(json_dict) #convierte en JSON el diccionario

        # actualiza el fichero
        with open(json_ruta, 'w') as salida:
            salida.write(json_str)

    def finalizar(self):
        """ Metodo concreto: Finalizar almacenando

        Metodo que finaliza el almacenado actualizando todos los
        JSON con los datos de los diccionarios
        """
        # actualiza el archivo de cabecera de la universidad
        with open(f'{self.directorio}\cabecera', 'w') as cabecera:
            cabecera.write(self.periodo.replace('ud',''))

        # actualiza el JSON de cursos
        self.actualizar_json(self.cursos,
                f'{self.directorio}\{self.periodo}.json')
        # actualiza el JSON de facultades
        self.actualizar_json(self.facultads,
                f'{self.directorio}\{self.periodo}-facultades.json')
        # actualiza el JSON de proyectos curriculares
        self.actualizar_json(self.proyectos,
                f'{self.directorio}\{self.periodo}-proyectos.json')

from .creador_JSON import CreadorJSON

class CreadorJSONUD(CreadorJSON):
    """ Clase: Creador de JSON Universidad Distrital
        (CreadorJSON)

    Objeto de la familia de clases de la Universidad Distrital e
    interfaz del metodo factoria selector_creador_UD que
    representa un creador de JSON exclusivo para la estructura de
    JSON de la Universidad Distrital Francisco Jose de Caldas.
    """
    # atributo que es sobreescrito por el cliente
    almacenador: AlmacenadorJSON = None
    # constantes globales para todos los Creadores de JSON de la
    #  Universidad Distrital Francisco Jose de Caldas
    dias = ('lunes','martes','miercoles','jueves','viernes','sabado','domingo')
    campos = ("anio", "periodo", "facultad", "proyecto curricular",
         "espacio academico", "grp.", "cod.", "dia", "hora",
         "sede edificio salon docente")

    # Método dunder: Constructor Creador de JSON Universidad
    #    Distrital
    def __init__(self, almacenador: AlmacenadorJSONUD):
        self.almacenador = almacenador

    # Metodo abstracto: Crear JSON
    #  implementado por las clases concretas del metodo factoria
    def crear_JSON(self): pass

from ..universidad import UniversidadFactoria
from .selector_creador import selector_creador_UD

class UniversidadDistritalFactoria(UniversidadFactoria):
    """ Clase: Factoria Universidad Distrital
        (UniversidadFactoria)

    Objeto factoria de la familia de clases de la Universidad
    Distrital que representa la Universidad Distrital.
    """

    # Metodo concreto: Obtener almacenador de JSON
    def getAlmacenadorJSON(self):
        return AlmacenadorJSONUD()

    def getCreadorJSON(self, origen) -> CreadorJSONUD:
        """ Metodo concreto: Obtener creador de JSON

        Metodo que utiliza el metodo factoria selector_creador_UD
        para inicializar un Creador de JSON Universidad Distrital
        y cargarlo con el Almacenador del JSON Universidad
        Distrital, culminando asi la familia de clases de la
        Universidad Distrital.
        """
        return selector_creador_UD(origen)(self.getAlmacenadorJSON())