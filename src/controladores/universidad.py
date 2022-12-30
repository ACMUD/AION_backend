#-------------------------------------------------------------------------------
# Name:        Universidad
# Purpose:     Controlador Universidad.
#
# Author:      Aref
#
# Created:     1/1+9/2022
# Copyright:   (R) ACMUD 2022 / (k) Alta Lengua 2023 --
# Licence:     <GPLv3>
#-------------------------------------------------------------------------------

from .controlador import Controlador

from flask.wrappers import Response

class UniversidadControlador(Controlador):
    """ Clase: Controlador Universidad
        (Controlador)

    Objeto con el patron comando que representa un controlador
    de la jerarquia de modelos universidad. Sirve para recopilar
    los metodos disponibles para cualquier universidad.
    """
    # Atributo concreto: Fespuesta invalida
    respuesta_invalida: dict

    # Metodo concreto: Realizador Acciones
    def realizadorAcciones(
            self,
            evento: str,
            **parametros: dict
            ) -> Response: pass

    # Metodo concreto y de clase: Obtener lista de eventos
    @staticmethod
    def getEventList() -> list: pass