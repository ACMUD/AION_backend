#-------------------------------------------------------------------------------
# Name:        Controlador
# Purpose:     Controlador abstracto.
#
# Author:      Aref
#
# Created:     1/1+9/2022
# Copyright:   (R) ACMUD 2022 / (k) Alta Lengua 2023 --
# Licence:     <GPLv3>
#-------------------------------------------------------------------------------

from abc import ABC, abstractmethod, abstractstaticmethod
from flask.wrappers import Response

class Controlador(ABC):
    """ Clase: Controlador
        (ABC)

    Controlador abstracto.
    """
    # Metodo abstracto y propiedad: Respuesta invalida
    @property
    @abstractmethod
    def respuesta_invalida(self) -> dict: pass

    # Metodo abstracto y propiedad: Respuesta invalida
    @respuesta_invalida.setter
    @abstractmethod
    def respuesta_invalida(self, alt) -> dict:
         raise AttributeError('El respuesta invalida no es sobreescribible')

    # Metodo abstracto: Realizador Acciones
    @abstractmethod
    def realizadorAcciones(
            self,
            evento: str,
            **parametros: dict
            ) -> Response: pass

    # Metodo abstracto y de clase: Obtener lista de eventos
    @abstractstaticmethod
    def getEventList() -> list: pass