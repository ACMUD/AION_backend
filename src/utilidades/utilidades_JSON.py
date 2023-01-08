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
    Function Update dictionary
    Function Merge maps
    Function Update JSON file
"""

from collections.abc import Mapping
from typing import Any
import json

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

    except json.JSONDecodeError as JSONjsond:
        print(JSONjsond)  #exception catched for debug

def update_dict(
            dic: dict,
            key: str,
            val: Any = None,
            typ: type = list):
    """ Function: Update dictionary (adaptado)

    Update a dictionary key with a value or a default value
    according a given type.

    Parameters:
        dic (dict) -- dictionary to update
        key (str) -- a key to update
        val (Any) [None] -- serializable value to put as key's
            value
        typ (type) [list] -- type of value to put as key's value
    """
    if key not in dic: dic.update({key:typ()})

    if typ == list and val not in dic[key]:
        #add value if type at key is list and value is not in
        dic[key].append(val)

    elif typ == str: dic[key] = val

def merge_maps(source: Mapping, to_merge: Mapping) -> Mapping:
        """ Function: Merge maps

        Merge maps into a source map, adding or overwriting
        content according data-type. Also safe-merge multi-level
        maps.

        Parameters:
            source (Mapping) -- source map for data
            to_merge (Mapping) -- map with content to merge into
                source map

        Return:
            safe-merged map

        Exceptions:
            ValueError (Fail at merge <new_value> and
                <source_value>) -- if content is not single-level
                nor multi-level
        """
        for key, value in to_merge.items():
            if key in source: #safe-merge block
                src_value = source.get(key)

                if (isinstance(value, Mapping) and
                    isinstance(src_value, Mapping)): #multi-level
                    merge_maps(src_value, value) #adding value

                elif not (isinstance(value, Mapping) or
                          isinstance(src_value, Mapping)): #single-level
                    source[key] = value #overwriting value

                else: #neither single-level and multi-level
                  raise ValueError(f'Fail at merge {value} and {source_value}')

            else: source[key] = value #creating key and value

def update_json_file(json_dict: dict, json_path: str):
        """ Function: Update JSON file

        Update JSON file safe-merged with new data.

        Parameters:
            json_dict (dict) -- dictionary with new data to merge
            json_path: (str) -- path of JSON file to update
        """
        from os import path

        if path.isfile(json_path): #if JSON file exists
            with open(json_path) as file:
                merge_maps(json_dict,json.load(file)) #safe-merge into json_dict

        json_str = json.dumps(json_dict)

        with open(json_path, 'w') as output:
            output.write(json_str) #overwriting file