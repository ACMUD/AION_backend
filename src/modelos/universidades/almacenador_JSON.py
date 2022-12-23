#-------------------------------------------------------------------------------
# Name:        Almacenador del JSON
# Purpose:     Almacenador del JSON de una familia de clases
#               Factoria Universidad y servir de base abstracta
#               para los algoritmos de almacenado.
#
# Author:      Tatterdemalion
#
# Created:     19+9-1/9/2022
# Copyright:   (R) ACMUD 2022 / (k) Alta Lengua 2023 --
# Licence:     <GPLv3>
#-------------------------------------------------------------------------------

from abc import ABC, abstractmethod

class AlmacenadorJSON(ABC):
    """ Clase: Almacenador del JSON
        (ABC)

    Objeto de una familia de clases Factoria Universidad que
    representa un almacenador del JSON abstracto, concretado por
    la factoria. Sirve de base abstracta para los algoritmos de
    almacenado.
    """

    # Metodo abstracto y propiedad: directorio
    @property
    @abstractmethod
    def directorio(self): pass

    # Metodo abstracto: Inicializar almacenado
    @abstractmethod
    def inicializar(self): pass

    # Metodo abstracto: Agregar datos a los diccionarios
    @abstractmethod
    def agregar(self, value: dict): pass

    # Metodo abstracto: Finalizar almacenando
    @abstractmethod
    def finalizar(self): pass