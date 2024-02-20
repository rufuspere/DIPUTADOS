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
#ESCANOS

# +
#PARTE I: IMPORTACIÓN DE DATOS
# -

guion='PARTE I'

# %precision %.2f

dire=input('Introducir directorio de trabajo: \n')

import os
os.chdir(dire)
print('Directorio de trabajo: ',os.getcwd())


import pickle
import warnings
import pandas as pd

# +
#importar Excel con datos de las elecciones. Son del Ministerio del Interior o las CCAA 
#modificados para adaptarse a las hipótesis sobre candidaturas

while True:
    voto=input ('introduce el nombre del fichero de resultados de la votación: ')
    year=input('y el año: ')
    votos=voto+year+'.xlsx'
    try:
        print('nombre del fichero: ',votos)
        print(os.path.exists(votos))
        df0 = pd.read_excel(votos,sheet_name='Hoja1', header=0)
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
#df2 es la lista de partidos y grupos 

# -

#genero la lista de claves de partidos
l=[]
for item in df2:
    l.append(str(item))
l_sinbarr=l


#defino función que encuentra posición de columna en df
def pos(df,col):
    return(list(df.keys()).index(col))


party1=set(df2.loc[1])
grupos=list(party1)
party2=pd.Series(df2.columns.values,index=df2.columns.values)
party2=pd.DataFrame(party2)

#añado a cada partdo un número de identificación que será el usado en adelante
warnings.filterwarnings("ignore")
df2=pd.concat([df2,pd.DataFrame(party2.T)],ignore_index=True).copy()

df2.head()


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


df0['TOTAL_VOTANTES']/df0['CENSO_ELECTORAL']
if (df0['TOTAL_VOTANTES']/df0['CENSO_ELECTORAL']).any()>1:
    print ('¡ERROR!',df0['TOTAL_VOTANTES']/df0['CENSO_ELECTORAL'])
else:
    print ('¡OK!\n',df0['TOTAL_VOTANTES']/df0['CENSO_ELECTORAL'])


#inserto participación por provincia
df0.insert(loc = pos(df0,"VOTOS A CANDIDATURAS"),
          column = '%PARTICIPACIÓN',
          value =df0['TOTAL_VOTANTES']/df0['CENSO_ELECTORAL'])


df0['TOTAL_VOTANTES']/df0['CENSO_ELECTORAL']
if (df0['TOTAL_VOTANTES']/df0['CENSO_ELECTORAL']).any()>1:
    print ('¡ERROR!',df0['TOTAL_VOTANTES']/df0['CENSO_ELECTORAL'])
else:
    print ('¡OK!\n')
    print('Porcentaje de Votantes:',100*df0['TOTAL_VOTANTES'].sum()/df0['CENSO_ELECTORAL'].sum(),'%')

W1=[]#datos de provincia y votos de cada partidos
W2=[]#escaños de cada partido
for i in range(0,list(df0.keys()).index("1Votos")):
    W1.append(df0.loc[0].keys()[i])
for i in range(0,len(df0.keys())):
    if ('Votos' in df0.loc[0].keys()[i]):
        W1.append(df0.loc[0].keys()[i])
   
    if ('Diputados' in df0.loc[0].keys()[i]):
        W2.append(df0.loc[0].keys()[i])

Y=[]#nombres de columnas con los votos a cada partido
leng=len(W1)
for x in range(0,leng):
    if ('Votos' in W1[x]):
        Y.append(W1[x])


Z=[]#nombres de columnas con los diputados a cada partido
for x in range(0,len(W2)):
    if ('Diputados' in W2[x]):
        Z.append(W2[x])

new_l=Y

new_d=Z

dfaux0=df0[W1]#datos censales y resumidos por provincia


dfaux1=df0[W2[0:]]

# +
#df1

df1=pd.concat([dfaux0,dfaux1], axis=1)
# -

Var=dict(zip(W1[pos(df1,'1Votos'):],l))#diccionario que asigna votos a 
#identificación numérica de partido


a1=pos(df1,'Número de mesas')

a2=pos(df1,'Censo electoral sin CERA')

