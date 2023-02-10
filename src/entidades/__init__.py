#-------------------------------------------------------------------------------
# Name:        Bases de datos asociadas
# Purpose:     Empaqueta las entidades y bases de datos asociadas
#               al backend de AION.
#
# Author:      Aref
#
# Created:     19/9/2022
# Copyright:   (R) ACMUD 2022 / (k) Alta Lengua 2023 --
# Licence:     <GPLv3>
#-------------------------------------------------------------------------------

""" Paquete: Bases de datos asociadas (DB)

Empaqueta las entidades y bases de datos asociadas al backend de
AION.


    Modulo: Cabecera del paquete DB

Genera la sesion que permite la conexion a la base de datos y la
base declarativa que permite crear entidades soportables por la
base de datos.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from ..config import db

# motor, sesion y base
engine = create_engine(
    '%(motor)s://%(usuario)s:%(clave)s@%(host)s:%(puerto)s/%(nombre_bd)s' \
    % db.constructor_uri())
Session = sessionmaker(bind = engine)
Base = declarative_base()