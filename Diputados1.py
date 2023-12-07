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


#defino función que encuentra osición de columna en df
def pos(df,col):
    return(list(df.keys()).index(col))


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
    print('Porcentaje de Votantes:',100*df0['TOTAL_VOTANTES'].sum()/df0['CENSO_ELECTORAL'].sum(),'%')

#inserto participación por provincia
df0.insert(loc = pos(df0,"VOTOS A CANDIDATURAS"),
          column = '%PARTICIPACIÓN',
          value =df0['TOTAL_VOTANTES']/df0['CENSO_ELECTORAL'])


dfaux0=df0[W1[0:pos(df0,"1Votos")-1]]#datos censales y resumidos por provincia


dfaux1=df0[W1[pos(df0,"1Votos")-1:pos(df0,"1Diputados")-1]]

dfaux2=df0[W2[0:]]

# +
#df1

df1=pd.concat([dfaux0,dfaux1,dfaux2], axis=1)
# -

a1=pos(df1,'Número de mesas')

a2=pos(df1,'Censo electoral sin CERA')

a3=pos(df1,'Censo CERA')

a4=pos(df1,'Solicitudes voto CERA aceptadas')

a5=pos(df1,'Total votantes CER')

a6=pos(df1,'Total votantes CERA')

# +
#eliminamos ciertas columnas innecesarias (a1=Número de mesas, a3=Censo CERA,...)
#para obtener df1

df1 = df1.drop(df1.columns[[ a1,a2,a3,a4,a5,a6]], axis=1)
# -


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
#PARTE II: INTRODUCIR GRUPOS
# -

#agrupaciones para votos registrados
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
    list_vgroups[x]=C


#grupos para votos > barrera electoral
grupos=['DERECHA',
'CENTRO',
'IZQUIERDA',
'NACIONALISTAS',
'OTROS']

#grupos para votos> barrera electoral
import re
list_groups = {key: None for key in grupos}
for x in grupos:#nombres de los grupos (CENTRO, DERECHA,...)
    C=[]
    
    for i in df2.loc[2][:]:#nombres de los partidos (1,2,...NPARTIDOS)
        if df2.loc[1][i] ==re.sub('V', '', x):
            C.append(str(i))
    #print(x,C)
    list_groups[x]=C

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

#votos por grupos por provincias
df1= df1.reindex(columns = df1.columns.tolist() 
                                  +vot_grupos+dgrupos+grupos)


# +
for j in range (N_PROV):
    for x in l:
        columna='%'+x 
        if df1.loc[j,columna]<barrera:
            df1.loc[j,x]=0
        else:
            df1.loc[j,x]=df1.loc[j][x+"Votos"]
            
       
    
# -

for j in range (N_PROV):#provincias
    for x in vot_grupos:#grupos de partidos
        df1.loc[j,x]=df1.loc[j][list_vgroups[x]].sum()

#votos por grupos por provincias
for j in range (N_PROV):#provincias
    S=0
    for x in dgrupos:#grupos de partidos
        df1.loc[j,x]=df1.loc[j][list_dgroups[x]].sum()

#votos por grupos por provincias
for j in range (N_PROV):#provincias
    S=0
    for x in grupos:#grupos de partidos
        df1.loc[j,x]=df1.loc[j][list_groups[x]].sum()

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

results=df1.copy()

# +
#PARTE III: ARCHIVO DE SALIDA EXCEL
# -

percent=list(results.loc[0][:].keys()[pos(df1,"%1"):pos(df1,'VDERECHA')+1])


#chequeos
#suma de votos igual a votos a candidaturas
for j in range (N_PROV):#provincias
    print('\n','PROVINCIA',results.loc[j]['PROVINCIA'].strip(),f'{j:,.0f}')
    S=0
    S1=0
    for x in new_l:#votos de partidos
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
        S=S+results.loc[j][x]
    for y in Y:
        S1=S1+results.loc[j][y].sum()
    a=results.loc[0]['CENSO_ELECTORAL']
    print('--CENSO ELECTORAL',f'{a:,.0f}','\n','--TOTAL VOTOS',f'{S1:,.0f}','\n','--DIPUTADOS A CANDIDATURAS',
         f'{S:,.0f}')

# +
D=[]
for y in l:
    
    if (df1.loc[:][y].sum()!=0):
        
        D.append(int(y))
        
D=list(set(D))
D.sort()#partidos que superan la barrera
# -

for x in range(0,len(D)):
    D[x]=str(D[x])


for j in range (N_PROV):#provincias
    Su=0
    for x in D:#partidos que superan la barrera
        if df1.loc[j][x].any()!=0:
            Su=Su+1
    df1.loc[j,'PARTIDOS>']=Su

to_remove=list(set(l)-set(D))

U0=[i for i in range(0,pos(df1,'1Votos'))]
UU0=list(df1.loc[0][U0].keys())
U1=[i for i in range(pos(df1,'DDERECHA'),pos(df1,'DNACIONALISTAS')+1)]
UU1=list(df1.loc[0][U1].keys())