a3=pos(df1,'Censo CERA')

# +
#eliminamos ciertas columnas innecesarias (a1=Número de mesas, a3=Censo CERA,...)
#para obtener df1

df1 = df1.drop(df1.columns[[ a1,a2,a3]], axis=1)
# -


estructura(df1)

print('La barrera electoral es \n 0.03 para el Congreso\n 0.05 para las eleciones en la CAM y\n 0 para el Europarlamento')

barrera=input('barrera electoral (<1)')
barrera=float(barrera)

#inserto número de partidos
df1.insert(loc = pos(df1,'CENSO_ELECTORAL'),
          column = 'NPARTIDOS',
          value =N_PARTIDOS)


#partidos con más votos que la barrera electoral
df1.insert(loc = pos(df1,'CENSO_ELECTORAL'),
          column ='PARTIDOS>' ,
          value =0)


for x in l:
    columna='%'+x
    df1[columna]=df1[x+'Votos']/df1['VOTOS_VÁLIDOS']


# +
#################################################################################################################################

# +
#PARTE II: INTRODUCIR GRUPOS
# -

guion="PARTE II"

df11=df1.copy()

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

list_vgroups

#grupos para votos >barrera
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
df11= df11.reindex(columns = df11.columns.tolist() 
                                  + vot_grupos)


#diputados por grupos por provincias
df11= df11.reindex(columns = df11.columns.tolist() 
                                  + dgrupos)

for j in range(N_PROV):
    for x in dgrupos:
        df11.loc[j,list_dgroups[x]]=0

#extraigo los diputados a cada candidatura y provincia
diputados=df11.copy()
diputados=diputados[diputados.columns.intersection(Z)]    

#votos por grupos por provincias
for j in range (N_PROV):#provincias
    print('\n','PROVINCIA',df11.loc[j]['PROVINCIA'].strip(),f'{j:,.0f}','\n')
    S=0
    for x in vot_grupos:#grupos de partidos
        print(x, f'{df11.loc[j][list_vgroups[x]].sum():,.0f}')
        S=S+df11.loc[j][list_vgroups[x]].sum()
    print('--TOTAL VOTOS ',f'{S:,.0f}')
#los diputados habrán de asignarse por el método d'Hondt

#votos>barrera por grupos por provincias
df11= df11.reindex(columns = df11.columns.tolist() 
                                  + grupos)


df=df1.rename(columns=Var)

estructura(df11)

U0=[i for i in range(0,pos(df11,'1Votos'))]
U1=[i for i in range(pos(df11,'1Votos'),pos(df11,'1Diputados'))]
U2=[i for i in range(pos(df11,'VDERECHA'),pos(df11,'VOTROS')+1)]
U3=[i for i in range(pos(df,'1'),pos(df,'1Diputados'))]
U4=[i for i in range(pos(df11,'DERECHA'),pos(df11,'OTROS')+1)]
U5=[i for i in range(pos(df11,'1Diputados'),pos(df11,'%1'))]
U6=[i for i in range(pos(df11,'DDERECHA'),pos(df11,'DOTROS')+1)]

VV=[]
UU0=list(df11.loc[0][U0].keys())
UU1=list(df11.loc[0][U1].keys())
UU2=list(df11.loc[0][U2].keys())
UU3=list(df.loc[0][U3].keys())
UU4=list(df11.loc[0][U4].keys())
UU5=list(df11.loc[0][U5].keys())
UU6=list(df11.loc[0][U6].keys())
UU=UU0+UU1+UU2+UU3+UU4+UU5+UU6

# +

df12=pd.concat([df11[UU0],df11[UU1],df11[UU2],df[UU3],df11[UU4],df11[UU5],df11[UU6]], axis=1)
df12=df12.fillna(0)
# -

estructura(df12)

print("---------------------------------------------------","TERMINADO:",guion)

# +
################################################################################################################################

# +
#PARTE III: ELIMINAR CANDIDATURAS <barrera
# -

guion="PARTE III"

df3=df12.copy()


df1.loc[:]['%1']

