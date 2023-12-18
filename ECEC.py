# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.15.2
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

#PARTE I: importación de datos del Ministerio del interior
listScripts=["Diputados11.py"]
for script in listScripts:
    with open(script,encoding="utf-8") as f:
        contents = f.read()
    exec(contents)

# +
###################################################################
# -

#PARTE II: funciones de análisis y su importacoón para comprobaciones
listScripts=["funciones.py","Diputados2.py"]
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
#############################################################3
# -

dipugrupos

for i in range(len(df3)):
    print('-PROVINCIA',i,'(',df1.loc[i]['PROVINCIA'].strip(),')','\n --DIPUTADOS:')
    print('   DERECHA',DF72.loc[i]['DIPDERECHA'])
    print('   IZQUIERDA',DF72.loc[i]['DIPIZQUIERDA'])
    print('   CENTRO',DF72.loc[i]['DIPCENTRO'])
    print('   NACIONALISTAS',DF72.loc[i]['DIPNACIONALISTAS'])
    print('   OTROS',DF72.loc[i]['DIPOTROS'])
    print('  --TOTAL',DF72.loc[i][dipugrupos].sum(),'DIPUTADOS')

print("---------------------------------------------------",
     "---------------------------------------------------",
     "TERMINADO:",guion+".py")

# +
##############################################################
# -

#PARTE VIII: ARCHIVO DE SALIDA EXCEL
#recibe df5 y lo transforma en df6,df7,df71,DF71 y sale DF72
listScripts=["Diputados38.py"]
for script in listScripts:
    with open(script,encoding="utf-8") as f:
        contents = f.read()


# +
###################################################################

# +
#DIPUTADOS38: PARTE VIII: ARCHIVO DE SALIDA EXCEL
# -

guion="Diputados38"

#salida con ceros de datos MinInt
output1=resultados.copy()

estructura(output1)

list(output1.loc[0].keys())[dipugrupos][9:]

A=[]
M1=[i for i in range(pos(df3,'DIPUTADOS')+1,pos(df3,'DDERECHA'))]
M=list(df3.loc[0][M1].keys())
for y in M:
    if (df3[y] == 0).all():
        A.append(y)

common=set(A).intersection(set(output1.loc[0].keys()))
#salida sin ceros
output2=output1.drop(columns=list(common),axis=1)

#salida con ceros de asignaciones
output3=pd.concat([DF71[VV0],DF71[VV1],DF71[VV2],DF71[VV7],DF71[VV8]],axis=1)

common=set(A).intersection(set(output3.loc[0].keys()))
#salida sin ceros de asignaciones
output4=output3.drop(columns=list(common),axis=1)

#salida de >barrera con ceros
output5=pd.concat([DF71[VV0],DF71[VV5],DF71[VV6],DF71[VV7],DF71[VV8]],axis=1)

common=set(A).intersection(set(output5.loc[0].keys()))
#salida sin ceros de >barrera
output6=output5.drop(columns=list(common),axis=1)

# +

F=input("¿DESEA EXPORTAR LOS RESULTADOS? (Y/N)\n")
if F=='Y' or F=='Y'.lower():
    Res=input("¿Qué nombre desea concatenar con 'Resultados'\n")
    Name='Resultados'+str(Res)
    G=input("¿DESEA ELIMINAR VALORES NULOS DE VOTOS?\n\
    (no es conveniente si se desea comparación con resultados iniciales\n(Y/N)\n") 
    if G=='Y' or G=='Y'.lower():
        writer = pd.ExcelWriter(Name+'.xlsx')
        results=output2
        results.to_excel(writer,sheet_name='DatosRealesMint')
        results=output4
        results.to_excel(writer,sheet_name='VotosReasignados')
        results=output6
        results.to_excel(writer,sheet_name='Datos>barrera')
        writer.close()
    if G=='N' or G=='N'.lower():
        writer = pd.ExcelWriter(Name+'.xlsx')
        results=output1
        results.to_excel(writer,sheet_name='DatosRealesMint')
        results=output3
        results.to_excel(writer,sheet_name='VotosReasignados')
        results=output5
        results.to_excel(writer,sheet_name='Datos>barrera')
        writer.close()
# -


print("---------------------------------------------------",
     "---------------------------------------------------",
     "TERMINADO:",guion+".py")




