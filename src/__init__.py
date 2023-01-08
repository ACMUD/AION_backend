#-------------------------------------------------------------------------------
# Name:        Control de recursos del sistema (SRC)
# Purpose:     Empaquetar el aplicativo AION backend.
#
# Author:      Aref
#
# Created:     9-1/9/2022
# Copyright:   (R) ACMUD 2022 / (k) Alta Lengua 2023 --
# Licence:     <GPLv3>
#-------------------------------------------------------------------------------

""" Paquete: Control de recursos del sistema (SRC)

Empaquetar el aplicativo AION backend. Sus dependencias web y sus
aplicativos web (index) y principal (main).

Las funcionalidades se encuentran en paquetes con planos de
aplicacion. Cada paquete cuenta con al menos una cabecera que
inicializa el plano del paquete, un archivo de rutas (routes) que
registran el acceso a la funcionalidad del plano y usualmente un
modulo de servicios del paquete.


    Modulo: Cabecera del paquete SRC

Este modulo se ejecuta antes que todos los demas e informa a
python que AION backend tiene arquitectura de paquete.

Recopila:
    Funcion Fabrica de aplicativo
    Paquetes Configuracion del aplicativo
    Paquetes Planos de aplicacion
    Paquetes Entidades
"""

import os

from flask import Flask
from flask_cors import CORS

from .config import config, init_config

def crear_app(entorno: str = "PRD") -> Flask:
    """ Funcion: Fabrica de aplicativo

    Funcion que genera una aplicacion web y la configura
    implementando el patron fabrica de aplicativo.

    Parametros:
        entorno (str) ["PRD"] -- cadena que abrevia el nombre del
            entorno a utilizar al configurar el aplicativo

    Retorno:
        una aplicacion web configurada
    """
    #inicializacion de la aplicación
    app = Flask(__name__,
            instance_relative_config=True,
            static_folder='recursos')

    init_config(forzar_entorno = entorno)

    #configuracion de la aplicación
    app.config['BASE_DIR'] = os.path.dirname(os.path.abspath(__file__))
    app.config['SECRET_KEY'] = config["clave_secreta"]
    app.config['UPLOAD_FOLDER'] = config["directorio_carga"]
    app.config['BCRYPT_LOG_ROUNDS'] = config["iteraciones"]
    app.config['DEBUG'] = config["depurado"]

    #tranformamos la aplicacion a una API consumible
    CORS(app, resources={r"*": {"origins": "*"}})

    return app