l_barr=[[] for j in range(N_PROV)]
for j in range (N_PROV):
    for x in l:
        if df1.loc[j]['%'+x] < barrera:
            df3.loc[j,x]=0
            l_barr[j].append(x)
        else:
            df3.loc[j,x]=df1.loc[j][x+'Votos']

for j in range (N_PROV):#provincias
    Su=0
    for x in l:
        if df1.loc[j]['%'+x] >= barrera:#partidos que superan la barrera
            Su=Su+1
        df3.loc[j,'PARTIDOS>']=Su


df3.loc[:]['PARTIDOS>']

df3.insert(loc = 5,
          column = 'VOTOS_REPARTIR',
          value =df3[l].sum(axis=1))

print("---------------------------------------------------","TERMINADO:",guion)

# +
#PARTE IV: TABLAS d'HONDT
# -

guion="PARTE IV"

list1 = [int(x) for x in list(df2.keys())]
list1.sort()
claves = [str(x) for x in list1]

#lista de partidos por provincia que superan la barrera
no_nulos=[[] for j in range(N_PROV)]
for j in range(N_PROV):
    for x in claves:
        if(df3.loc[j][x])!=0:
            no_nulos[j].append(x)    

#partidos que superan el mínimo de votos (barrera) en provincia 30
no_nulos

Koef=[[] for j in range(N_PROV)]
for j in range(N_PROV):
    coef=[i for i in range(1,int(df3.loc[j]['DIPUTADOS'])+1)]
    for k in no_nulos[j]:
        x=dict.fromkeys(['partido','diputados'])
        x1 = dict.fromkeys([i for i in range(1,int(df3.loc[j]['DIPUTADOS'])+1)], [])
        x.update(x1)
        x['partido']=k
        x['diputados']=int(df3.loc[j]['DIPUTADOS'])
        for l in coef:
            x[l]=0
        Koef[j].append(x)


K=[[] for j in range(N_PROV)]
#genero DataFrames para tablas d'Hondt a partir de los diccionarios
for j in range(N_PROV):    
    K[j]=pd.DataFrame(Koef[j])  
    K[j].insert(loc=0, column='provincia', value=0, allow_duplicates = False)

dHondt=[[] for i in range(N_PROV)]
for i in range(len(df3)):
    dHondt[i]=pd.DataFrame(K[i])
    dHondt[i].index=list(dHondt[i][:]['partido'])

for i in range(N_PROV):
     for k in list(dHondt[i][:]['partido']):
        dHondt[i].loc[(k),'provincia']=i

# +

for j in range(N_PROV):
    #print('provincia',j)
    for l in no_nulos[j]:
     #   print('partido',l)
        for m in range (1,int(df3.loc[j]['DIPUTADOS'])+1):
            a=df3.loc[j][l]/m
            dHondt[j].loc[l,m]=a
# -

lista_votos=[[] for i in range(N_PROV)]
for i in range(N_PROV):
    N_DIP=list(dHondt[i].keys())[3:]
    PARTS=list(dHondt[i].index)
    lista_votos[i]=[]
    for j in PARTS:
        #print('provincia',i,list(dHondt[i].loc[j][2:]))
        lista_votos[i]=lista_votos[i]+list(dHondt[i].loc[j][3:])
        lista_votos[i].sort(reverse=True)

#Exporto d'Hondt 
F=input("¿DESEA EXPORTAR LAS TABLAS d'HONDT? (Y/N)")
if F=='Y' or F=='Y'.lower():
    sufijo=input("AÑADA SUFIJO A LAS TABLAS d'HONDT O BLANCO")
    for i in range(N_PROV):
        A=dHondt[i] 
        B=pd.DataFrame(lista_votos[i])
        B[B>0].dropna(axis=0, how='all') 
        Name='dHondt'+str(i)+sufijo
        writer = pd.ExcelWriter(Name+sufijo+'.xlsx')
        A.to_excel(writer,'dHondt')
        B.to_excel(writer,'lista_votos')
        writer.close()

print("---------------------------------------------------","TERMINADO:",guion)


# +
#PARTE V: COMPROBAR SI HAY EMPATES
# -

guion="PARTE V"

