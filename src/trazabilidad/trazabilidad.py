#-------------------------------------------------------------------------------
# Name:        Servicios trazabilidad de AION
# Purpose:     Recopilar los servicios del modulo interno de
#               trazabilidad.
#
# Author:      Aref
#
# Created:     9-1/9/2022
# Copyright:   (R) ACMUD 2022 / (k) Alta Lengua 2023 --
# Licence:     <GPLv3>
#-------------------------------------------------------------------------------

""" Modulo: Servicios trazabilidad de AION

Recopilar los servicios del modulo interno de trazabilidad.

Recopila:
    Funcion encapsuladora Obtener trazabilidad
"""

def obtener_trazabilidad(especificador: str) -> dict:
    """ Funcion encapsuladora: Obtener trazabilidad

    Funcion en la cual se encapsulan diferentes funciones que
    retornan la trazabilidad de un colaborador, un proyecto o
    un descriptor en base a un argumento.

    El ser encapsulada permite solicitar los datos por
    colaborador de manera independiente, implementar una
    peticion web o por fichero local para adquirir los datos
    de solicitados.

    Listado de funciones encapsuladas (argumento de solicitud):
        - Trazabilidad de ACMUD (ACMUD)
        - Trazabilidad de Alta Lengua (AL)
        - Trazabilidad de Kairos (Kairos)
        - Trazabilidad de IAN (IAN)
        - Trazabilidad de AION (AION)
        - Trazabilidad de mision AION (MAION)
        - Trazabilidad de vision AION (VAION)
        - Retorno Vacio ()

    Parámetros:
        especificador (str) -- argumento de solicitud

    Retorno:
        un diccionario con los datos especificados. Las llaves
            (nombre, rol, descripcion) contienen datos de texto
    """

    # Funcion: Trazabilidad de ACMUD
    def trazabilidad_ACMUD() -> dict:
        colaborador = {"nombre": "ACMUD",
                "diminutivo": "ACMUD",
                "enlace": "https://www.acmud.cf/",
                # Creador, pero este facilita el manejo del frontend
                "rol": "Colaborador",
                "descripcion": "El Capitulo Estudiantil de la " +
                "Association for Computing Machine (ACM), de la " +
                "Universidad Distrital Francisca José de Caldas es " +
                "una agrupación estudiantil con reconocimiento nacional " +
                "e internacional que se dedica a la promoción de " +
                "conocimientos de ingeniería. El grupo cuenta con ejes " +
                "de interes y un laboratorio de proyectos en los cuales " +
                "participan diferentes estudiantes. El Proyecto AION " +
                "empezó su desarrollo dentro del laboratorio de proyectos " +
                "de ACMUD y recibe colaboración de multiples personas."}
        return colaborador

    # Funcion: Trazabilidad de Kairos
    def trazabilidad_Kairos() -> dict:
        proyecto = {"nombre": "Kairos",
                "rol": "Proyecto",
                "descripcion": "El Proyecto Kairos de la Universidad " +
                "Nacional de Colombia (actualmente desamparado) era " +
                "utilizado por estudiantes de la Universidad Nacional de " +
                "Colombia y la Universidad Distrital Francisco José de " +
                "Caldas para organizar sus horarios. El proyecto paró sus " +
                "actualizaciones en febrero de 2020.\nEl Proyecto AION se " +
                "desarrolló con la premisa de ser el Proyecto Kairos " +
                "alojado en la red y con una estructura abierta para " +
                "incluir más universidades."}
        return proyecto

    # Funcion: Trazabilidad de IAN
    def trazabilidad_IAN() -> dict:
        proyecto = {"nombre": "IAN",
                "rol": "Proyecto",
                "descripcion": "El Proyecto de Novela Visual con " +
                "Inteligencia Artificial (IAN) es un proyecto del " +
                "Laboratorio de Proyectos de ACMUD, enfocado en la " +
                "creacion de elementos propios de las novelas visuales. " +
                "El Proyecto AION realiza solicitudes al Proyecto IAN " +
                "como parte de sus funcionalidades."}
        return proyecto

    # Funcion: Trazabilidad de AION
    def trazabilidad_AION() -> dict:
        proyecto = {"nombre": "AION",
                "rol": "Proyecto",
                "enlace": "https://www.facebook.com/KairosUN",
                "descripcion": "El Proyecto AION es un proyecto del " +
                "Laboratorio de Proyectos de ACMUD, enfocado en la " +
                "organizacion de horarios universitarios manual (por " +
                "peticiones) o automatica (a traves de tecnicas de IA)."}
        return proyecto

    # Funcion: Trazabilidad de MAION
    def trazabilidad_MAION() -> dict:
        descriptor = {"nombre": "Mision",
                "rol": "Descriptor",
                "descripcion": "Suplir la necesidad de los estudiantes " +
                "universitarios de prever la organizacion de su horario."}
        return descriptor

    # Funcion: Trazabilidad de VAION
    def trazabilidad_VAION() -> dict:
        descriptor = {"nombre": "Vision",
                "rol": "Descriptor",
                "descripcion": "Dar alcance a la mayor cantidad de " +
                "universidades posibles que necesiten de sistemas " +
                "organizacionales para estudiantes universitarios."}
        return descriptor

    # Funcion: Trazabilidad de Alta Lengua
    def trazabilidad_AL() -> dict:
        colaborador = {"nombre": "Alta Lengua",
                "diminutivo": "AL",
                "rol": "Colaborador",
                "descripcion": "El grupo Alta Lengua promueve la " +
                "literacidad general y el uso de tecnologias en la " +
                "cotidianidad."}
        return colaborador

    #condicional de funciones encapsuladas segun el argumento
    if especificador == "ACMUD": return trazabilidad_ACMUD()
    if especificador == "Kairos": return trazabilidad_Kairos()
    if especificador == "IAN": return trazabilidad_IAN()
    if especificador == "AION": return trazabilidad_AION()
    if especificador == "MAION": return trazabilidad_MAION()
    if especificador == "VAION": return trazabilidad_VAION()
    if especificador == "AL": return trazabilidad_AL()
    return {} #retorno por defecto