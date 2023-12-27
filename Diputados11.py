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
#DIPUTADOS1

# %%
#PARTE I: IMPORTACIÓN DE DATOS

# %%
guion="Diputados11"

# %%
#importar datos de las elecciones. Son del Ministerio del Interior adaptados
import pandas as pd 
import pickle
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
#defino función que encuentra posición de columna en df
def pos(df,col):
    return(list(df.keys()).index(col))


# %%
#genero la lista de claves de partidos
l=[]
for item in df2:
    l.append(str(item))

# %%
party1=set(df2.loc[1])
grupos=list(party1)
party2=pd.Series(df2.columns.values,index=df2.columns.values)
party2=pd.DataFrame(party2)


# %%
#añado a cada partido un número de identificación que será el usado en adelante
warnings.filterwarnings("ignore")
df2=pd.concat([df2,pd.DataFrame(party2.T)],ignore_index=True).copy()


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
    print ('¡OK!\n')
    print('Porcentaje de Votantes:',100*df0['TOTAL_VOTANTES'].sum()/df0['CENSO_ELECTORAL'].sum(),'%')

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
#PARTE II: INTRODUCIR GRUPOS

# %%
df3=df1.copy()

# %%
#agrupaciones para votos registrados
vot_grupos=['VDERECHA',
'VCENTRO',
'VIZQUIERDA',
'VNACIONALISTAS',
'VOTROS']

# %%
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


# %%
#grupos para votos > barrera electoral
grupos=['DERECHA',
'CENTRO',
'IZQUIERDA',
'NACIONALISTAS',
'OTROS']

# %%
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

# %%
#grupos para diputados
dgrupos=['DDERECHA',
'DCENTRO',
'DIZQUIERDA',
'DNACIONALISTAS',
'DOTROS']

# %%
#asignar a cada grupo sus partidos para escaños
list_dgroups = {key: None for key in dgrupos}
for x in dgrupos:#nombres de los grupos (CENTRO, DERECHA,...)
    C=[]
    
    for i in df2.loc[2][:]:#nombres de los partidos (1,2,...NPARTIDOS)
        if df2.loc[1][i] ==x[1:]:
            C.append(str(i)+'Diputados')
    #print(x,C)
    list_dgroups[x]=C

# %%
for j in range (N_PROV):
    for x in l:
        columna='%'+x 
        if df3.loc[j,columna]<barrera:
            df3.loc[j,x]=0
        else:
            df3.loc[j,x]=df3.loc[j][x+"Votos"]
            
       
    

# %%
for j in range (N_PROV):#provincias
    for x in vot_grupos:#grupos de partidos
        df3.loc[j,x]=df3.loc[j][list_vgroups[x]].sum()

# %%
#votos por grupos por provincias
for j in range (N_PROV):#provincias
    S=0
    for x in dgrupos:#grupos de partidos
        df3.loc[j,x]=df3.loc[j][list_dgroups[x]].sum()

# %%
#votos por grupos por provincias
for j in range (N_PROV):#provincias
    S=0
    for x in grupos:#grupos de partidos
        df3.loc[j,x]=df3.loc[j][list_groups[x]].sum()

# %%
#votos por grupos por provincias
for j in range (N_PROV):#provincias
    print('\n','PROVINCIA',df3.loc[j]['PROVINCIA'].strip(),f'{j:,.0f}','\n')
    S=0
    for x in vot_grupos:#grupos de partidos
        print(x, f'{df3.loc[j][list_vgroups[x]].sum():,.0f}')
        S=S+df3.loc[j][list_vgroups[x]].sum()
    print('--TOTAL VOTOS ELECCIONES REALES',f'{S:,.0f}')

# %%
#diputados por grupos por provincias
for j in range (N_PROV):#provincias
    print('\n','PROVINCIA',df3.loc[j]['PROVINCIA'].strip(),f'{j:,.0f}','\n')
    S=0
    for x in dgrupos:#grupos de partidos
        print(x, f'{df3.loc[j][list_dgroups[x]].sum():,.0f}')
        S=S+df3.loc[j][list_dgroups[x]].sum()
    print('--TOTAL DIPUTADOS ELECCIONES REALES',f'{S:,.0f}')

# %%
results=df3.copy()

# %%
#PARTE III: ARCHIVO DE SALIDA EXCEL

# %%
percent=list(results.loc[0][:].keys()[pos(df3,"%1"):pos(df3,'VDERECHA')])


# %%
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

# %%
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

# %%
D=[]
for y in l:
    
    if (df3.loc[:][y].sum()!=0):
        
        D.append(int(y))
        
