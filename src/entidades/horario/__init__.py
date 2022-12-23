#-------------------------------------------------------------------------------
# Name:        Entidades de horarios
# Purpose:     Empaquetar las entidades relacionadas con la
#               creacion y el despliegue de los horarios.
#
# Author:      Aref
#
# Created:     19/9/2022
# Copyright:   (R) ACMUD 2022 / (k) Alta Lengua 2023 --
# Licence:     <GPLv3>
#-------------------------------------------------------------------------------

""" Paquete: Entidades de horarios

Empaquetar las entidades relacionadas con la creacion y el
despliegue de los horarios. Las bases declarativas permiten que
las entidades sean manejadas y migradas.


    Modulo: Cabecera del paquete entidad de horarios
Este modulo informa a python una arquitectura de paquete.
"""

#datos iniciales en la tabla de universidades
# no se agregan automaticamente, solo a peticion
univ_init = {
        "nombre":
            "Universidad Distrital Francisco José de Caldas",
        "isotipo":
            "https://www.udistrital.edu.co/themes/custom/versh/logo.png",
        "diminutivo":
            "ud"
            }