# +
#vemos la lista de los valores de la tabla d'Hondt repetidos en cada provincia:  repitentes[I] extaídos de lista_votos[I]
repitentes=[[] for i in range(N_PROV) ]
S=0
PR=[]
for i in range(N_PROV):
    D=([x for x in lista_votos[i] if lista_votos[i].count(x) >= 2])
    D.sort(reverse=True)
    
    for j in range(len(D)):
        if D[j]!=0:
            repitentes[i].append(D[j])
            a=repitentes[i][j]
            S=S+1
            PR.append(i)
    if len(repitentes[i])>0:       
        print('provincia: ', df3.loc[i]['PROVINCIA'],i,'\n',repitentes[i])

if S==0:
    print('NO HAY CANDIDATURAS EMPATADAS')
    Empates=0
    
else:
    print('Hay candidaturas empatadas en provincias',set(PR))
    Empates=1
# -

print("---------------------------------------------------","TERMINADO:",guion)


# +
#PARTE VI: SI HAY EMPATES
# -

guion="PARTE VI"

repeated=[[] for i in range(N_PROV)]
for i in range(N_PROV):
    my_set = {s for s in repitentes[i]}
    repeated[i]=list(my_set)
    repeated[i].sort(reverse=True)
#valores repetidos en cada provincia en la tabla d'Hondt (un solo valor)

repeated[2]

#defino función que identifica y recopila valores repetidos
from collections import defaultdict
def list_duplicates(seq):
    tally = defaultdict(list)
    for i,item in enumerate(seq):
        tally[item].append(i)#tally es diccionario que asigna a cada valor los índices en que aparece
    return ((key,locs) for key,locs in tally.items() if len(locs)>1)#solo se queda con los índices de valores repetidos
#devuelve un diccionario en el que la key es el elemento de seq y el value es una lista de los índices
#en que aparece


# +
repeat_loc=[[] for i in range(N_PROV)]
for i in range(N_PROV):
    for dup in list_duplicates(lista_votos[i]):
        repeat_loc[i].append(dup)
        repeat_loc[i] = sorted(list_duplicates(lista_votos[i]),reverse=True)
        
#tuplas que asocian key=VALOR repetido con value lista de los ÍNDICES de lista_votos[I]
#en la mayoría de casos es 0 el único valor que se repite
# -

for i in range(N_PROV):
    for j in range (len(repeat_loc[i])):
        a=min([x for x in repeat_loc[i][j][1]])
        b=max([x for x in repeat_loc[i][j][1]])
        c=df3.loc[i]['DIPUTADOS']-1
        
        if(b>c and a<=c):
           
            print('Se precisa sorteo en provincia Nº', i,'(',df3.loc[i]['PROVINCIA'].strip(),')')
            print('Mínimo',a,'; Índice',c,'; Máximo',b)
         #   print(i,df3.loc[i]['PROVINCIA'].strip(),j,b>=df3.loc[i]['DIPUTADOS'] and a<=df3.loc[i]['DIPUTADOS'])

#devuelve el rango de las posiciones de lista_votos en que se repite el valor que ha de ser asignado
#a un partido aleatoriamente ya que el coeficiente de d'Hondt es el mismo para varios partidos.
locations=[[] for i in range(N_PROV)]
for i in range(N_PROV):
    for j in range (len(repeat_loc[i])):
        a=min([x for x in repeat_loc[i][j][1]])
        b=max([x for x in repeat_loc[i][j][1]])
        e=b-a+1
        if(b>df3.loc[i]['DIPUTADOS']-1 and a<=df3.loc[i]['DIPUTADOS']-1):
            print('Provincia Nº:',i,'(',df3.loc[i]['PROVINCIA'].strip(),')')
            print('Escaños a sortear:',e,'entre las candidaturas de índices',repeat_loc[i][j][1])
            print('Mínimo:',min([x for x in repeat_loc[i][j][1]]),'; Máximo:', max([x for x in repeat_loc[i][j][1]]),'\n')
            
            locations[i].append(a)
            locations[i].append(b)
#muchas de ellas no serán susceptibles de sorteo al no cubrir
#el número de diputados de la provincia