masde=pd.concat([df1[UU0],df1[l],df1[UU1]],axis=1)

masde=masde.drop(columns=to_remove)

#votos por grupos por provincias
for j in range (N_PROV):#provincias
    S=0
    for x in grupos:#grupos de partidos
        masde.loc[j,x]=masde.loc[j][list(set.intersection(set(list_groups[x]),set(D)))].sum()

U=[i for i in range(pos(df1,'%1'),pos(df1,'VDERECHA'))]
borrar=list(df1.loc[0][U].keys())

df1=df1.drop(columns=borrar)

A=[]
M1=[i for i in range(pos(df1,'DIPUTADOS')+1,pos(df1,'VDERECHA'))]
M=list(df1.loc[0][M1].keys())
for y in M:
    if (df1[y] == 0).all():
        A.append(y)

U0=[i for i in range(0,pos(df1,'DIPUTADOS')+1)]
U1=[i for i in range(pos(df1,'1Votos'),pos(df1,'1Diputados'))]
U2=[i for i in range(pos(df1,'VDERECHA'),pos(df1,'DDERECHA'))]
U3=[i for i in range(pos(df1,'1Diputados'),pos(df1,'VDERECHA'))]
U4=[i for i in range(pos(df1,'DDERECHA'),pos(df1,'DERECHA'))]
UU0=list(df1.loc[0][U0].keys())
UU1=list(df1.loc[0][U1].keys())
UU2=list(df1.loc[0][U2].keys())
UU3=list(df1.loc[0][U3].keys())
UU4=list(df1.loc[0][U4].keys())

resultados=pd.concat([df1[UU0],df1[UU1],df1[UU2],df1[UU3],df1[UU4]], axis=1)

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
        masde.to_excel(writer,sheet_name='Datos>barrera')
        writer.close()
    if G=='N' or G=='N'.lower():
        writer = pd.ExcelWriter(Name+'.xlsx')
        resultados.to_excel(writer,sheet_name='DatosMint1')
        resultados.to_excel(writer,sheet_name='Datos>barrera')
        writer.close()


# +
#PARTE IV: GUARDAR FICHEROS DE INTERÉS

# +
#creo un diccionario inverso
b=[x[1:] for x in (vot_grupos)]
party_grupo={}
  
for j in range(len(b)):
    S=list(list_vgroups.values())[j]
    #print(S)
    T=vot_grupos[j]
    #print(T)
    #print(dict(zip(S,T)))
    U=[vot_grupos[j][1:] for i in range(len(list_vgroups[vot_grupos[j]]))]
    #print(dict(zip(S,U)),len(dict(zip(S,U))))
    party_grupo.update(dict(zip(S,U)))



# +
# lista de comunidades
CA1=list(set(df0['COMUNIDAD']))

for x in range(len(CA1)):
    CA1[x]=CA1[x].strip()

#diccionario con provincias correspondientes a cada CA
CA=dict.fromkeys(CA1, []) 
for y in CA1:
    U=[]
    print(y)
    for x in range(len(df0)):
        if df0.loc[x]['COMUNIDAD'].strip()==y:
            print(df0.loc[x]['NPROVINCIA'])      
            U.append(list(df0.loc[:]['PROVINCIA'].keys())[x])
    CA[y]=U


# -


# provincias
dfprov=df0.loc[:][['NPROVINCIA','PROVINCIA']]

#exporto ficheros de interés
df0.to_pickle(dire+"\\df0.pkl")
df1.to_pickle(dire+"\\df1.pkl")
df2.to_pickle(dire+"\\df2.pkl")
dfprov.to_pickle(dire+"\\dfprov.pkl")
resultados.to_pickle((dire+"\\resultados.pkl"))
variables={}
variables['N_PROV']=N_PROV
variables['N_PARTIDOS']=N_PARTIDOS
d=open(dire+"\\new_l.pkl","wb")
pickle.dump(new_l,d)
d.close()
e=open(dire+"\\new_d.pkl","wb")
pickle.dump(new_d,e)
e.close()
h = open(dire+"\\variables.pkl","wb")
pickle.dump(variables,h)
h.close()
q = open(dire+"\\l.pkl","wb")
pickle.dump(l,q)
q.close()
s=open(dire+"\\CA.pkl","wb")
pickle.dump(CA,s)
s.close()
u=open(dire+"\\dfprov.pkl","wb")
pickle.dump(dfprov,u)
u.close()
t = open(dire+"\\vot_grupos.pkl","wb")
pickle.dump(vot_grupos,t)
t.close()
n=open(dire+"\\party_grupo.pkl","wb")
pickle.dump(party_grupo,n)
n.close()
v=open(dire+"\\list_vgroups.pkl","wb")
list_vgroups=pickle.dump(list_vgroups,v)
v.close()
w=open(dire+"\\list_dgroups.pkl","wb")
list_dgroups=pickle.dump(list_dgroups,w)
w.close()
