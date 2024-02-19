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

dire=input('Introducir directorio de trabajo: \n')

import os
os.chdir(dire)
print('Directorio de trabajo: ',os.getcwd())


# +
###################################################################
# -

#PARTE I: importación de datos del Ministerio del interior o CCAA
listScripts=["Diputados11.py"]
for script in listScripts:
    with open(script,encoding="utf-8") as f:
        contents = f.read()
    exec(contents)

# +
###################################################################
# -

#PARTE II: funciones de análisis y su importacoón para comprobaciones
listScripts=["funciones.py","Diputados21.py"]
for script in listScripts:
    with open(script,encoding="utf-8") as f:
        contents = f.read()
    exec(contents)

# +
###################################################################
# -

# SEGUNDA FASE.PARTE I: IMPORTACIÓN DE NUEVOS DATOS
listScripts=["Diputados31.py"]
for script in listScripts:
    with open(script,encoding="utf-8") as f:
        contents = f.read()
    exec(contents)

# +
###################################################################
# -

#PARTE II: INTRODUCIR NUEVOS GRUPOS
listScripts=["Diputados32.py"]
for script in listScripts:
    
    with open(script,encoding="utf-8") as f:
        contents = f.read()
    exec(contents)

# +
#################################################################
# -

#PARTE III: ELIMINAR DE NUEVO CANDIDATURAS <barrera
#comienza copiando df3=df1.copy()
listScripts=["Diputados33.py"]
for script in listScripts:
    with open(script,encoding="utf-8") as f:
        contents = f.read()
    exec(contents)

estructura(df3)

# +
##############################################################
# -

#PARTE IV: TABLAS d'HONDT
#No modifica df3
listScripts=["Diputados34.py"]
for script in listScripts:
    with open(script,encoding="utf-8") as f:
        contents = f.read()
    exec(contents)

# +
###############################################################
# -

# PARTE V: COMPROBAR SI HAY EMPATES
#No modifica df3
listScripts=["Diputados35.py"]
for script in listScripts:
    with open(script,encoding="utf-8") as f:
        contents = f.read()
    exec(contents)

# +
################################################################
# -

#PARTE VI: SI HAY EMPATES
#hago df4=df3.copy() a medio programa
#df4 contiene escaños asignados cuando no hay sorteo
#df5 contiene escaños asignados cuando hay sorteo
listScripts=["Diputados36.py"]
for script in listScripts:
    with open(script,encoding="utf-8") as f:
        contents = f.read()
    exec(contents)

# +
##################################################################
# -

#PARTE VII: ASIGNACIÓN DE ESCAÑOS DEFINITIVA
#recibe df5 y lo transforma en df6,df7,df71,DF71 y sale DF72
listScripts=["Diputados37.py"]
for script in listScripts:
    with open(script,encoding="utf-8") as f:
        contents = f.read()
    exec(contents)

# +
#######################################################################
# -

#PARTE VIII: ARCHIVO DE SALIDA EXCEL
#recibe df5 y lo transforma en df6,df7,df71,DF71 y sale DF72
listScripts=["Diputados38.py"]
for script in listScripts:
    with open(script,encoding="utf-8") as f:
        contents = f.read()
    exec(contents)