D=list(set(D))
D.sort()#partidos que superan la barrera

# %%
for x in range(0,len(D)):
    D[x]=str(D[x])


# %%
for j in range (N_PROV):#provincias
    Su=0
    for x in D:#partidos que superan la barrera
        if df3.loc[j][x].any()!=0:
            Su=Su+1
    df3.loc[j,'PARTIDOS>']=Su

# %%
to_remove=list(set(l)-set(D))

# %%
U0=[i for i in range(0,pos(df3,'1Votos'))]
UU0=list(df3.loc[0][U0].keys())
U1=[i for i in range(pos(df3,'DERECHA'),pos(df3,'OTROS')+1)]
UU1=list(df3.loc[0][U1].keys())
U2=[i for i in range(pos(df3,'1Diputados'),pos(df3,'%1'))]
UU2=list(df3.loc[0][U2].keys())
U3=[i for i in range(pos(df3,'DDERECHA'),pos(df3,'DOTROS')+1)]
UU3=list(df3.loc[0][U3].keys())
UU=UU0+UU1+UU2+UU3

# %%
masde=pd.concat([df3[UU0],df3[l],df3[UU1],df3[UU2],df3[UU3]],axis=1)

# %%
U=[i for i in range(pos(df3,'%1'),pos(df3,'1'))]
borrar=list(df3.loc[0][U].keys())

# %%
df3=df3.drop(columns=borrar)

# %%
U0=[i for i in range(0,pos(df3,'DIPUTADOS')+1)]
U1=[i for i in range(pos(df3,'1Votos'),pos(df3,'1Diputados'))]
U2=[i for i in range(pos(df3,'VDERECHA'),pos(df3,'DDERECHA'))]
U3=[i for i in range(pos(df3,'1Diputados'),pos(df3,'1'))]
U4=[i for i in range(pos(df3,'DDERECHA'),pos(df3,'DERECHA'))]
UU0=list(df3.loc[0][U0].keys())
UU1=list(df3.loc[0][U1].keys())
UU2=list(df3.loc[0][U2].keys())
UU3=list(df3.loc[0][U3].keys())
UU4=list(df3.loc[0][U4].keys())

# %%
resultados=pd.concat([df3[UU0],df3[UU1],df3[UU2],df3[UU3],df3[UU4]], axis=1)

# %%
U=[]
U=UU1+UU3
A=[]
M=list(resultados.loc[0][U].keys())
for y in M:
    if (resultados[y] == 0).all():
        A.append(y)

# %%
B=[]
M1=[i for i in range(pos(df3,'1Votos'),pos(df3,'VDERECHA'))]
M=list(df3.loc[0][M1].keys())
for y in M:
    if (df3[y] == 0).all():
        B.append(y)

# %%
F=input("¿DESEA EXPORTAR LOS RESULTADOS? (Y/N)\n")
if F=='Y' or F=='Y'.lower():
    Res=input("¿Qué nombre desea concatenar con 'Resultados'\n")
    Name='Resultados'+str(Res)
    G=input("¿DESEA ELIMINAR VALORES NULOS DE VOTOS?\n\
    (no es conveniente si se desea comparación con resultados iniciales\n(Y/N)\n") 
    if G=='Y' or G=='Y'.lower():
        common=set(A).intersection(set(resultados.loc[0].keys()))
        results=resultados.drop(columns=common,axis=1)
        writer = pd.ExcelWriter(Name+'.xlsx')
        results.to_excel(writer,sheet_name='DatosMint')
        comi=set(B).intersection(set(masde.loc[0].keys()))
        masde1=masde.drop(columns=comi,axis=1)
        masde1.to_excel(writer,sheet_name='Datos>barrera')
        writer.close()
    if G=='N' or G=='N'.lower():
        writer = pd.ExcelWriter(Name+'.xlsx')
        resultados.to_excel(writer,sheet_name='DatosMint1')
        masde.to_excel(writer,sheet_name='Datos>barrera')
        writer.close()


# %%
#PARTE IV: GUARDAR FICHEROS DE INTERÉS

# %%
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



# %%
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


# %%
#exporto ficheros de interés
df0.to_pickle(dire+"\\df0.pkl")
df1.to_pickle(dire+"\\df1.pkl")
df2.to_pickle(dire+"\\df2.pkl")
dfprov.to_pickle(dire+"\\dfprov.pkl")
resultados.to_pickle(dire+"\\minint.pkl")
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
z=open(dire+"\\l.pkl","wb")
pickle.dump(l,z)
z.close()

# %%
print("---------------------------------------------------",
     "---------------------------------------------------",
     "TERMINADO:",guion+".py")
