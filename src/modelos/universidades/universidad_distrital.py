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

from .almacenador_JSON import AlmacenadorJSON
from ...config import config
from ...utilidades.utilidades_JSON import update_dict, update_json_file

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
            update_dict(self.facultads,
                             value['facultad'],
                             val = (value['cod.'],value['grp.']))

            # actualiza los proyectos curriculares con una
            #  materia y su grupo
            update_dict(self.proyectos,
                             value['proyecto curricular'],
                             val = (value['cod.'],value['grp.']))

            # actualiza los dursos, para que exista un
            #  diccionario por cada curso
            update_dict(self.cursos,
                             value['cod.'],
                             typ = dict)

            # actualiza el diccionario del curso con un nombre de
            #  espacio academico
            update_dict(self.cursos[value['cod.']],
                             'espacio academico',
                             val = value['espacio academico'],
                             typ = str)

            # actualiza el diccionario del curso con los demas
            #  datos relevantes (materia, grupo, anio y periodo)
            update_dict(self.cursos[value['cod.']],
                             value['grp.'],
                             val = {i: value[i]
                                    for i in value
                                    if i not in ['cod.','grp.',
                                                 'anio','periodo']},
                             typ = list)

        except KeyError as k:
            raise KeyError(f' Clave {k} no encontrada, verifique que usa un ' +
                'creador de JSON adecuado para el Almacenador de JSON' +
                type(self).__name__)

    def finalizar(self):
        """ Metodo concreto: Finalizar almacenando

        Metodo que finaliza el almacenado actualizando todos los
        JSON con los datos de los diccionarios
        """
        # actualiza el JSON de cursos
        update_json_file(self.cursos,
                f'{self.directorio}\{self.periodo}.json')

        # actualiza el JSON de facultades
        update_json_file(self.facultads,
                f'{self.directorio}\{self.periodo}-facultades.json')

        # actualiza el JSON de proyectos curriculares
        update_json_file(self.proyectos,
                f'{self.directorio}\{self.periodo}-proyectos.json')

        # actualiza el archivo de cabecera de la universidad
        with open(f'{self.directorio}\cabecera', 'w') as cabecera:
            cabecera.write(self.periodo.replace('ud',''))

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

    @staticmethod
    def extension_permitida(origen: str) -> str:
        """ Metodo de clase: Extension es permitida

        Metodo que retorna la extension de un fichero de origen
        si es una extension permitida, o nulo en otro caso.

        Parametro:
            origen (str) -- nombre de un fichero de origen

        Retorno:
            una extension validada o nulo
        """
        if '.' in origen:
            extension = origen.rsplit('.', 1)[1].lower()

            if extension in ['pdf','xml']:
                return extension

        return None