#-------------------------------------------------------------------------------
# Name:        Usuario
# Purpose:     Entidad y Esquema de usuario.
#
# Author:      Aref
#
# Created:     9/10/2022
# Copyright:   (R) ACMUD 2022 / (k) Alta Lengua 2023 --
# Licence:     <GPLv3>
#-------------------------------------------------------------------------------

""" Modulo: Usuario

Entidad y Esquema de usuario.
"""

from flask_login import UserMixin
from sqlalchemy import (
        Column,
        Boolean,
        Integer,
        String,
        CheckConstraint,
        UniqueConstraint,
        exc)
from typing import Union

from ..entidad import Entidad
from ...entidades import Base
from ...utilidades.utilidades_db import add_record

from ...utilidades.utilidades_sesion import (
        trocear_clave,
        chequear_clave)

class UsuarioEntidad(Entidad, Base, UserMixin):
    """ Clase: Entidad Usuario
        (Entidad, Base, UserMixin)

    Objeto entidad que representa un usuario para la base de
    datos. Con los campos identificador (usur_id), nombres
    (usur_nombres), apellidos (usur_apellidos), correo
    electronico [unico] (usur_correo), apodo [unico]
    (usur_apodo), clave encriptada con un algoritmo de picadillo
    (usur_clave_troceada), valor si ha iniciado sesion
    (usur_esta_sesion) y valor si es un administrador
    (usur_es_administrador).
    """
    __tablename__ = 'usuario'
    __table_args__ = (
        UniqueConstraint("usur_apodo",
            name="usuario_usur_apodo_uk"),

        CheckConstraint("usur_apodo ~* '^[A-Za-z0-9._%-]+$'",
            name="usuario_usur_apodo_ck"),

        UniqueConstraint("usur_correo",
            name="usuario_usur_correo_uk"),

        CheckConstraint("usur_correo ~* '^[A-Za-z0-9._-]" +
                "+@[A-Za-z0-9.-]+[.][A-Za-z]+$'",
            name="usuario_usur_correo_ck")
        )

    usur_id = Column(Integer, primary_key=True)
    usur_nombres = Column(String(75), nullable=False)
    usur_apellidos = Column(String(75), nullable=False)
    usur_correo = Column(String(75), nullable=False, index = True)
    usur_apodo = Column(String(30), nullable=False, index = True)
    usur_clave_troceada = Column(String(256), nullable=False)
    usur_esta_sesion = Column(Boolean, nullable=False, default=False)
    #En versiones posteriores la columna usur_es_administrador puede ser
    # despreciada, y ser reemplazada por una columna de roles con cadenas de
    # texto separadas por espacios
    usur_es_administrador = Column(Boolean, nullable=False, default=False)

    # Metodo dunder: Constructor Usuario
    def __init__(self,
            nombres: str,
            apellidos: str,
            correo: str,
            apodo: str,
            clave: str, #recibe la clave del usuario desencriptada
            **kargs):
        Entidad.__init__(
                self,
                'usur_' +
                    ''.join(
                    i[0].lower() #genera el diminutivo con los datos
                    for i in f'{nombres} {apellidos}'.split()
                ))

        self.usur_nombres = nombres
        self.usur_apellidos = apellidos
        self.usur_correo = correo
        self.usur_apodo = apodo
        self.usur_clave_troceada = trocear_clave(clave)

    # Metodo dunder: Cadena Usuario
    def __str__(self) -> str:
        return f'{self.usur_apodo} [{self.diminu}] <{self.usur_correo}>'

    # Metodo propiedad: Identificador
    @property
    def id(self) -> int:
        return self.usur_id

    # Metodo propiedad: Nombre completo
    @property
    def nombre_completo(self) -> int:
        return f'{self.usur_nombres} {self.usur_apellidos}'

    # Metodo concreto: Obtener identificador
    #Metodo sobreescrito de la clase padre UserMixin para las
    # funcionalidades de flask_login.
    def get_id(self):
        return self.id

    # Metodo: Chequear clave
    def chequear_clave(self, clave: str) -> bool:
        return chequear_clave(clave,self.usur_clave_troceada)

    # Metodo: Iniciar sesion
    def iniciar_sesion(self):
        self.usur_esta_sesion = True

    # Metodo: Cerrar sesion
    def cerrar_sesion(self):
        self.usur_esta_sesion = False

    def crear_usuario(self):
        """ Metodo: Crear usuario

        Metodo que crea un usuario en la base de datos en base al
        usuario en memoria.

        Si sucede un error en los datos autogenerados del
        usuario, se generan nuevos datos libres del error.

        Excepciones:
            exc.SQLAlchemyError -- si al crear el usuario en la
                base de datos, se viola alguna regla de
                integridad (indices, chequeos, unicidad, etc.)
            RecursionError -- si tras varias capturas de la
                excepcion exc.SQLAlchemyError, no se resuelve
        """
        try: add_record(self)

        except exc.SQLAlchemyError as SQL:
            #condicional si el error en la sentencia es por una violacion de
            # la integridad del diminutivo
            if all(mss in str(SQL)
                    for mss in
                    ['UniqueViolation','«usuario_diminu_key»']):
                from random import choice

                #genera un diminutivo alterno
                self.diminu += choice(self.diminu.replace('usur_',''))
                self.crear_usuario() #recursion

            else: raise exc.SQLAlchemyError(SQL) #excepcion capturada y lanzada

        except RecursionError as r: #(no esta funcionando... pero deberia...)
            print(r) ##excepcion capturada y depurada

