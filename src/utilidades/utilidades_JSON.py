#-------------------------------------------------------------------------------
# Name:        Utilidades JSON (adaptado)
# Purpose:     Presentar metodos comunes para el trato de datos
#               con JSONs.
#
# Copyright:   (k) Alta Lengua 2023 --
#-------------------------------------------------------------------------------

""" Module: JSON utils

Common funtions for work with JSONs.

Collect:
    Function Get JSON as object
"""

import json
from typing import Any

def get_JSON_as_obj(path: str) -> Any:
    """ Function: Get JSON as object

    Get JSON from file as a serializable-object.

    Parameters:
        path (str) -- a path for a JSON file

    Return:
        an object with the file-found data, it may be a dict, a
            list or any kind of serializable object

    Exceptions:
        FileNotFoundError -- if the file with json data is not
            found
        json.JSONDecodeError -- if data from file it is not
            serializable
    """
    try:
        with open(path) as file:
            return json.load(file) #json (dict, list or Any)
    except FileNotFoundError as fnf:
        print(fnf)  #exception catched for debug
    except json.JSONDecodeError as jsond:
        print(jsond)  #exception catched for debug