if not any(locations):
    print("locations está vacío")
else:
    for i in range(N_PROV):
        if len(locations[i])!=0:
            print('Provincia Nº:',i,'(',df3.loc[i]['PROVINCIA'].strip(),'):',locations[i],';N_DIPUTADOS:',int(df3.loc[i]['DIPUTADOS']))
#nos da el índice mínimo  y el máximo que comprende el número de DIPUTADOS
#donde la lista está vacía, no hay coeficientes d'Hondt duplicados.
#donde no está vacía muestra el rango [MIN,MAX] en el que se encuentran los coeficientes empatados y
#el intervalo siempre ha de cubrir el valor del número de diputados asignados a la provincia.

# +
#el número de veces que se ha de elegir al azar en cada provincia
n_rep=[]
pr_alea=[]#provincias donde hacer sorteo
for i in range(N_PROV):
    try:
        n=(+int(df3.loc[i]['DIPUTADOS'])-min(locations[i]))
        print('Provincia Nº:',i,'(',df3.loc[i]['PROVINCIA'].strip(),'):',' SELECCIONES ALEATORIAS ',n)
        n_rep.append(n)
        pr_alea.append(i)
    except:
        n_rep.append(0)

s=[(i,df3.loc[i]['PROVINCIA'].strip()) for i in range(N_PROV)]
n_rep1=list(zip(s,n_rep))
print(n_rep1)
#n_rep1 asocia para cada provincia el número de veces a elegir al azar

# +
#comprobación del muestreo
# -

import random
M=[[] for o in range(N_PROV)]
for o in range(N_PROV):
    try:
        m=[i for i in range(min(locations[o]),max(locations[o])+1)]
        M[o].append(m)
        print('POSICIONES A SORTEAR EN PROVINCIA:',o,';Número:',len(M[o]),';',M[o])
    except:
        continue


#función que valora la frecuencia de cada partido en el sorteo
def suerte(provincia,veces):
    N=[[] for o in range(N_PROV)]
    for i in range(veces):

        for k in pr_alea:
            for j in range(len(M[k])):    
                r=random.sample(M[k][0], int(df3.loc[k]['DIPUTADOS'])-min(locations[k]))
                r.sort()

                #print ('pasada',i+1,'provincia',k,'muestra',r)
                N[k].append(r)
    cuenta=pd.DataFrame(N[provincia], columns = ['alea'])
    return('Porcentaje de cada valor del indice:',100*(cuenta['alea'].value_counts())/veces)


#provincias con y sin duplicados
S1=0
S2=0
for i in range(N_PROV):
    if n_rep[i]==0:
        #print('\n','SIN DUPLICADOS','\n')
        #print('PROVINCIA ',i,'\n',dHondt[i],'\n')
        S1=S1+1
    else:
        # dHondt con duplicados
        if max(locations[i])+1-min(locations[i])<=df3.loc[0]['NPARTIDOS']:
            print('PROVINCIA CON DUPLICADOS',df3.loc[i]['PROVINCIA'].strip(),i,'\n','NÚMERO DE PARTIDOS EMPATADOS ',
                  max(locations[i])+1-min(locations[i]))
            S2=S2+1
print('\n','NÚMERO DE PROVINCIAS SIN DUPLICADOS',S1,'\n','NÚMERO DE PROVINCIAS CON DUPLICADOS',S2)


#función que cuenta el número de diputados que cada partido obtiene en función del orden en tabla dHondt
def CountFrequency(my_list):
    count = {}
    for i in my_list:
        count[i] = count.get(i, 0) + 1
    return count


import numpy as np
#es la función que localiza valores en DataFrame
M=np.array(dHondt[3],dtype=float)
i,j=np.where(np.isclose(M, 39357.3333333333,rtol=0,atol=0.01))
indices=list(zip(i,j))#tupla que da el número de fila y el de columna (f,c) de la tabla d'Hondt
print('Indices',indices)

i,j
#devuelve una tupla

