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

# +
#Diputados1

# +
#PARTE 0: ESTABLECER DIRECTORIO DE TRABAJO
# -

dire=input('Introducir directorio de trabajo: \n')

import os
os.chdir(dire)
print('Directorio de trabajo: ',os.getcwd())

import pickle
w = open(dire+"\\dire.pkl","wb")
pickle.dump(dire,w)
w.close()
import sys
sys.path.append(dire)

# +
#PARTE I: IMPORTACIÓN DE DATOS


# +
#PARTE I: IMPORTACIÓN DE DATOS

# +
#importar datos de las elecciones. Son del Ministerio del Interior adaptados
import pandas as pd
import warnings
#importar datos de las elecciones. Son del Ministerio del Interior adaptados
while True:
    voto=input ('introduce el nombre del fichero de resultados de la votación: ')
    year=input('y el año: ')
    votos=voto+year+'.xlsx'
    try:
        print('nombre del fichero: ',votos)
        df0 = pd.read_excel(votos,header=0)
        break
    except:
        print('no existe')

df0.head()#df0 es el resultado de las elecciones 


# +
# importar partidos por grupo
parties=input ('introduce el nombre del fichero de partidos: ')
year=input('y el año: ')
party=parties+year+'.xlsx'
    
try:
    print('nombre del fichero: ',party)
    df2 = pd.read_excel(party)
except:
    print('no existe')
df2.head()#df2 es la lista de partidos y grupos 


# -

#definimos función que permita conocer la estructura de un DataFrame. Es muy
#necesario para construir Data Frames.
def estructura(my_Frame):
    A=[]
    B=[]
    C=[]
    my_Frame=my_Frame.keys()
    my_List=list(my_Frame)
    for i in range (len(my_List)):
        A.append(my_List[i])
        B.append(i)
    col_list=list(zip(B,A))
   #print('Longitud:',len(col_list),'\n', 'Posición y labels:','\n',col_list)
    return col_list


#genero la lista de claves de partidos
l=[]
for item in df2:
    l.append(str(item))

party1=set(df2.loc[1])
grupos=list(party1)
party2=pd.Series(df2.columns.values,index=df2.columns.values)
party2=pd.DataFrame(party2)


#añado a cada partido un número de identificación que será el usado en adelante
warnings.filterwarnings("ignore")
df2=pd.concat([df2,pd.DataFrame(party2.T)],ignore_index=True).copy()


df2.to_pickle(dire+'\partidos')

estructura(df0)#da una lista de diccionarios donde cada diccionario es un
#número:nombre de columna.Se ve que se intercalan votos y dioutados


#creamos dos variables para número de provincias y de partidos
N_PROV=len(df0)
N_PARTIDOS=len(df2.T)
print(N_PROV,N_PARTIDOS)


#renombramos algunas columnas
df0.rename(columns={'Nombre de Comunidad':'COMUNIDAD','Código de Provincia': 'NPROVINCIA',
'Nombre de Provincia':'PROVINCIA','Total censo electoral': 'CENSO_ELECTORAL',
'Total votantes':'TOTAL_VOTANTES',
'Votos en blanco':'VOTOS_BLANCOS','Votos válidos':'VOTOS_VÁLIDOS','Diputados':'DIPUTADOS',
'Población':'POBLACIÓN','Votos a candidaturas':'VOTOS A CANDIDATURAS',
'Votos nulos':'VOTOS NULOS','Diputados':'DIPUTADOS'},
inplace=True )


# +
#extraemos las columnas que nos serán necesarias para aplicar el método d'Hondt
W1=[]#datos de provincia y votos de cada partidos
W2=[]#escaños de cada partido
for i in range(0,17):
    W1.append(df0.loc[0].keys()[i])
for i in range(17,151):
    if ('Votos' in df0.loc[0].keys()[i]):
        W1.append(df0.loc[0].keys()[i])
for i in range(17,151):    
    if ('Diputados' in df0.loc[0].keys()[i]):
        W2.append(df0.loc[0].keys()[i])

#print(W1)
#print(W2)
# -


Y=[]#nombres de columnas con los votos a cada partido
for x in range(17,84):
    if ('Votos' in W1[x]):
        Y.append(W1[x])


Z=[]#nombres de columnas con los diputados a cada partido
for x in range(0,67):
    if ('Diputados' in W2[x]):
        Z.append(W2[x])