from marshmallow import Schema, fields, post_load

class UsuarioEsquema(Schema):
    """ Clase: Esquema Usuario
        (Schema)

    Objeto esquema que representa un usuario para la
    serializacion en peticiones POST. Con los campos
    identificador (id), diminutivo (diminu), nombres
    (usur_nombres), apellidos (usur_apellidos), correo
    electronico (usur_correo), apodo (usur_apodo), clave
    (usur_clave_troceada), sesionado (usur_esta_sesion) y
    administrador (usur_es_administrador).
    """
    id = fields.Number()
    diminu = fields.Str(data_key="diminutivo")
    usur_nombres = fields.Str(data_key="nombres")
    usur_apellidos = fields.Str(data_key="apellidos")
    usur_correo = fields.Str(data_key="correo")
    usur_apodo = fields.Str(data_key="apodo")
    usur_clave_troceada = fields.Str(data_key="clave")
    usur_esta_sesion = fields.Bool(data_key="sesionado")
    #En versiones posteriores el campo usur_es_administrador puede ser
    # despreciado, y ser reemplazado por un campo de roles con una lista de
    # cadenas de texto
    usur_es_administrador = fields.Bool(data_key="administrador")

    @staticmethod
    def campos(tipo_retrn: type = list) -> Union[list, tuple, set]:
        """ Metodo de clase: Campos del esquema

        Metodo que retorna los campos de los objetos esquema
        usuario.

        Los campos corresponden con algunos atributos y sirven
        para convertir una entidad usuario en un esquema usuario
        (Entidad->Esquema).

        Parametros:
            tipo_return (type) -- tipo de dato en el cual se
                retornan los campos

        Retorno:
            un iterador con los campos del esquema usuario
        """
        return tipo_retrn(["usur_nombres","usur_apellidos","usur_correo",
                 "usur_apodo","usur_clave_troceada"])

    @staticmethod
    def claves(tipo_retrn: type = list):
        """ Metodo de clase: Claves de la entidad

        Metodo que retorna las claves necesarias en el
        constructor entidad usuario.

        Las claves corresponden con los parametros del
        constructor entidad y sirven para construir una entidad
        usuario en base a un esquema usuario (Esquema->Entidad).

        Parametros:
            tipo_return (type) -- tipo de dato en el cual se
                retornan las claves

        Retorno:
            un iterador con las claves del constructor entidad
                usuario
        """
        return tipo_retrn(["nombres","apellidos","correo",
                "apodo","clave"])

    @post_load
    def crear_usr(self, data: dict, **kargs) -> UsuarioEntidad:
        """ Metodo: Conversion esquema-entidad

        Metodo que asocia los campos del esquema usuario a la
        entidad usuario para la serializacion.

        Parametros:
            data (dict) -- campos de usuario en forma de
                diccionario
            **kargs (dict) -- campos opcionales de configuracion

        Retorno:
            una entidad usuario formada por los datos del
                diccionario
        """
        for clave_dic, campo_esquema in zip(self.claves(), self.campos()):
            #los parametros al construir una entidad usuario son diferentes a
            # sus columnas, por ello se debe estar seguro que se envian las
            # claves correctas
            if clave_dic not in data:
                data[clave_dic] = data[campo_esquema]

        return UsuarioEntidad(**data)