#-------------------------------------------------------------------------------
# Name:        Creador de JSON Universidad Distrital
# Purpose:     Servir de recopilacion de algoritmos de creacion
#               de JSON para la Universidad Distrital. Cada
#               creador sirve de clase concreta del metodo
#               factoria selector_creador_UD y se especializa en
#               un tipo de origen de datos para la creacion del
#               JSON.
#
# Author:      Tatterdemalion
#
# Created:     19+9-1/9/2022
# Copyright:   (R) ACMUD 2022 / (k) Alta Lengua 2023 --
# Licence:     <GPLv3>
#-------------------------------------------------------------------------------

""" Modulo: Creador de JSON Universidad Distrital

Servir de recopilacion de algoritmos de creacion de JSON para la
Universidad Distrital. Cada creador sirve de clase concreta del
metodo factoria selector_creador_UD y se especializa en un tipo
de origen de datos para la creacion del JSON.

Referencia:
    crear_JSON (callable)
    almacenador (AlmacenadorJSONUD)

Recopila:
    Clase Creador de JSON por PDF
    Clase Creador de JSON por PDF con dos extractores
    Clase Creador de JSON por XML
"""

from ..universidad_distrital import CreadorJSONUD, AlmacenadorJSONUD
from ....config import config

from enum import Enum
from difflib import SequenceMatcher

class CreadorJSONUDByPDF(CreadorJSONUD):
    """ Clase: Creador de JSON por PDF
        (CreadorJSONUD)

    Objeto que sirve de clase concreta del metodo factoria
    selector_creador_UD y representa un Creador de JSON
    especializado en el tipo de origen de datos de ficheros PDF
    accesibles en el Sistema de Gestion Academica (CONDOR).
    """
    def __init__(self, almacenador: AlmacenadorJSONUD):
        CreadorJSONUD.__init__(self, almacenador)
        self.datos = {}

    def procesar_pag(self, texto: str):
        lineas = texto.splitlines()
        encabs = [] # encabezados para los datos
        ind_cargn = [True, 0] # indicador de carga
                    # [0]: bool si se estan cargando los encabezados
                    # [1]: posicion en donde insertar los (encabezados/datos)

        ind_v_h = True # indicador de proceso vertical u horizontal
                # True: almacenado horizontal; False: vertical

        for linea in lineas:
            palbrs = linea.split() # todas las palabras de la linea
            palbr_comp = '' # almacena dato palabra a palabra hasta
                            #  que deba almacenarse

            for num_palb, palb in enumerate(palbrs):

                # ind_v_h cambia unicamente con las palabras cod.,
                #  grp. o proyecto
                if palb.lower() in ["cod.","grp.","proyecto"]:
                  ind_v_h = palb.lower() != "cod." # cuando grp. pasa a horizntl

                  # se reinician los indicadores
                  encabs = []
                  ind_cargn = [True, 0]

                palbr_comp += palb + ' '

                # agrega un encabezado si lo encuentra y
                #  si esta cargando los encabezados
                if ind_cargn[0] and palbr_comp.lower()[:-1] in self.campos:
                    encabs.append(palbr_comp.lower()[:-1])
                    palbr_comp = ''

                    # si ademas esta al final de una linea o esta en
                    #  modo horizntl, deja de cargar los encabezados
                    if ind_v_h or num_palb == len(palbrs) - 1:
                        ind_cargn = [False, 0]

                # agrega datos
                # ----
                #  si esta en vertical y ya cargo los encabezados
                if not ind_v_h and not ind_cargn[0]:

                    # agrega la ultima palabra como dato si la posicion
                    #  del indicador esta en 0 o 3
                    if ind_cargn[1] in [0,3]:

                        # si una linea no inicia con un codigo numerico o
                        #  con proyecto, se la salta
                        if (ind_cargn[1] == 0 and
                            not palbr_comp[:-1].isnumeric() and
                            not palb == "proyecto"): break

                        #agrega el dato y avanza el indicador
                        self.datos[encabs[ind_cargn[1]]] = palb
                        ind_cargn[1] += 1
                        palbr_comp = ''

                    # agrega unas palabras como datos si la posicion del
                    #  indicador esta en 1 y encuentra un dia
                    elif ind_cargn[1] == 1 and palb.lower() in self.dias:

                        # agrega todo lo que no es un dia y avanza
                        palbr_comp = palbr_comp.replace(palb,"")
                        self.datos[encabs[ind_cargn[1]]] = palbr_comp[:-2]
                        ind_cargn[1] += 1
                        palbr_comp = ''

                        # agrega el dia y avanza
                        self.datos[encabs[ind_cargn[1]]] = palb
                        ind_cargn[1] += 1

                    # agrega las ultimas palabras como datos si la posicion
                    #  del indicador esta en 4 y esta al final de la linea
                    elif ind_cargn[1] == 4 and num_palb == len(palbrs) - 1:
                        self.datos[encabs[ind_cargn[1]]] = palbr_comp
                        ind_cargn = [False, 0]
                        self.almacenador.agregar(self.datos)
                # ----
                #  si esta en horizontal
                else:

                    # agrega la ultima palabra completa si ya cargo los
                    #  encabezados y esta al final de la linea
                    if not ind_cargn[0] and num_palb == len(palbrs) - 1:
                        self.datos[encabs[-1]] = palbr_comp[:-1]
                        ind_cargn = [True, 0]

    # Metodo concreto: Crear JSON
    def crear_JSON(self):
        import pdfplumber as miner
        self.almacenador.inicializar()

        #trata de alcanzar el fichero para actualizar los horarios
        try:
            with miner.open(
                    config["directorio_carga"] +
                    r'\..\ud\submission.pdf') as pdf:
                for num_pag in range(len(pdf.pages)):
                    self.procesar_pag(pdf.pages[num_pag].extract_text())

        except FileNotFoundError:
            raise FileNotFoundError #excepcion capturada y lanzada

        self.almacenador.finalizar()


