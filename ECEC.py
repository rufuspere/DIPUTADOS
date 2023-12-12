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


listScripts=["Diputados11.py","funciones.py","Diputados2.py"]
for script in listScripts:
    with open(script,encoding="utf-8") as f:
        contents = f.read()
    exec(contents)

listScripts=["Diputados31.py"]
for script in listScripts:
    with open(script,encoding="utf-8") as f:
        contents = f.read()
    exec(contents)

listScripts=["Diputados32.py"]
for script in listScripts:
    with open(script,encoding="utf-8") as f:
        contents = f.read()
    exec(contents)

listScripts=["Diputados33.py"]
for script in listScripts:
    with open(script,encoding="utf-8") as f:
        contents = f.read()
    exec(contents)

df3.loc[30]['PARTIDOS>']

# +
#PARTE IV: TABLAS d'HONDT
# -

list1 = [int(x) for x in D]
list1.sort()
claves = [str(x) for x in list1]

#lista de partidos por provincia que superan la barrera
no_nulos=[[] for j in range(N_PROV)]
for j in range(N_PROV):
    for x in claves:
        if(df3.loc[j][x])!=0:
            no_nulos[j].append(x)    

#partidos que superan el mínimo de votos (barrera) en provincia 30
no_nulos[0]

#creo un diccionario Koef vacío salvo par partidos para guardar
 #las tablas d'Hondt para cada provincia
Koef=[[] for j in range(N_PROV)]
Dict={}
for j in range(N_PROV):
    coef=[i for i in range(1,int(df3.loc[j]['DIPUTADOS']))]
    for x in no_nulos[j]:
        Dict['partido']=x
        for c in coef:
            Dict[c]=0
        a=Dict
        #print(j,a)
        Koef[j].append(a.copy())

Koef[0]

#genero DataFrames para tablas d'Hondt a partir de los diccionarios
for j in range(N_PROV):    
    K[j]=pd.DataFrame(Koef[j])  
    K[j].insert(loc=0, column='provincia', value=0, allow_duplicates = False)

dHondt=[[] for i in range(N_PROV)]
for i in range(len(df3)):
    dHondt[i]=pd.DataFrame(K[i])
    dHondt[i].index=list(dHondt[i][:]['partido'])


for i in range(len(df3)):
     for k in list(dHondt[i][:]['partido']):
        dHondt[i].loc[k,'provincia']=i

for i in range(len(df3)):
    
    for k in list(dHondt[i][:]['partido']):
            
        for l in range (1,int(df3.loc[i]['DIPUTADOS'])+1):
            a=float(df3.loc[i][k])/float(l)
            dHondt[i].loc[k,l]=a


# +
lista_votos=[[] for i in range(N_PROV)]
for i in range(N_PROV):
    N_DIP=list(dHondt[i].keys())[2:]
    PARTS=list(dHondt[i].index)
    lista_votos1[i]=[]
    for j in PARTS:
        #print('provincia',i,list(dHondt[i].loc[j][2:]))
        lista_votos[i]=lista_votos[i]+list(dHondt[i].loc[j][2:])
    
       
      
# -

#Exporto d'Hondt 
F=input("¿DESEA EXPORTAR LAS TABLAS d'HONDT? (Y/N)")
if F=='Y' or F=='Y'.lower():
    for i in range(N_PROV):
        A=dHondt[i] 
        B=pd.DataFrame(lista_votos[i])
        B[B>0].dropna(axis=0, how='all') 
        Name='dHondt'+str(i)
        writer = pd.ExcelWriter(Name+'.xlsx')
        A.to_excel(writer,'dHondt')
        B.to_excel(writer,'lista_votos')
        writer.close()

# +
#DIPUTADOS34: PARTE IV: TABLAS d'HONDT
# -

p=[[] for i in range(N_PROV)]
for i in range(N_PROV):
    c=df3.loc[j,ll]
    p[i]=[]
    
    for k in range (1,int(df3.loc[j]['DIPUTADOS'])+1):
        part_voto=c/k
        p[i].append(part_voto)
#p[I][J] es una lista de dimensión N_PROVINCIAS y donde cada elemento de la lista es 
#otra lista de longitud N_PARTIDOSxDIPUTADOS cuyo contenido es el número de votos de 
#cada partido dividido por 1,2,...DIPUTADOS.

# +
import numpy as np
q=[[] for i in range(N_PROV)]
r=[[] for i in range(N_PROV)]
dHondt=[[] for i in range(N_PROV)]
for i in range(N_PROV):
    r[i]=[]
    for j in range(int(df3.loc[i]['DIPUTADOS'])):
        A=p[i][j]
        r[i].append(A.values)
        q[i]=np.array((r[i])).T
        dHondt[i]=pd.DataFrame(q[i])
        
#dHondt es un array que representa la tabla d'Hondt  
# -

#lista_votos[I] es una lista de longitud N_PROVINCIAS que tiene los valores ordenados de la 
#tabla d'Hondt de cada provincia. Si no existen valores duplicados con lista_votos[I][DIPUTADOS-1]
#en lista_votos[I][>=DIPUTADOS] se eligen los primeros términos hasta DIPUTADOS y se asignan los escaños
#según las veces que aparezca cada partido. Si existen duplicados, se seleccionan aquellos partidos
#que tienen el mismo valor del índice que lista_votos[I][DIPUTADOS-1] y, enre ellos, se eligen al azar
#las candidaturas que deben completar el número de escaños. p.e. si hay DIPUTADOS=6 y 
#lista_votos[I][4]=lista_votos[I][5]=lista_votos[I][6]=lista_votos[I][7]=1000 elegiremos aleatoriamente
#dos de las cuatro empatadas para los dos escaños vacantes.
lista_votos=[[] for i in range(N_PROV)]
for i in range(N_PROV):
    lista_votos[i]=[]
    for j in range(int(df3.loc[i]['DIPUTADOS'])):
        lista_votos[i]=lista_votos[i]+list(p[i][j])
        
        lista_votos[i].sort(reverse=True)

#Exporto d'Hondt 
F=input("¿DESEA EXPORTAR LAS TABLAS d'HONDT? (Y/N)")
if F=='Y' or F=='Y'.lower():
    for i in range(N_PROV):
        A=dHondt[i][dHondt[i]>0].dropna(axis=0, how='all') 
        B=pd.DataFrame(lista_votos[i])
        B[B>0].dropna(axis=0, how='all') 
        Name='dHondt'+str(i)
        writer = pd.ExcelWriter(Name+'.xlsx')
        A.to_excel(writer,'dHondt')
        B.to_excel(writer,'lista_votos')
        writer.close()


