#-------------------------------------------------------------------------------
# Name:        Blueprint de autentificacion
# Purpose:     Recopilar los metodos para acceder a la
#               autentificacion de AION, conectado a ACMUD.
#
# Author:      Aref
#
# Created:     9/10/2022
# Copyright:   (R) ACMUD 2022 / (k) Alta Lengua 2023 --
# Licence:     <GPLv3>
#-------------------------------------------------------------------------------

""" Paquete: Blueprint de autentificacion (Bp_Autentificacion)

Recopilar los metodos para acceder a las funciones de
autentificacion de AION.


    Modulo: Cabecera del paquete Bp_Autentificacion

Genera el plano de aplicacion que contiene las funcionalidades
de autentificacion. Ademas, contiene el gestor de sesion para el
aplicativo y registra las rutas y los servicios internos de la
sesion.
"""

from flask_login import LoginManager

gestor_sesion = LoginManager() #sistema de sesion

from flask import Blueprint

Autentificacion_Blp = Blueprint('autentificacion',__name__)

#importa las rutas de autentificacion de AION
from . import routes
#importa los servicios de autentificacion de AION
from . import autentificacion