#provincias sin sorteo
dipus=[[] for k in range(N_PROV)]
num_part=[]
elements_count=[[] for k in range(N_PROV)]
for k in range(N_PROV):
    dipus[k]=[]
    if n_rep[k]==0:
        f=[]
        for x in list(set(lista_votos[k][0:int(df3.loc[k]['DIPUTADOS'])])):
            M=np.array(dHondt[k],dtype=float)
            i,j=np.where(np.isclose(M,x))
            f.append(list(i))
        #print(k,f)
        
        for z in range(len(f)):
            dipus[k]=dipus[k]+f[z]
        a=CountFrequency(dipus[k])
        elements_count[k].append(a)
    num_part.append(elements_count[k])

#lista de candidaturas que recibirán diputados sin muestreo 
#ordenadas según la regla d'Hondt
S=0
for i in range (N_PROV):
    S=S+1
    print(df3.loc[i]['PROVINCIA'],dipus[i],len(dipus[i]))
print(S)

l=[]
for item in df2:
    l.append(str(item))
Dl=[]
for x in l:
    columna='DIPUTADOS'+x
    Dl.append(columna)

type(dHondt[0])

for j in range(N_PROV):
    for x in Dl:
        df3.loc[j,x]=0

#corrijo los dHondt para que coincidan los índices con el número de partido
pretty_dict=[[] for x in range(N_PROV)]
indhondt=[[] for x in range(N_PROV)]
indi=[[] for x in range(N_PROV)]
indef=[[] for x in range(N_PROV)]
for j in range(N_PROV):
    indhondt[j]=[int(i) for i in dHondt[j].index.tolist()]
    indi[j]=[i for i in range(len(dHondt[j].index.tolist()))]
    indef[j]=dict(zip(indi[j],indhondt[j]))
    #print(j, indef[j])
    try:
        pretty_dict[j] = {indef[j][k]: v for k, v in elements_count[j][:][0].items()}
    except:
        continue


#Asigno diputados a provincias donde no hay empates
df4=df3.copy()
P=[[] for k in range(N_PROV)]
for k in range(N_PROV):
    for j in list(pretty_dict[k]):
        P[k].append('DIPUTADOS'+str(j))
    if n_rep[k]==0:#si no hay duplicados en la provincia n_rep[k]==0
        
        for x in P[k]:
            df4.loc[k,x]=pretty_dict[k][int(x[9:])]

df4.loc[:]['DIPUTADOS3']

#lista de provincias sin empates
nemp=[]
for k in range(N_PROV):
    if n_rep[k]==0:
        nemp.append(df1.loc[k]['PROVINCIA'].strip())
emp=[]
#lista de provincias con empates
for k in range(N_PROV):
    if n_rep[k]!=0:
        emp.append(df1.loc[k]['PROVINCIA'].strip())


emp

nemp

#provincias con empates
dipus1=[[] for k in range(N_PROV)]
elements_count1=[[] for k in range(N_PROV)]
loto=[]
dipus2=[[] for k in range(N_PROV)]
dipus3=[[] for k in range(N_PROV)]
for k in range(N_PROV):
    dipus1[k]=[]
    if n_rep[k]!=0:
        
        E=set(lista_votos[k][0:int(df4.loc[k]['DIPUTADOS'])])
        F=list(E)
        F.sort(reverse=True)
        for x in F:#coeficientes d'Hondt a considerar
            M=np.array(dHondt[k],dtype=float)
            i,j=np.where(np.isclose(M,x,rtol=0,atol=0.01))
            v=list(zip(i,j))
            print(k,x,v,i[0])
            dipus1[k].append(v)
            flat_list = [item for sublist in dipus1[k][:] for item in sublist]
            dipus2[k]= [item for item in flat_list[:min(locations[k])]]
            dipus3[k]=[item for item in flat_list[min(locations[k]):]]
#dipus3 contiene para cada provincia los indices de los partidos
#entre los que hay que sortear los escaños.
#si p.e. dipus3[7]=[(0, 6), (2, 6)] quier decir que el sorteo tendrá que
#elegir entre una de las dos tuplas.


