# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.16.0
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# +
#Diputados21: importa funciones que pueden ser útiles para analizar 
#resultados
# -

guion="Diputados21"

import funciones as aux

print ("ESTA ES LA LISTA DE FUNCIONES EN EL MÓDULO 'funciones'")
print("--1)Identificar partido:\n    partido(codigo)")
print('--2) Listar nombre, índice, código y comunidad de una provincia:\n     provincia(codigo)')
print('--3) Lista de votos y escaños por provincia:\n     Resumen_Prov()')
print('--4) Lista de votos por grupo político:\n     Votos_y_Escaños_Grupos()')
print('--5) Lista de votos y escaños por CA:\n     Votos_y_Diputados(Com)')
print('--6) Lista de votos y escaños por provincia:\n     VotEscaño_Prov(codigo)')
print('--7) lista comunidades con sus provincias:\n     Com_Aut()')
print('--8) lista de partidos:\n     lista_partidos()')
print('NO OLVIDE AÑADIR EL PREFIJO aux. AL NOMBRE DE LA FUNCIÓN: aux.provincia(codigo)')

print ("\nAntes de iniciar Eleccion3 compruebe los resultados con las funciones definidas previamente o con consultas propias")

aux.lista_partidos()


aux.Votos_y_Escaños_Grupos()

aux.minint