# +
#modificamos df0 el Data Frame que sirve de base a la asignación de escaño y
#que contiene los datos de circunscripción y los votos y diputados

DF1 = pd.DataFrame(data=None, columns=df0.columns, index=df0.index)
DF2 = pd.DataFrame(data=None, columns=df0.columns, index=df0.index)
for i in range(N_PROV):
    for x in W1:
        DF1.loc[i][x]=df0.loc[i][x]
for i in range(N_PROV):
    for x in W2:
        DF2.loc[i][x]=df0.loc[i][x]
DF1=DF1.dropna(axis=1,how='all')
DF2=DF2.dropna(axis=1,how='all')
df0=pd.concat([DF1,DF2],axis=1)
# -


df0['TOTAL_VOTANTES']/df0['CENSO_ELECTORAL']
if (df0['TOTAL_VOTANTES']/df0['CENSO_ELECTORAL']).any()>1:
    print ('¡ERROR!',df0['TOTAL_VOTANTES']/df0['CENSO_ELECTORAL'])
else:
    print ('¡OK!\n')
    print(df0['TOTAL_VOTANTES']/df0['CENSO_ELECTORAL'])


#inserto participación por provincia
df0.insert(loc = 13,
          column = '%PARTICIPACIÓN',
          value =df0['TOTAL_VOTANTES']/df0['CENSO_ELECTORAL'])


df0.loc[2]['%PARTICIPACIÓN']


dfaux0=df0[W1[0:17]]#datos censales y resumidos por provincia


dfaux1=df0[W1[17:]]

Var=dict(zip(W1[17:],l))#diccionario que asigna votos a 
#identificación numérica de partido


Var

dfaux2=df0[W2[0:]]


# +
#df1

df1=pd.concat([dfaux0,dfaux1,dfaux2], axis=1)

# +
#eliminamos ciertas columnas innecesarias (Censo CERA, Mesas Electorales...)
#para obtener df1

df1 = df1.drop(df1.columns[[ 4,5,6,8,9,10]], axis=1)
# -


#inserto número de partidos
df1.insert(loc = 4,
          column = 'NPARTIDOS',
          value =N_PARTIDOS)


#partidos con más del 3% de votos
df1.insert(loc = 5,
          column = 'PARTIDOS>3',
          value =0)


for x in l:
    columna='%'+x
    df1[columna]=df1[x+'Votos']/df1['VOTOS_VÁLIDOS']


# +
#PARTE II: INTRODUCIR GRUPOS
# -

#agrupaciones para votos
vot_grupos=['VDERECHA',
'VCENTRO',
'VIZQUIERDA',
'VNACIONALISTAS',
'VOTROS']

import re
#asignar a cada grupo sus partidos para votos
B=vot_grupos
list_vgroups = {key: None for key in B}
for x in vot_grupos:#nombres de los grupos (CENTRO, DERECHA,...)
    C=[]
    
    for i in df2.loc[2][:]:#nombres de los partidos (1,2,...NPARTIDOS)
        if df2.loc[1][i] ==re.sub('V', '', x):
            C.append(str(i)+'Votos')
    #print(x,C)
    list_vgroups[x]=C

vot_grupos

list_vgroups

#grupos para votos >3%
grupos=['DERECHA',
'CENTRO',
'IZQUIERDA',
'NACIONALISTAS',
'OTROS']

list_groups = {key: None for key in grupos}
for x in grupos:#nombres de los grupos (CENTRO, DERECHA,...)
    C=[]
    
    for i in df2.loc[2][:]:#nombres de los partidos (1,2,...NPARTIDOS)
        if df2.loc[1][i] ==re.sub('V', '', x):
            C.append(str(i))
    #print(x,C)
    list_groups[x]=C

list_groups

#grupos para diputados
dgrupos=['DDERECHA',
'DCENTRO',
'DIZQUIERDA',
'DNACIONALISTAS',
'DOTROS']

#asignar a cada grupo sus partidos para escaños
list_dgroups = {key: None for key in dgrupos}
for x in dgrupos:#nombres de los grupos (CENTRO, DERECHA,...)
    C=[]
    
    for i in df2.loc[2][:]:#nombres de los partidos (1,2,...NPARTIDOS)
        if df2.loc[1][i] ==x[1:]:
            C.append(str(i)+'Diputados')
    #print(x,C)
    list_dgroups[x]=C

