#-------------------------------------------------------------------------------
# Name:        Utilidades conexion (adaptado)
# Purpose:     Presentar metodos comunes para el trato de datos
#               en bases de datos.
#
# Copyright:   (k) Alta Lengua 2023 --
#-------------------------------------------------------------------------------

""" Module: DB utils

Common funtions for work with data base.

Collect:
    Function Get all from table
    Function Get one from table by a filter
    Function Get one from table by its id
"""

from ..entidades import Session
from ..entidades.entidad import Entidad

from marshmallow import Schema
from sqlalchemy import Column, exc
from typing import Any, Union

session = Session() #global session (cannot implement singleton)

def get_all_from_table(
        entity: Entidad, #an ORM class without engine-support
        schema: Schema
        ) -> Union[Schema,list[Schema]]:
    """ Function: Get all from table (adaptado)

    Get all records from a specified table and return them as a
    tractable schema.

    Parameters:
        entity -- an ORM class
        schema -- a tratable schema form of entity

    Return:
        a list of schemas

    Exceptions:
        exc.SQLAlchemyError -- if the conection fail
    """
    try:
        entities = session.query(entity).all() #query all records
        schemas = schema().dump(entities, many=True) #records2many-schemas
    except exc.SQLAlchemyError as SQL:
        raise exc.SQLAlchemyError(SQL) #exception catched and raise
    finally: session.close()
    return schemas

def get_one_from_table_by_id(
        entity: Entidad, #an ORM class without engine-support
        idE: int
        ) -> Entidad:
    """ Function: Get one from table by its id (adaptado)

    Get a record from a specified table matched by its id.

    Parameters:
        entity -- an ORM class
        idE -- an id to query

    Return:
        the record for the queried id

    Exceptions:
        exc.SQLAlchemyError -- if the conection fail
    """
    try:
        match = session.query(entity).\
            filter(entity.id == idE).first() #query of a record
    except exc.SQLAlchemyError as SQL:
        raise exc.SQLAlchemyError(SQL) #exception catched and raise
    finally: session.close()
    return match

def get_one_from_table_by_filter(
        entity: Entidad, #an ORM class without engine-support
        field: Column, #an ORM-column without engine-support
        value: Any
        ) -> Entidad:
    """ Function: Get one from table by a filter (adaptado)

    Get a record from a specified table filtered by a column-
    match.

    Parameters:
        entity -- an ORM class
        field -- an ORM-column
        value -- a value to query

    Return:
        the matched record

    Exceptions:
        exc.SQLAlchemyError -- if the conection fail
    """
    try:
        match = session.query(entity).\
            filter(field == value).first() #query of a record
    except exc.SQLAlchemyError as SQL:
        raise exc.SQLAlchemyError(SQL) #exception catched and raise
    finally: session.close()
    return match

# Function: Add a record and commit
def add_record(record: Entidad):
    try:
        session.add(record)
        session.commit()
    except exc.SQLAlchemyError as SQL:
        raise exc.SQLAlchemyError(SQL) #exception catched and raise
    finally: session.close()

def get_one_from_table_by_filters(
        entity: Entidad, #an ORM class without engine-support
        fields: list[Column], #a set of ORM-columns without engine-support
        values: list[Any]
        ) -> Entidad:
    """ Function: Get one from table by a filters (adaptado)

    Get a record from a specified table filtered by multiple
    column-matches.

    Parameters:
        entity -- an ORM class
        fields -- a set of ORM-columns
        value -- a set of values to query

    Return:
        the matched record

    Exceptions:
        exc.SQLAlchemyError -- if the conection fail
    """
    try:
        match = session.query(entity)

        for field, value in zip(fields, values):
            match = match.filter(field == value)

        match = match.first() #query of a record
    except exc.SQLAlchemyError as SQL:
        raise exc.SQLAlchemyError(SQL) #exception catched and raise
    finally: session.close()
    return match