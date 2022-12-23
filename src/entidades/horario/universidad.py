#-------------------------------------------------------------------------------
# Name:        Universidad
# Purpose:     Entidad y Esquema de universidad.
#
# Author:      Aref
#
# Created:     19/9/2022
# Copyright:   (R) ACMUD 2022 / (k) Alta Lengua 2023 --
# Licence:     <GPLv3>
#-------------------------------------------------------------------------------

""" Modulo: Universidad

Entidad y Esquema de universidad.
"""

from sqlalchemy import Column, ForeignKey, Integer, String

from .. import Base
from ..entidad import Entidad

class UniversidadEntidad(Entidad, Base):
    """ Clase: Entidad Universidad
        (Entidad, Base)

    Objeto entidad que representa una universidad para la base de
    datos. Con los campos identificador (univ_id), nombre
    (univ_nombre) y enlace web al logotipo (univ_url_logo).
    """
    __tablename__ = 'universidad'

    univ_id = Column(Integer, primary_key=True)
    univ_nombre = Column(String)
    univ_url_logo = Column(String)

    # Metodo dunder: Constructor Universidad
    def __init__(self,
            nombre: str,
            url_isotipo: str,
            diminu: str = None,
            **kargs):
        #condicional genera el diminutivo si no recibe alguno
        if not diminu: diminu = ''.join(i[:2] for i in nombre.split())

        Entidad.__init__(self, diminu)
        self.univ_nombre = nombre
        self.univ_url_logo = url_isotipo

    # Metodo dunder: Cadena Universidad
    def __str__(self) -> str: return f'{self.univ_nombre} [{self.diminu}]'

    # Metodo propiedad: Identificador
    @property
    def id(self) -> int: return self.univ_id

from marshmallow import Schema, fields, post_load

class UniversidadEsquema(Schema):
    """ Clase: Esquema Universidad
        (Schema)

    Objeto esquema que representa una universidad para la
    serializacion en peticiones POST. Con los campos
    identificador (id), diminutivo (diminu), nombre (univ_nombre)
    y isotipo (univ_url_logo).
    """
    id = fields.Number()
    diminu = fields.Str(data_key="diminutivo")
    univ_nombre = fields.Str(data_key="nombre")
    univ_url_logo = fields.Str(data_key="isotipo")

    @post_load
    def crear_u(self, data: dict, **kargs) -> UniversidadEntidad:
        """ Metodo: Conversion esquema-entidad

        Metodo que asocia los campos del esquema universidad a la
        entidad universidad para la serializacion.

        Parametros:
            data (dict) -- campos de universidad en forma de
                diccionario
            **kargs (dict) -- campos opcionales de configuracion

        Retorno:
            una entidad universidad formada por los datos del
                diccionario
        """
        if "nombre" not in data:
            data["nombre"] = data["univ_nombre"]

        if "url_isotipo" not in data:
            data["url_isotipo"] = data["univ_url_logo"]

        return UniversidadEntidad(**data)