#asignación por sorteo
dipus4=[[] for k in range(N_PROV)]
for k in range(N_PROV):
    try:
        w=int(df4.loc[k]['DIPUTADOS'])-min(locations[k])
        print(w)
        r=random.sample(dipus3[k][:], w)
        print(k,r)
        dipus3[k]=(dipus2[k]+r)
        for i in range(len(dipus3[k])):
            dipus4[k].append(dipus3[k][i][0])
    except:
        continue
#dipus4 lista los indices de los partidos que reciben diputado.
#P.e. si dipus4[3]=[2, 3, 2, 2, 3, 2, 1] la provincia 4 recibe
# 4 escaños para el partido de índice 2, 2 escaños para el 
#de índice 3 y 1 escaño para el partido 1.

df4.loc[:]['DIPUTADOS1']

elements_count1=[[] for k in range(N_PROV)]
for k in pr_alea:
    a=CountFrequency(dipus4[k])
    elements_count1[k].append(a)
    print(k,elements_count1[k][0])
# el diccionario elements1_count[k] nos da el par (PARTIDO, ESCAÑOS) para cada PROVINCIA k

#corrijo los dHondt para que coincidan los índices con el número de partido
New_pretty_dict=[[] for x in range(N_PROV)]
New_indhondt=[[] for x in range(N_PROV)]
New_indi=[[] for x in range(N_PROV)]
New_indef=[[] for x in range(N_PROV)]
for j in range(N_PROV):
    New_indhondt[j]=[int(i) for i in dHondt[j].index.tolist()]
    New_indi[j]=[i for i in range(len(dHondt[j].index.tolist()))]
    New_indef[j]=dict(zip(New_indi[j],New_indhondt[j]))
    print(j, New_indef[j])
    try:
        New_pretty_dict[j] = {New_indef[j][k]: v for k, v in elements_count1[j][:][0].items()}
    except:
        continue


print("---------------------------------------------------","TERMINADO:",guion)

# +
#PARTE VII: ASIGNACIÓN DE ESCAÑOS DEFINITIVA
# -

guion="PARTE VII"

df5=df4.copy()

#votos por grupo político
df6=df5.copy()
for k in range(N_PROV):
    for x in grupos:
        df6.loc[k,x]=df6.loc[k][list_groups[x]].sum()


#diputados por grupo político
for k in range(N_PROV):
    for x in dgrupos:
        df6.loc[k,x]=df6.loc[k][list_dgroups[x]].sum()

df7=df6.copy()
import warnings
warnings.filterwarnings("ignore")
for k in range(N_PROV):
    for x in grupos:
        df7.loc[k,x]=df7.loc[k][list_groups[x]].sum()
df7 = df7.fillna(0)


df=df0.copy()
for j in range(N_PROV):
    for x in l:
        df.loc[j,x]=df0.loc[j][x+'Votos']

for j in range (N_PROV):#provincias
    for x in vot_grupos:#grupos de partidos
        df7.loc[j,x]=df7.loc[j][list_vgroups[x]].sum()

df7.loc[0]['VDERECHA']

#grupos para diputados
dipugrupos=['DIPDERECHA',
'DIPCENTRO',
'DIPIZQUIERDA',
'DIPNACIONALISTAS',
'DIPOTROS']

#asignar a cada grupo sus partidos para escaños
list_dipugroups = {key: None for key in dipugrupos}
for x in dipugrupos:#nombres de los grupos (CENTRO, DERECHA,...)
    D=[]
    
    for i in df2.loc[2][:]:#nombres de los partidos (1,2,...NPARTIDOS)
        if df2.loc[1][i] ==re.sub('DIP', '', x):
            D.append('DIPUTADOS'+str(i))
    #print(x,C)
    list_dipugroups[x]=D

df71=df7.copy()
df71= df71.reindex(columns = df71.columns.tolist() 
                                  + dipugrupos)
df71=df71.fillna(0)

estructura(df71)

for j in range (N_PROV):#provincias
    for x in dipugrupos:#grupos de partidos
        df71.loc[j,x]=df71.loc[j][list_dipugroups[x]].sum()

new_l

new_d

Diputats = ['DIPUTADOS'+str(x) for x in list(df2.keys())]


Diputats

