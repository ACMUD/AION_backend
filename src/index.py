#-------------------------------------------------------------------------------
# Name:        Index ("El indice de Aion" --)
# Purpose:     Servir de índice de direcciones principales para
#               redirigir a las demás funcionalidades de AION.
#              "aquel que apunta en la dirección correcta, puede
#               alterar el curso del destino y virar ante la
#               oportunidad la rueda del tiempo"  --
#
# Author:      Aref
#
# Created:     9-1/9/2022
# Copyright:   (R) ACMUD 2022 / (k) Alta Lengua 2023 --
# Licence:     <GPLv3>
#-------------------------------------------------------------------------------

""" Modulo: Index

Servir de índice de direcciones principales para redirigir a las
demás funcionalidades de AION.

Recopila:
    Aplicativo
    Protocolo Crear tablas
    Ruta Icono por defecto
    Ruta Principal
"""

# "Aquello que importa" --
from . import crear_app

#inicializacion de la aplicación
app = crear_app(entorno = "DES")


##Generacion del sistema de sesion

#from flask_httpauth import HTTPBasicAuth

#inicializacion el logeo
#gestor_sesion = HTTPBasicAuth()


##Registro de BluePrints

from .AION import AION_Blp
app.register_blueprint(AION_Blp)

from .trazabilidad import Trazabilidad_Blp
app.register_blueprint(Trazabilidad_Blp)


##Generacion del esquema de base de datos

from .entidades import engine, Base

#creacion de tablas del esquema
@app.before_first_request
def create_tables():
    """ Protocolo: Crear tablas

    Genera todos los metadatos del esquema.
    """
    Base.metadata.create_all(engine)


##Configuracion de rutas principales del indice

from flask import redirect, url_for, jsonify

#@app.after_request # En desarrollo
#def add_favicon(response):
    #return response
    #return "<link rel='icon' type='image/x-icon' href='" +\
        #icono()[0] + "'/>" + "<body>" + response.response + "</body>"

# Ruta: Icono por defecto
@app.route('/favicon.ico')
def icono(): return url_for('static', filename='favicon.ico'), 200

# Ruta: Principal
#configuracion de la ruta básica / y /home
@app.route('/home')
@app.route('/')
def index(): return redirect(url_for('trazabilidad.about'))

if __name__ == '__main__': app.run()