list_dgroups

#votos por grupos por provincias
dfd=df0.copy()
dfd= dfd.reindex(columns = dfd.columns.tolist() 
                                  + dgrupos)


#extraigo los diputados a cada candidatura y provincia
diputados=df0.copy()
diputados=diputados[diputados.columns.intersection(Z)]    

for j in range (N_PROV):#provincias
    for x in dgrupos:#grupos de partidos
        dfd.loc[j,x]=dfd.loc[j][list_dgroups[x]].sum()

estructura(df0)

#votos por grupos por provincias
for j in range (N_PROV):#provincias
    print('\n','PROVINCIA',df1.loc[j]['PROVINCIA'].strip(),f'{j:,.0f}','\n')
    S=0
    for x in vot_grupos:#grupos de partidos
        print(x, f'{df1.loc[j][list_vgroups[x]].sum():,.0f}')
        S=S+df1.loc[j][list_vgroups[x]].sum()
    print('--TOTAL VOTOS ',f'{S:,.0f}')

#diputados por grupos por provincias
for j in range (N_PROV):#provincias
    print('\n','PROVINCIA',df1.loc[j]['PROVINCIA'].strip(),f'{j:,.0f}','\n')
    S=0
    for x in dgrupos:#grupos de partidos
        print(x, f'{df1.loc[j][list_dgroups[x]].sum():,.0f}')
        S=S+df1.loc[j][list_dgroups[x]].sum()
    print('--TOTAL DIPUTADOS ',f'{S:,.0f}')

#votos por grupos por provincias
for j in range (N_PROV):#provincias
    S=0
    for x in dgrupos:#grupos de partidos
        df0.loc[j,x]=df0.loc[j][list_dgroups[x]].sum()

df1=df1.rename(columns=Var)

list_vgroups

estructura(df0)

U0=[i for i in range(0,18)]
U1=[i for i in range(18,85)]
U3=[i for i in range(85,152)]
U2=[i for i in range(152,157)]


VV=[]
UU0=list(df0.loc[0][U0].keys())
UU1=list(df0.loc[0][U1].keys())
UU2=list(df0.loc[0][U2].keys())
UU3=list(df0.loc[0][U3].keys())
UU=UU0+UU1+UU3
UU


# +

results=pd.concat([df0[UU0],df0[UU1],df0[UU2],df0[UU3]], axis=1)
# -

estructura(results)

VV=list(results.loc[0][UU[18:]].keys())

VV

results= results.reindex(columns = results.columns.tolist() 
                                  + vot_grupos)

#votos por grupos por provincias
for j in range (N_PROV):#provincias
    S=0
    for x in vot_grupos:#grupos de partidos
        try:
            results.loc[j,x]=results.loc[j][list_vgroups[x]].sum()
        except:
            continue

estructura(results)

# +
#PARTE III: ARCHIVO DE SALIDA EXCEL
# -

vot=list(df0.loc[0][:].keys())

votes=vot[18:85]

percent=list(df1.loc[0][:].keys()[147:])

percent

#chequeos
#suma de votos igual a votos a candidaturas
for j in range (N_PROV):#provincias
    print('\n','PROVINCIA',results.loc[j]['PROVINCIA'].strip(),f'{j:,.0f}')
    S=0
    S1=0
    for x in votes:#votos de partidos
        S=S+results.loc[j][x].sum()
    for y in vot_grupos:
        S1=S1+results.loc[j][y].sum()
    a=(results.loc[j]['VOTOS A CANDIDATURAS'])
    print('--TOTAL VOTOS',f'{S:,.0f}','\n','--VOTOS A CANDIDATURAS',
         f'{a:,.0f}','\n','--VOTOS A GRUPOS',f'{S1:,.0f}')

#chequeos
#suma de diputados igual número de diputados y suma por grupos
for j in range (N_PROV):#provincias
    print('\n','PROVINCIA',results.loc[j]['PROVINCIA'].strip(),f'{j:,.0f}')
    S=0
    S1=0
    for x in Z:#diputados
        S=S+results.loc[j][x].sum()
    for y in dgrupos:
        S1=S1+results.loc[j][y].sum()
    a=(results.loc[j]['DIPUTADOS'])
    print('--TOTAL VOTOS',f'{S:,.0f}','\n','--DIPUTADOS A CANDIDATURAS',
         f'{a:,.0f}','\n','--DIPUTADOS A GRUPOS',f'{S1:,.0f}')

