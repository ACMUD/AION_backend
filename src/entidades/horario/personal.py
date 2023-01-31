#-------------------------------------------------------------------------------
# Name:        Personal
# Purpose:     Entidad y Esquema de horario personal.
#
# Author:      Aref
#
# Created:     9/1/2023
# Copyright:   (R) ACMUD 2022 / (k) Alta Lengua 2023 --
# Licence:     <GPLv3>
#-------------------------------------------------------------------------------

""" Modulo: Personal

Entidad y Esquema de horario personal.
"""

from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    Sequence,
    PrimaryKeyConstraint
  )

from ..entidad import Entidad
from ...entidades import Base

personal_seq = Sequence(
    'personal_seq',
    minvalue = 1,
    maxvalue = 9999999999,
    increment = 1,
    start = 9,
    cache = None,
    order = None,
    cycle = False
  )

class PersonalEntidad(Entidad, Base):
    """ Clase: Entidad Personal
        (Entidad, Base)

    Objeto entidad que representa un horario personal para la
    base de datos. Con los campos identificador (persl_id),
    identificador de usuario (usur_id), identificador de
    universidad (univ_id), almacenado estado filtrado
    (persl_estd_filtr) y almacenado estado selecto
    (persl_estd_selct).
    """
    __tablename__ = 'personal'
    __table_args__ = (
        PrimaryKeyConstraint("persl_id", "usur_id", "univ_id", name="personal_uk"),
        )

    persl_id = Column(
        Integer,
        personal_seq,
        nullable=False,
        server_default=personal_seq.next_value()
      )

    usur_id = Column(
        Integer,
        ForeignKey('usuario.usur_id', name="usuario_id_fk"),
        nullable=False
      )

    univ_id = Column(
        Integer,
        ForeignKey('universidad.univ_id', name="universidad_id_fk"),
        nullable=False
      )

    persl_estd_filtr = Column(String)
    persl_estd_selct = Column(String)

    # Metodo dunder: Constructor Personal
    def __init__(self,
            usuario: int,
            universidad: int,
            estd_filtr: str,
            estd_selct: str,
            **kargs):
        Entidad.__init__(self, f'persl_{int(usuario)}_{int(universidad)}')
        self.usur_id = usuario
        self.univ_id = universidad
        self.estd_filtr = estd_filtr
        self.estd_selct = estd_selct

    # Metodo dunder: Cadena Personal
    def __str__(self) -> str:
        return f'Horario personal <{self.usur_id}, {self.univ_id}>'

    # Metodo propiedad: Identificador
    @property
    def id(self) -> int: return self.persl_id

from marshmallow import Schema, fields, post_load

class PersonalEsquema(Schema):
    """ Clase: Esquema Personal
        (Schema)

    Objeto esquema que representa un horario personal para la
    serializacion en peticiones POST. Con los campos
    identificador (id), diminutivo (diminu), usuario [id]
    (usur_id), universidad [id] (univ_id), filtros
    (persl_estd_filtr) y selectos (persl_estd_selct).
    """
    id = fields.Number()
    diminu = fields.Str(data_key="diminutivo")
    usur_id = fields.Number(data_key="usuario")
    univ_id = fields.Number(data_key="universidad")
    persl_estd_filtr = fields.Str(data_key="filtros")
    persl_estd_selct = fields.Str(data_key="selectos")

    @post_load
    def crear_p(self, data: dict, **kargs) -> PersonalEntidad:
        """ Metodo: Conversion esquema-entidad

        Metodo que asocia los campos del esquema de horario
        personal a la entidad de horario personal para la
        serializacion.

        Parametros:
            data (dict) -- campos de un objeto de horario personal
                en forma de diccionario
            **kargs (dict) -- campos opcionales de configuracion

        Retorno:
            una entidad de horario personal formada por los datos
                del diccionario
        """
        if "usuario" not in data: data["usuario"] = data["usur_id"]
        if "universidad" not in data: data["universidad"] = data["univ_id"]

        if "estd_filtr" not in data:
            data["estd_filtr"] = data["persl_estd_filtr"]

        if "estd_selct" not in data:
            data["estd_selct"] = data["persl_estd_selct"]

        return PersonalEntidad(**data)