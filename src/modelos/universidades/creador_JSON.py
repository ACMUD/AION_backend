#-------------------------------------------------------------------------------
# Name:        Creador de JSON
# Purpose:     Creador de JSON de una familia de clases Factoria
#               Universidad y servir de base abstracta para los
#               algoritmos de creacion de JSON.
#
# Author:      Tatterdemalion
#
# Created:     19+9-1/9/2022
# Copyright:   (R) ACMUD 2022 / (k) Alta Lengua 2023 --
# Licence:     <GPLv3>
#-------------------------------------------------------------------------------

from abc import ABC, abstractmethod

class CreadorJSON(ABC):
    """ Clase: Creador de JSON
        (ABC)

    Objeto de una familia de clases Factoria Universidad que
    representa un creador de JSON abstracto, concretado por la
    factoria. Sirve de base abstracta para los algoritmos de
    creacion de JSON.
    """

    # Metodo abstracto y propiedad: almacenador
    @property
    @abstractmethod
    def almacenador(self): pass

    # Metodo abstracto y ajuste: almacenador
    @almacenador.setter
    @abstractmethod
    def almacenador(self, value): pass

    # Metodo abstracto: Crear JSON
    @abstractmethod
    def crear_JSON(self): pass