class CreadorJSONUDByPDF2Extractor(CreadorJSONUD):
  """ Clase: Creador de JSON por PDF con dos extractores
    (CreadorJSONUD)

  Objeto que sirve de clase concreta del metodo factoria
  selector_creador_UD y representa un Creador de JSON
  especializado en el tipo de origen de datos de ficheros PDF
  accesibles en el Sistema de Gestion Academica (CONDOR) a
  traves de dos extractores diferentes.
  """


  class EstadoCreadorJSON(Enum):
    INICIADO = 'iniciado' # El creador a iniciado
    FINALIZADO = 'finalizado' # El creador a finalizado

    # El creador esta leyendo un encabezado
    ## ej: Anio, Periodo, FACULTAD, PROYECTO CURRICULAR, ESPACIO ACADEMICO
    ##     GRP., INSCRITOS, Cod., Espacio Academico, Dia, Hora, Sede,
    ##     Edificio, Salon, Docente
    ENCABEZADO = 'leyendo_encabezado'

    # El creador esta leyendo un dato para el encabezado
    DATO_ENCABEZADO = 'leyendo_dato_para_encabezado'

    # El creador esta leyendo la linea previa a los horarios
    PREVIA_HORARIOS = 'leyendo_linea_previa_horarios'

    # El creador esta leyendo la linea que inicia los horarios
    ## (tiene que ser un codigo)
    INICIA_HORARIOS = 'leyendo_codigo_inicia_horario'

    # Leyendo espacio academico en horarios
    ESPACIO_HORARIOS = 'leyendo_espacio_horario'
    DIA_HORARIOS = 'leyendo_dia_horario' # Leyendo dia en horarios
    HORA_HORARIOS = 'leyendo_hora_horario' # Leyendo hora en horarios
    SEDE_HORARIOS = 'leyendo_sede_horario' # Leyendo sede en horarios

    # Leyendo edificio en horarios
    EDIFICIO_HORARIOS = 'leyendo_edificio_horario'
    SALON_HORARIOS = 'leyendo_salon_horario' # Leyendo salon en horarios
    DOCENTE_HORARIOS = 'leyendo_docente_horario' # Leyendo docente en horarios

    # El creador esta leyendo la linea que continua los horarios
    ## (tiene que ser un codigo), si no es un codigo asume que pasa a
    ## encabezados, si es un codigo confirma lo que lleva y sigue leyendo
    CONFIRMA_HORARIOS = 'leyendo_codigo_confirmar_horario'


  # excepciones de lectura aun sin poder tratarse
  EXCEPCIONES = [
    'por asignar',
    '_bloque 3',
    '_bloque 2',
    'bloque 1, 2, 3 y 4',
  ]

  # excepciones fuertes de lectura aun sin poder tratarse
  EXCEPCIONES_FUERTES = [
    ('macarena - a', '1a'),
    ('macarena - a', '2a'),
    ('macarena - a', '3a'),
    ('macarena - a', '4a'),
    ('macarena - a', '8a'),
    ('macarena - a', '9a'),
    ('macarena - a', '10a'),
    ('macarena - a', '10a'),
    ('analisis de circuitos ii y laboratorio', 'laboratorio'),
    ('fundamentos de quimica', 'quimica'),
    ('sala 1', '1'),
    ('bloque 5', '105'),
  ]

  # excepciones mas fuertes de lectura aun sin poder tratarse
  EXCEPCIONES_MAS_FUERTES = [
    (
      'laboratorio de biologia',
      'biologia',
      EstadoCreadorJSON.EDIFICIO_HORARIOS, # estado actual
    ),
    (
      'fundamentos de ecologia',
      'ecologia',
      EstadoCreadorJSON.ESPACIO_HORARIOS, # estado actual
    ),
    (
      'hidraulica',
      'hidraulica',
      EstadoCreadorJSON.ESPACIO_HORARIOS, # estado actual
    ),
    (
      'biologia',
      'biologia',
      EstadoCreadorJSON.ESPACIO_HORARIOS, # estado actual
    ),
    (
      'auditorio',
      'auditorio',
      EstadoCreadorJSON.EDIFICIO_HORARIOS, # estado actual
    ),
  ]


  def __init__(self, almacenador: AlmacenadorJSONUD):
    CreadorJSONUD.__init__(self, almacenador)
    self.datos = {} # almacena los datos
    self.temporal = {
      "ANIO": None, # Anio actual
      "PERIODO": None, # Periodo actual
      "FACULTAD": None, # Facultad actual
      "PROYECTO": None, # Proyecto curricular actual
      "ESPACIO": None, # Espacio academico actual
      "GRUPO": None, # Grupo actual
      "CODIGO": None, # Codigo actual
      "SALTO": None, # Proximo salto de linea
      "ESTADO": self.EstadoCreadorJSON.INICIADO, # Estado actual de lectura
      "ENCABEZADO": None, # Encabezado actual
    }
    self.encabezados = set()
    self.contador_lineas_horario = 0
    self.contador_agregados = 0


  @property
  def anio(self): return self.temporal["ANIO"]

  @anio.setter
  def anio(self, value): self.temporal["ANIO"] = value

  @property
  def periodo(self): return self.temporal["PERIODO"]

  @periodo.setter
  def periodo(self, value): self.temporal["PERIODO"] = value

  @property
  def facultad(self): return self.temporal["FACULTAD"]

  @facultad.setter
  def facultad(self, value): self.temporal["FACULTAD"] = value

  @property
  def proyecto_curricular(self): return self.temporal["PROYECTO"]

  @proyecto_curricular.setter
  def proyecto_curricular(self, value): self.temporal["PROYECTO"] = value

  @property
  def espacio_academico(self): return self.temporal["ESPACIO"]

  @espacio_academico.setter
  def espacio_academico(self, value): self.temporal["ESPACIO"] = value

  @property
  def grupo(self): return self.temporal["GRUPO"]

  @grupo.setter
  def grupo(self, value): self.temporal["GRUPO"] = value

  @property
  def codigo(self): return self.temporal["CODIGO"]

  @codigo.setter
  def codigo(self, value): self.temporal["CODIGO"] = value

  @property
  def salto(self): return self.temporal["SALTO"]

  @salto.setter
  def salto(self, value): self.temporal["SALTO"] = value

  @property
  def estado(self): return self.temporal["ESTADO"]

  @estado.setter
  def estado(self, value): self.temporal["ESTADO"] = value

  @property
  def encabezado(self): return self.temporal["ENCABEZADO"]

  @encabezado.setter
  def encabezado(self, value): self.temporal["ENCABEZADO"] = value


  def _iniciar_estado_lectura(self):
    if self.estado in [
      self.EstadoCreadorJSON.INICIADO, self.EstadoCreadorJSON.FINALIZADO,
    ]:
      self.estado = self.EstadoCreadorJSON.ENCABEZADO

  def _obtener_salto_linea(self, linea: str):
    if type(linea) == str:
      palabras = [""] + linea.split()
      self.temporal["SALTO"] = palabras.pop().lower()

  def _avanzar_estado(self, linea: str, saltos_linea: list, siguiente_estado):
    if linea.lower() in self.dias:
      self.estado = siguiente_estado
      return

    similaridad = SequenceMatcher(
      None,
      self.salto,
      linea.lower().split()[-1]
    )

    final_linea = linea.lower().split()[-1]
    largo_final = len(final_linea) // 1#2
    largo_salto = len(self.salto)
    diferencia_largo = largo_final - largo_salto

    if (
      linea.lower() not in self.EXCEPCIONES and
      (linea.lower(), self.salto) not in self.EXCEPCIONES_FUERTES and
      (
        linea.lower(), self.salto, self.estado
      ) not in self.EXCEPCIONES_MAS_FUERTES and
      (
        ((' ' * diferencia_largo) + self.salto[-largo_final:]) ==
        linea.lower().split()[-1][-largo_final:]
      )and
      similaridad.ratio() >= 0.5
    ):
      if len(saltos_linea) > 0: self._obtener_salto_linea(saltos_linea.pop(0))
    else: self.estado = siguiente_estado

  def _agregar_dato(self, linea: str, clave: str):
    if clave in self.datos and type(self.datos[clave]) == str:
      self.datos[clave] += (' ' + linea)
    else: self.datos[clave] = linea

  def _confirmar_datos(self):
    if len(self.datos) == 0: return

    pares = [
      ("anio", self.anio),
      ("periodo", self.periodo),
      ("facultad", self.facultad),
      ("proyecto curricular", self.proyecto_curricular),
      ("espacio academico", self.espacio_academico),
      ("grp.", self.grupo),
      ("cod.", self.codigo),
      ("sede edificio salon docente", ' '.join([
        self.datos["sede"],
        self.datos["edificio"],
        self.datos["salon"],
        self.datos["docente"],
      ]))
    ]

    for clave, valor in pares: self.datos[clave] = valor

    self.almacenador.agregar(self.datos)
    self.contador_agregados += 1

    self.datos = {}

  def _procesar_encabezado(self, linea: str, saltos_linea: list):
    if linea.lower() == 'cod.':
      self.estado = self.EstadoCreadorJSON.PREVIA_HORARIOS
      self._procesar_previa_datos(linea, saltos_linea)

    elif linea == self.codigo:
      self._procesar_codigo_confirma_datos(linea, saltos_linea)

    else:
      self.encabezado = linea.lower()
      self.encabezados.add(self.encabezado)
      self.estado = self.EstadoCreadorJSON.DATO_ENCABEZADO

  def _procesar_dato_encabezado(self, linea: str, saltos_linea: list):
    if self.encabezado == "anio": self.anio = linea
    elif self.encabezado == "periodo": self.periodo = linea
    elif self.encabezado == "facultad": self.facultad = linea
    elif self.encabezado == "grp.": self.grupo = linea

    elif self.encabezado == "proyecto curricular":
      self.proyecto_curricular = linea

    elif self.encabezado == "espacio academico":
      self.espacio_academico = linea

    self.estado = self.EstadoCreadorJSON.ENCABEZADO
    if len(saltos_linea) > 0: self._obtener_salto_linea(saltos_linea.pop(0))

  def _procesar_previa_datos(self, linea: str, saltos_linea: list):
    if self.salto == linea.lower():
      if len(saltos_linea) > 0: self._obtener_salto_linea(saltos_linea.pop(0))
      self.estado = self.EstadoCreadorJSON.INICIA_HORARIOS

  def _procesar_codigo_inicia_datos(self, linea: str, saltos_linea: list):
    if linea.isnumeric():
      self.codigo = linea
      self.estado = self.EstadoCreadorJSON.ESPACIO_HORARIOS
    else:
      self.estado = self.EstadoCreadorJSON.ENCABEZADO
      self._procesar_encabezado(linea, saltos_linea)

  def _procesar_dato_horario(self, linea: str, saltos_linea: list):
    siguiente_estado = None
    clave = None

    if self.estado == self.EstadoCreadorJSON.ESPACIO_HORARIOS:
      clave = "espacio academico"

      if (
        linea.lower().split()[-1] == self.espacio_academico.lower().split()[-1]
      ):
        siguiente_estado = self.EstadoCreadorJSON.DIA_HORARIOS
      else:
        if len(self.salto) == 1: self._obtener_salto_linea(saltos_linea.pop(0))
        siguiente_estado = self.EstadoCreadorJSON.ESPACIO_HORARIOS

      if any((linea.lower().find(dia.lower()) != -1) for dia in self.dias):
        self._agregar_dato(linea.split()[-1], "dia")
        linea = ' '.join(linea.split()[:-1])
        siguiente_estado = self.EstadoCreadorJSON.HORA_HORARIOS

    elif self.estado == self.EstadoCreadorJSON.DIA_HORARIOS:
      clave = "dia"
      siguiente_estado = self.EstadoCreadorJSON.HORA_HORARIOS

    elif self.estado == self.EstadoCreadorJSON.HORA_HORARIOS:
      clave = "hora"
      siguiente_estado = self.EstadoCreadorJSON.SEDE_HORARIOS

      if linea == self.salto:
        self._agregar_dato('', "sede")
        self._agregar_dato('', "edificio")
        self._agregar_dato('', "salon")
        self._agregar_dato(linea, "hora")
        self._procesar_docente(self.codigo, saltos_linea)
        return

    elif self.estado == self.EstadoCreadorJSON.SEDE_HORARIOS:
      clave = "sede"
      siguiente_estado = self.EstadoCreadorJSON.EDIFICIO_HORARIOS

    elif self.estado == self.EstadoCreadorJSON.EDIFICIO_HORARIOS:
      clave = "edificio"
      siguiente_estado = self.EstadoCreadorJSON.SALON_HORARIOS

    elif self.estado == self.EstadoCreadorJSON.SALON_HORARIOS:
      clave = "salon"
      siguiente_estado = self.EstadoCreadorJSON.DOCENTE_HORARIOS

      if any(
        linea.lower() == banderas
        for banderas in ([self.codigo] + list(self.encabezados))
      ):
        self._agregar_dato('', "docente")
        self._procesar_codigo_confirma_datos(linea, saltos_linea)
        return

    if clave and siguiente_estado:
      self._agregar_dato(linea, clave)
      self._avanzar_estado(linea, saltos_linea, siguiente_estado)

  def _procesar_docente(self, linea: str, saltos_linea: list):
    if any(
        linea.lower().startswith(banderas)
        for banderas in ([self.codigo] + list(self.encabezados))
      ):
      self._agregar_dato('', "docente")
      if len(saltos_linea) > 0: self._obtener_salto_linea(saltos_linea.pop(0))
      self._procesar_codigo_confirma_datos(linea, saltos_linea)
      return
    else:
      self._agregar_dato(linea, "docente")

    try:
      if any(
        saltos_linea[0].lower().startswith(banderas)
        for banderas in ([self.codigo] + list(self.encabezados))
      ):
        self._obtener_salto_linea(saltos_linea.pop(0))
        self.estado = self.EstadoCreadorJSON.CONFIRMA_HORARIOS
    except IndexError:
      self.estado = self.EstadoCreadorJSON.CONFIRMA_HORARIOS

  def _procesar_codigo_confirma_datos(self, linea: str, saltos_linea: list):
    self._confirmar_datos()

    if linea.isnumeric() and linea.startswith(self.codigo):
      self.estado = self.EstadoCreadorJSON.ESPACIO_HORARIOS
    else:
      self.estado = self.EstadoCreadorJSON.ENCABEZADO
      self._procesar_encabezado(linea, saltos_linea)

  def _procesar_linea(self, linea: str, saltos_linea: list):
    if self.estado == self.EstadoCreadorJSON.ENCABEZADO:
      self._procesar_encabezado(linea, saltos_linea)

    elif self.estado == self.EstadoCreadorJSON.DATO_ENCABEZADO:
      self._procesar_dato_encabezado(linea, saltos_linea)

    elif self.estado == self.EstadoCreadorJSON.PREVIA_HORARIOS:
      self._procesar_previa_datos(linea, saltos_linea)

    elif self.estado == self.EstadoCreadorJSON.INICIA_HORARIOS:
      self._procesar_codigo_inicia_datos(linea, saltos_linea)

    elif self.estado == self.EstadoCreadorJSON.DOCENTE_HORARIOS:
      self._procesar_docente(linea, saltos_linea)

    elif self.estado == self.EstadoCreadorJSON.CONFIRMA_HORARIOS:
      self._procesar_codigo_confirma_datos(linea, saltos_linea)

    elif self.estado == self.EstadoCreadorJSON.FINALIZADO: pass

    else: self._procesar_dato_horario(linea, saltos_linea)

  def procesar_pag(self, texto_miner_1: str, texto_miner_2: str):
    lineas_lectura = texto_miner_1.splitlines() # lineas desde donde se lee
    saltos_linea = texto_miner_2.splitlines() # lineas para detectar saltos

    self._iniciar_estado_lectura()
    self._obtener_salto_linea(saltos_linea.pop(0))

    for linea in lineas_lectura:
      if any((linea.lower().find(dia.lower()) != -1) for dia in self.dias):
        self.contador_lineas_horario += 1
      self._procesar_linea(linea, saltos_linea)

    if self.estado in [
      self.EstadoCreadorJSON.SALON_HORARIOS,
      self.EstadoCreadorJSON.DOCENTE_HORARIOS,
    ]:
      self._agregar_dato('', "docente")
      self._confirmar_datos()
      self.estado = self.EstadoCreadorJSON.ENCABEZADO


  # Metodo concreto: Crear JSON
  def crear_JSON(self):
    import pymupdf as miner1
    from pypdf import PdfReader as miner2

    self.almacenador.inicializar()

    PDF_FILE = config["directorio_carga"] + r'\..\ud\submission.pdf'

    #trata de alcanzar el fichero para actualizar los horarios
    try:
      with miner1.open(PDF_FILE) as pdf_doc_1:
        pdf_doc_2 = miner2(PDF_FILE)

        for num_page, pages in enumerate(zip(pdf_doc_1, pdf_doc_2.pages)):
          page_miner_1 = pages[0]
          page_miner_2 = pages[1]

          text_miner_1 = page_miner_1.get_text()
          text_miner_2 = page_miner_2.extract_text()

          self.procesar_pag(text_miner_1, text_miner_2)

          self._confirmar_datos()

          assert self.contador_lineas_horario == self.contador_agregados

        self.estado = self.EstadoCreadorJSON.FINALIZADO

    except FileNotFoundError:
      raise FileNotFoundError #excepcion capturada y lanzada

    except AssertionError:
      raise AssertionError #excepcion

    self.almacenador.finalizar()

  def _debugger(
    self,
    *args,
    condition: callable = lambda s: s.contador_lineas_horario > 0
  ):
    if condition(self): print('\n', *args, sep=' // ', end='\n')


# Clase: Creador de JSON por XML (CreadorJSONUD)
class CreadorJSONUDByXML(CreadorJSONUD):
    # Metodo concreto: Crear JSON
    def crear_JSON(self): pass