#en caso de que los nuevos datos de diputados no se compadezcan con los de la  Xunta (por haber cambiado
# el número de diputados por circunscripción, p.e) igualamos los diputados iniciales con los calculados.
DF71=df71.copy()
for j in range (N_PROV):#provincias
    for x in Diputats:
        DF71.loc[j,re.sub('DIPUTADOS','',x)+'Diputados']=DF71.loc[j,x]
for j in range (N_PROV):#provincias
    for x in dipugrupos:
        DF71.loc[j,'D'+re.sub('DIP','',x)]=DF71.loc[j,x]

estructura(DF71)

V0=[i for i in range(0,pos(DF71,'DIPUTADOS')+1)]
V1=[i for i in range(pos(DF71,'1Votos'),pos(DF71,'VDERECHA'))]
V2=[i for i in range(pos(DF71,'VDERECHA'),pos(DF71,'1'))]
V3=[i for i in range(pos(DF71,'1Diputados'),pos(DF71,'DDERECHA'))]
V4=[i for i in range(pos(DF71,'DDERECHA'),pos(DF71,'DIPUTADOS1'))]
V5=[i for i in range(pos(DF71,'1'),pos(DF71,'DERECHA'))]
V6=[i for i in range(pos(DF71,'DERECHA'),pos(DF71,'1Diputados'))]
V7=[i for i in range(pos(DF71,'DIPUTADOS1'),pos(DF71,'DIPDERECHA'))]
V8=[i for i in range(pos(DF71,'DIPDERECHA'),pos(DF71,'DIPOTROS')+1)]


VV=[]
VV0=list(DF71.loc[0][V0].keys())
VV1=list(DF71.loc[0][V1].keys())
VV2=list(DF71.loc[0][V2].keys())
VV3=list(DF71.loc[0][V3].keys())
VV4=list(DF71.loc[0][V4].keys())
VV5=list(DF71.loc[0][V5].keys())
VV6=list(DF71.loc[0][V6].keys())
VV7=list(DF71.loc[0][V7].keys())
VV8=list(DF71.loc[0][V8].keys())
VV=VV0+VV1+VV2+VV3+VV4+VV5+VV6+VV7+VV8
NV=VV1+VV2+VV3+VV4+VV5+VV6+VV7+VV8

NV

DF71.loc[0][vot_grupos]

resultados=DF71[NV]

estructura(resultados)

print("---------------------------------------------------","TERMINADO:",guion)

# +
#################################################################

# +
#PARTE VIII: ARCHIVO DE SALIDA EXCEL
# -

guion="PARTE VIII"

#salida con ceros de asignaciones
output3=pd.concat([DF71[VV0],DF71[VV1],DF71[VV2],DF71[VV7],DF71[VV8]],axis=1)

estructura(output3)

B=[]
M1=[i for i in range(pos(output3,'1Votos'),pos(output3,'DIPDERECHA'))]
M=list(output3.loc[0][M1].keys())
for y in M:
    if (output3[y] == 0).all():
        B.append(y)

common=set(B).intersection(set(output3.loc[0].keys()))
#salida sin ceros de asignaciones
output4=output3.drop(columns=list(common),axis=1)

#salida de >barrera con ceros
output5=pd.concat([DF71[VV0],DF71[VV5],DF71[VV6],DF71[VV7],DF71[VV8]],axis=1)

X=[]
X=VV5+VV7
C=[]
M=list(output5.loc[0][X].keys())
for y in M:
    if (output5[y] == 0).all():
        C.append(y)

common=set(C).intersection(set(output5.loc[0].keys()))
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
        results=output4
        results.to_excel(writer,sheet_name='VotosReasignados')
        results=output6
        results.to_excel(writer,sheet_name='Datos>barrera')
        writer.close()
    if G=='N' or G=='N'.lower():
        writer = pd.ExcelWriter(Name+'.xlsx')
        results=output3
        results.to_excel(writer,sheet_name='VotosReasignados')
        results=output5
        results.to_excel(writer,sheet_name='Datos>barrera')
        writer.close()

# -

print("---------------------------------------------------","TERMINADO EL PROGRAMA")
