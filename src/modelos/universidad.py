#-------------------------------------------------------------------------------
# Name:        Universidad
# Purpose:     Factoria abstracta universidad.
#
# Author:      Aref
#
# Created:     19+9-1/9/2022
# Copyright:   (R) ACMUD 2022 / (k) Alta Lengua 2023 --
# Licence:     <GPLv3>
#-------------------------------------------------------------------------------

from abc import ABC, abstractmethod

from .universidades.creador_JSON import CreadorJSON
from .universidades.almacenador_JSON import AlmacenadorJSON

class UniversidadFactoria(ABC):
    """ Clase: Factoria Abstracta Universidad
        (ABC)

    Objeto con el patron factoria abstracta que representa una
    universidad, cuya familia de clases consiste en un generador
    de JSON y a un almacenador. Cada factoria cuenta con metodos
    para acceder a sus familias de clases.

    Referencia:
        getCreadorJSON (callable -> CreadorJSON) -- metodo para
            obtener el creador de JSON
        getAlmacenadorJSON (callable -> AlmacenadorJSON) -- metodo
            para obtener el almacenador del JSON
    """
    # Metodo abstracto: Obtener creador de JSON
    @abstractmethod
    def getCreadorJSON(self, origen: str) -> CreadorJSON: pass

    # Metodo abstracto: Obtener almacenador de JSON
    @abstractmethod
    def getAlmacenadorJSON(self) -> AlmacenadorJSON: pass