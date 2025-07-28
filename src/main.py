#-------------------------------------------------------------------------------
# Name:        Main
# Purpose:     Servir de ejecutable principal para aplicación de
#               escritorio de Aion.
#
# Author:      Aref
#
# Created:     9-1/19-12/2022
# Copyright:   (k) Ka-Tet Co. 1999 / (k) Alta Lengua 2023
# Licence:     <uranus>
#-------------------------------------------------------------------------------

# "Aquello que importa" --
from typing import Union

from .entidades import Session, engine, Base

Base.metadata.create_all(engine)
sesion = Session()

from .entidades.horario.universidad import (UniversidadEntidad,
            UniversidadEsquema)
from .entidades.horario import univ_init

def init_us():
  n_us = sesion.query(UniversidadEntidad.diminu).count()
  if n_us == 0:
    ud = UniversidadEsquema(
            only=('univ_nombre', 'diminu', 'univ_url_logo'))\
          .load(univ_init)
    sesion.add(ud)
    sesion.commit()
    sesion.close()

#init_us()

def print_us():
  us = sesion.query(UniversidadEntidad).all()
  print('--- Universidades')
  for u in us: print(f'({u.id}) {u}')

#print_us()

import json

def get_u(ind: int) -> dict:
  u = sesion.query(UniversidadEntidad)\
        .filter(UniversidadEntidad.univ_id==ind).first()
  u = UniversidadEsquema().dump(u, many=False)
  sesion.close()
  return u

def get_head_u(diminu: str) -> dict:
  with open(f'src\\archivos\\{diminu}\\cabecera') as cabecera:
    return cabecera.read()

#d = get_u(1)
#d["periodo actual"] = get_head_u(d['diminutivo']))
#print(d)

#from .AION.AION import creadorHorario
#from .const import nodos
#horarios = creadorHorario(nodos)
#print(horarios)

from .config import init_config, config
init_config()

from .modelos.selector_universidad import selector_universidad

def actualizar_JSON():
    U = selector_universidad('Ud')()
    U.getCreadorJSON('pdf').crear_JSON()

#actualizar_JSON()

from .entidades.autentificacion.usuario import (UsuarioEntidad,
            UsuarioEsquema)
from .entidades.autentificacion import usu_init

def init_usrs():
  n_usrs = sesion.query(UsuarioEntidad.diminu).count()
  if n_usrs == 0:
    us1 = UsuarioEsquema(
            only=UsuarioEsquema.campos(tuple))\
          .load(usu_init)
    us1.crear_usuario()

#init_usrs()

def get_usr(ind: Union[int,str]) -> UsuarioEntidad:
    usr = sesion.query(UsuarioEntidad)\
        .filter(UsuarioEntidad.usur_apodo==ind).first()
    sesion.close()
    return usr

#usr = get_usr('JR3')
#simbolismo = usr.generar_autentificacion_simbolica(3600)
#print(simbolismo)
#apodo = UsuarioEntidad.chequear_autentificacion_simbolica(simbolismo)
#print(apodo)

from .entidades.horario.personal import PersonalEntidad, PersonalEsquema

def test_persl():
  usr = sesion.query(UsuarioEntidad).first()
  u = sesion.query(UniversidadEntidad).first()
  p_dict = {
      'usuario': usr.usur_id,
      'universidad': u.univ_id,
      'filtros': "",
      'selectos': ""
    }
  p = PersonalEsquema().load(p_dict)
  sesion.add(p)
  sesion.commit()
  sesion.close()

#test_persl()