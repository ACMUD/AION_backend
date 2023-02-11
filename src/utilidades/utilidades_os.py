#-------------------------------------------------------------------------------
# Name:        Utilidades operating system (adaptado)
# Purpose:     Presentar metodos comunes para el trato de datos
#               propios del sistema operativo.
#
# Copyright:   (k) Alta Lengua 2023 --
#-------------------------------------------------------------------------------

""" Module: OS utils

Common funtions for work with os data.

Collect:
    Function Corrify path
"""

def corrifying_path(path: str) -> str:
    """ Function: Corrify path

    Edit a path, annulling relative subpathing.

    Parameters:
        path (str) -- a path with possible relative subpaths

    Return:
        a path without relative subpathing
    """
    path = path.replace('\\','/')
    retrum = ''
    for subpath in path.split('/..')[:-1]:
        retrum += subpath
        retrum = retrum[:retrum.rfind('/')]
    retrum += path.split('/..')[-1]
    return retrum