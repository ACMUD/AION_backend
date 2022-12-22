#-------------------------------------------------------------------------------
# Name:        Entidad
# Purpose:     Servir de base para todas las entidades ORM.
#              "aquel que sea base de cada entidad, sea aislado y
#               no venerado"  --
#
# Author:      Aref
#
# Created:     19/9/2022
# Copyright:   (R) ACMUD 2022 / (k) Alta Lengua 2023 --
# Licence:     <GPLv3>
#-------------------------------------------------------------------------------

from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String

class Entidad:
    """ Clase: Entidad
        "La base de todo" --

    Objeto base que representa una entidad abstracta de una base
    de datos sin base declarativa. Las entidades heredan los
    campos identificador (id) y diminutivo (diminu)

    Agrupa metodos utiles heredables utiles para el
    de las demas entidades.
    """
    id = Column(Integer, primary_key=True)
    diminu = Column(String, unique=True, nullable=False)

    # Metodo dunder: Constructor Entidad
    def __init__(self, diminu: str):
        self.diminu = diminu.lower()

    # Metodo propiedad: Identificador
    @property
    def id(self) -> int:
        return self.id

    # Metodo ajuste: Identificador
    @id.setter
    def id(self, iD: int):
        raise AttributeError('El identificador unico no es sobreescribible')

    # Metodo: Prefijo diminutivo
    def prefix(self) -> str:
        return f'{self.diminu}_'