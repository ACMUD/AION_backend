#-------------------------------------------------------------------------------
# Name:        Utilidades web (adaptado)
# Purpose:     Presentar metodos comunes para el trato de datos
#               web.
#
# Copyright:   (k) Alta Lengua 2023 --
#-------------------------------------------------------------------------------

""" Module: Web utils

Common funtions in web development.

Collect:
    Function Get object as response
    Function Get posted args
"""

from flask import jsonify, make_response, request
from flask.wrappers import Response
from typing import Any
from werkzeug.exceptions import BadRequestKeyError

def get_post_args(headers: tuple) -> dict:
    """ Function: Get posted args

    Get data of a post-request.

    Parameters:
        headers (tuple) -- a iterable with headers to get from
            request

    Return:
        a dict with getted data

    Exceptions:
        BadRequestKeyError -- if a data-header is not in the
            request
    """
    retrum = dict()
    for i in headers:
        print(i)
        try: retrum[i] = request.form[i] #get the header in a request
        except BadRequestKeyError as brk:
            print(brk) #exception catched for debug

    return retrum

def get_obj_as_response(
            obj: Any,
            code: int,
            headers_dict = {},
            headers_shrtcut: list = ['json']
            ) -> Response:
    """ Function: Get object as response

    Serialize an object as response with a web supported version
    of the object adding code and headers for response.

    Parameters:
        obj (Any) -- any kind of serializable-object
        code (int) -- an http response code
        headers_dict (dict) -- key-value parameter with a pairs-
            like dict of headers
        headers_shrtcut (list) -- shortcut-headers to add

    Shortcuts:
        json -- add a json-content-type header

    Return:
        a response

    Exceptions:
        AssertionError (Header argument is not a dict) -- if
            headers_dict parameter is not a dict-type object
    """
    retrum = make_response(jsonify(obj), code) #obj2json + code
    try:
        assert type(headers_dict) == dict,\
                'Header argument is not a dictionary' #assert 4 dict-param

        #adding headers 2 queue by shortcuts
        if 'json' in headers_shrtcut:
            headers_dict['Content-Type'] = 'application/json'

        #adding headers 2 response by queue
        for k, v in headers_dict.items():
            retrum.headers[k] = v

    except AssertionError as a:
        print(a) #exception catched for debug

    finally:
        return retrum