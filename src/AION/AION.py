#-------------------------------------------------------------------------------
# Name:        Servicios modulo AION
# Purpose:     Recopilar los servicios del modulo interno de
#               AION, como su creador de horario aboulomano y
#               otros.
#
# Author:      Aref
#
# Created:     19-5=9+5/19-12/2022
# Copyright:   (k) Ka-Tet Co. 1999 / (k) Alta Lengua 2023
# Licence:     <uranus>
#-------------------------------------------------------------------------------

""" Modulo: Servicios modulo AION

Recopilar los servicios del modulo interno de AION, como su
creador de horario entre otros servicios.

Recopila:
    Funcion AION
"""
def creadorHorario(nodos: list[dict]) -> list[dict]:
    """ Funcion: Algoritmo-Inteligente de Organizacion sin Nombre
        (AION)

    Funcion que genera una serie de horarios ideales que no
    se solapan y que maximizan algunos criterios.

    Utiliza ciencia de datos, a traves de algoritmos de
    coloracion de grafos n-dimensionales para evitar el
    solapamiento de los datos. Ademas, usa colas para maximizar
    por algun criterio los datos.

    Parametros:
        nodos (list[dict]) -- listado de horarios que pueden
            presentar solapamientos multiples

    Referencia:
        cada nodo en la lista de nodos debe ser un diccionario
            con las llaves:
            identificadores -- permite que los nodos no se
                confundan, cada nodo en la lista debe tener unos
                identificadores unicos
            disgregadores -- permite que AION evite los
                solapamientos, son todos aquellos criterios que
                organizan el retorno para que los nodos no
                coexistan en una i-esima dimension (p.e.: hora y
                dia de la materia, ya que no se puede ver mas de
                una materia el mismo dia a la misma hora)
            [maximizadores] -- permite que AION priorize la
                existencia de algunos nodos en el retorno, son
                todos aquellos criterios que fuerzan el retorno
                para que esten presentes los mejores candidatos
                para un criterio (p.e. cantidad de creditos, ya
                que se quieren ver la mayor cantidad de creditos
                posibles en un semestre)

    Retorno:
        un listado de horarios sin solaparse y maximizados en
            algun criterio
    """
    cantMaterias = 0
    colores = [] #basado en el algoritmo de coloracion de grafos


    ## variable nodos puede ser ordenada en base a un criterio a maximizar ##


    for nodoBase in nodos:
        #variable que determina cuales solapamientos debe evitar en cada
        #  comparacion de esta iteracion
        disyuntorOrig = tuple(nodoBase['disgregadores'])

        colores.append([])

        #se desplaza por los nodos
        for nodoComp in nodos:
            flag = True #bandera no hay solapamiento

            #condicional nodo a comparar es diferente del nodo base
            if not nodoComp == nodoBase:

                #se desplaza por los disgregadores del nodo a comparar
                for disyuntorComp in nodoComp['disgregadores']:

                    #se desplaza por los disgregadores del nodo base
                    for disyuntorBase in nodoBase['disgregadores']:

                        #se desplaza conjuntamente para comparar
                        for index in range(len(disyuntorBase)):

                            #condicional encuentra solapamiento
                            if disyuntorBase[index] == disyuntorComp[index]:
                                #hayo solapamiento, entonces salta
                                flag = False
                                break

                        #hayo solapamiento, entonces salta
                        if not flag: break

                    #hayo solapamiento, entonces salta
                    if not flag: break

            #no hayo solapamiento con el nodo a comparar
            if flag:

                #agrega el nodo a comparar al retorno ya que no se solapa
                colores[-1].append(nodoComp['identificadores'])

                #agrega los disgregadores del nodo a comparar para que los
                #  siguientes nodos a comparar no se solapen con el recien
                #  agregado
                nodoBase['disgregadores'] += nodoComp['disgregadores']

        #restaura los disgregadores del nodo base antes de continuar iterando
        nodoBase['disgregadores'] = [i for i in disyuntorOrig]


        ## variable nodos puede ser ordenada en base a un criterio a    ##
        ##  maximizar, por defecto a continuacion se ordena maximizando ##
        ##  el numero de materias                                       ##


        #condicional maximiza numero de materias
        if len(colores[-1]) > cantMaterias:
            #el retorno actual es mejor que el retorno en memoria, entonces
            # lo sobreescribe
            cantMaterias = len(colores[-1])
            colores = [colores[-1]]

        #opcional no cumple con los criterios de maximizacion
        elif (len(colores[-1]) < cantMaterias or
                colores.index(colores[-1]) != len(colores) - 1):
            #el retorno actual es menor que el retorno en memoria, entonces
            # lo elimina
            colores.pop()

    #retorna la lista sin solapamientos
    return colores