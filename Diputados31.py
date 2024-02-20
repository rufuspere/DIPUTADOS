# ---
# jupyter:
#   jupytext:
#     formats: py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.16.0
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %%
#DIPUTADOS31: PARTE I: IMPORTACIÓN DE DATOS


# %%
guion="Diputados31"

# %%
import os
import pandas as pd
dire=os.getcwd()
print('Directorio de trabajo: ',os.getcwd())
minint=pd.read_pickle(dire+"\\minint.pkl")#contiene los datos de las últimas elecciones
#publicados por el MINT.

# %%
#importar datos de las elecciones. Son Son del Minit o CCAA 
#modificados para adaptarse a las hipótesis
#sobre candidaturas

import warnings
while True:
    voto=input ('introduce el nombre del fichero de resultados de la votación: ')
    year=input('y el año: ')
    extension=input('y la extensión (xls, xlsm,xlsx): ')
    votos=voto+year+'.'+extension
    try:
        print('nombre del fichero: ',votos)
        df0 = pd.read_excel(votos,header=0)
        break
    except:
        print('no existe')

df0.head()#df0 es el resultado de las elecciones 


# %%
# importar partidos por grupo
parties=input ('introduce el nombre del fichero de partidos: ')
year=input('y el año: ')
party=parties+year+'.xlsx'
    
try:
    print('nombre del fichero: ',party)
    df2 = pd.read_excel(party)
    
except:
    print('no existe')
#df2 es la lista de partidos y grupos 

 


# %%
#genero la lista de claves de partidos
l=[]
for item in df2:
    l.append(str(item))
l_sinbarr=l


# %%
#defino función que encuentra posición de columna en df
def pos(df,col):
    return(list(df.keys()).index(col))


# %%
party1=set(df2.loc[1])
grupos=list(party1)
party2=pd.Series(df2.columns.values,index=df2.columns.values)
party2=pd.DataFrame(party2)

# %%
#añado a cada partdo un número de identificación que será el usado en adelante
warnings.filterwarnings("ignore")
df2=pd.concat([df2,pd.DataFrame(party2.T)],ignore_index=True).copy()


# %%
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


# %%
#creamos dos variables para número de provincias y de partidos
N_PROV=len(df0)
N_PARTIDOS=len(df2.T)
print(N_PROV,N_PARTIDOS)


# %%
#renombramos algunas columnas
df0.rename(columns={'Nombre de Comunidad':'COMUNIDAD','Código de Provincia': 'NPROVINCIA',
'Nombre de Provincia':'PROVINCIA','Total censo electoral': 'CENSO_ELECTORAL',
'Total votantes':'TOTAL_VOTANTES',
'Votos en blanco':'VOTOS_BLANCOS','Votos válidos':'VOTOS_VÁLIDOS','Diputados':'DIPUTADOS',
'Población':'POBLACIÓN','Votos a candidaturas':'VOTOS A CANDIDATURAS',
'Votos nulos':'VOTOS NULOS','Diputados':'DIPUTADOS'},
inplace=True )


# %%
df0['TOTAL_VOTANTES']/df0['CENSO_ELECTORAL']
if (df0['TOTAL_VOTANTES']/df0['CENSO_ELECTORAL']).any()>1:
    print ('¡ERROR!',df0['TOTAL_VOTANTES']/df0['CENSO_ELECTORAL'])
else:
    print ('¡OK!\n',df0['TOTAL_VOTANTES']/df0['CENSO_ELECTORAL'])


# %%
#inserto participación por provincia
df0.insert(loc = pos(df0,"VOTOS A CANDIDATURAS"),
          column = '%PARTICIPACIÓN',
          value =df0['TOTAL_VOTANTES']/df0['CENSO_ELECTORAL'])


# %%
df0['TOTAL_VOTANTES']/df0['CENSO_ELECTORAL']
if (df0['TOTAL_VOTANTES']/df0['CENSO_ELECTORAL']).any()>1:
    print ('¡ERROR!',df0['TOTAL_VOTANTES']/df0['CENSO_ELECTORAL'])
else:
    print ('¡OK!\n')
    print('Porcentaje de Votantes:',100*df0['TOTAL_VOTANTES'].sum()/df0['CENSO_ELECTORAL'].sum(),'%')

# %%
W1=[]#datos de provincia y votos de cada partidos
W2=[]#escaños de cada partido
for i in range(0,list(df0.keys()).index("1Votos")):
    W1.append(df0.loc[0].keys()[i])
for i in range(0,len(df0.keys())):
    if ('Votos' in df0.loc[0].keys()[i]):
        W1.append(df0.loc[0].keys()[i])
   
    if ('Diputados' in df0.loc[0].keys()[i]):
        W2.append(df0.loc[0].keys()[i])

# %%
Y=[]#nombres de columnas con los votos a cada partido
leng=len(W1)
for x in range(0,leng):
    if ('Votos' in W1[x]):
        Y.append(W1[x])


# %%
Z=[]#nombres de columnas con los diputados a cada partido
for x in range(0,len(W2)):
    if ('Diputados' in W2[x]):
        Z.append(W2[x])

# %%
new_l=Y

# %%
new_d=Z

# %%
dfaux0=df0[W1]#datos censales y resumidos por provincia


# %%
dfaux1=df0[W2[0:]]

# %%
#df1

df1=pd.concat([dfaux0,dfaux1], axis=1)

# %%
Var=dict(zip(W1[pos(df1,'1Votos'):],l))#diccionario que asigna votos a 
#identificación numérica de partido


# %%
a1=pos(df1,'Número de mesas')

# %%
a2=pos(df1,'Censo electoral sin CERA')

# %%
a3=pos(df1,'Censo CERA')

# %%
#eliminamos ciertas columnas innecesarias (a1=Número de mesas, a3=Censo CERA,...)
#para obtener df1

df1 = df1.drop(df1.columns[[ a1,a2,a3]], axis=1)


# %%
estructura(df1)

# %%
print('La barrera electoral es \n 0.03 para el Congreso\n 0.05 para las eleciones en la CAM y\n 0 para el Europarlamento')

# %%
barrera=input('barrera electoral (<1)')
barrera=float(barrera)

# %%
#inserto número de partidos
df1.insert(loc = pos(df1,'CENSO_ELECTORAL'),
          column = 'NPARTIDOS',
          value =N_PARTIDOS)


# %%
#partidos con más votos que la barrera electoral
df1.insert(loc = pos(df1,'CENSO_ELECTORAL'),
          column ='PARTIDOS>' ,
          value =0)


# %%
for x in l:
    columna='%'+x
    df1[columna]=df1[x+'Votos']/df1['VOTOS_VÁLIDOS']


# %%
estructura(df1)

# %%
print("---------------------------------------------------","TERMINADO:",guion+".py")

# %%