Sumy=df1.copy()
D=[]
for x in range(N_PROV):
    for y in percent:
        if (df1.loc[x][y]>=0.03):
            Sumy.loc[x][y[1:]]=df1.loc[x][y[1:]]
            D.append(int(y[1:]))
        else:
            Sumy.loc[x][y[1:]]=0
D=list(set(D))
D.sort()

D = list(map(str, D))

UHU0=[i for i in range(0,13)]
UHU=list(df1.loc[0][UHU0].keys())

df1[UHU].head()

df1[l].head()

df1[UHU].reset_index(drop=True, inplace=True)
df1[l].reset_index(drop=True, inplace=True)

masde3=pd.concat([df1[UHU],df1[l]],axis=1)

df1[l].head()

masde3= masde3.reindex(columns = masde3.columns.tolist() 
                                  + grupos)

to_remove = list(set(l) - set(D))

len(to_remove)

masde3=masde3.drop(columns=to_remove)

list(set.intersection(set(list_groups['DERECHA']),set(D)))

#votos por grupos por provincias
for j in range (N_PROV):#provincias
    S=0
    for x in grupos:#grupos de partidos
        masde3.loc[j,x]=masde3.loc[j][list(set.intersection(set(list_groups[x]),set(D)))].sum()

masde3.loc[0][grupos].sum()

for j in range (N_PROV):#provincias
    Su=0
    for x in D:#grupos de partidos
        
        if masde3.loc[j][x].any()!=0:
            Su=Su+1
    print(j,Su)
    masde3.loc[j,'PARTIDOS>3']=Su


estructura(masde3)

#reordeno campos
S0=[i for i in range(0,85)]
S1=[i for i in range(157,162)]
S2=[i for i in range(90,157)]
S3=[i for i in range(85,90)]

SS0=list(results.loc[0][S0].keys())
SS1=list(results.loc[0][S1].keys())
SS2=list(results.loc[0][S2].keys())
SS3=list(results.loc[0][S3].keys())

resultados=pd.concat([results[SS0],results[SS1],results[SS2],results[SS3]],axis=1)

estructura(resultados)

M1=[i for i in range(18,162)]
M=list(resultados.loc[0][M1].keys())

A=[]
for y in M:
    if (resultados[y] == 0).all():
        A.append(y)

F=input("¿DESEA EXPORTAR LOS RESULTADOS? (Y/N)\n")
if F=='Y' or F=='Y'.lower():
    Res=input("¿Qué nombre desea concatenar con 'Resultados'\n")
    Name='Resultados'+str(Res)
    G=input("¿DESEA ELIMINAR VALORES NULOS DE VOTOS?\n\
    (no es conveniente si se desea comparación con resultados iniciales\n(Y/N)\n") 
    if G=='Y' or G=='Y'.lower():
        resultados=resultados.drop(columns=A,axis=1)
        writer = pd.ExcelWriter(Name+'.xlsx')
        resultados.to_excel(writer,sheet_name='DatosMint')
        masde3.to_excel(writer,sheet_name='Datos>3%')
        writer.close()
    if G=='N' or G=='N'.lower():
        writer = pd.ExcelWriter(Name+'.xlsx')
        resultados.to_excel(writer,sheet_name='DatosMint1')
        masde3.to_excel(writer,sheet_name='Datos>3%')
        writer.close()


# +
#PARTE IV: GUARDAR FICHEROS DE INTERÉS
# -

#exporto ficheros de interés
df0.to_pickle(dire+"\\df0.pkl")
df1.to_pickle(dire+"\\df1.pkl")
df2.to_pickle(dire+"\\df2.pkl")
resultados.to_pickle((dire+"\\resultados.pkl"))
variables={}
variables['N_PROV']=N_PROV
variables['N_PARTIDOS']=N_PARTIDOS
h = open(dire+"\\variables.pkl","wb")
pickle.dump(variables,h)
h.close()
q = open(dire+"\\l.pkl","wb")
pickle.dump(l,q)
q.close()

resultados.loc[30]['DDERECHA']


