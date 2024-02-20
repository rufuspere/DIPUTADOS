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
#Diputados36: PARTE VI: SI HAY EMPATES

# %%
guion="Diputados36"

# %%
repeated=[[] for i in range(N_PROV)]
for i in range(N_PROV):
    my_set = {s for s in repitentes[i]}
    repeated[i]=list(my_set)
    repeated[i].sort(reverse=True)
#valores repetidos en cada provincia en la tabla d'Hondt (un solo valor)

# %%
#defino función que identifica y recopila valores repetidos
from collections import defaultdict
def list_duplicates(seq):
    tally = defaultdict(list)
    for i,item in enumerate(seq):
        tally[item].append(i)#tally es diccionario que asigna a cada valor los índices en que aparece
    return ((key,locs) for key,locs in tally.items() if len(locs)>1)#solo se queda con los índices de valores repetidos
#devuelve un diccionario en el que la key es el elemento de seq y el value es una lista de los índices
#en que aparece


# %%
repeat_loc=[[] for i in range(N_PROV)]
for i in range(N_PROV):
    for dup in list_duplicates(lista_votos[i]):
        repeat_loc[i].append(dup)
        repeat_loc[i] = sorted(list_duplicates(lista_votos[i]),reverse=True)
        
#tuplas que asocian key=VALOR repetido con value lista de los ÍNDICES de lista_votos[I]
#en la mayoría de casos es 0 el único valor que se repite

# %%
for i in range(N_PROV):
    for j in range (len(repeat_loc[i])):
        a=min([x for x in repeat_loc[i][j][1]])
        b=max([x for x in repeat_loc[i][j][1]])
        c=df3.loc[i]['DIPUTADOS']-1
        
        if(b>c and a<=c):
           
            print('Se precisa sorteo en provincia Nº', i,'(',df3.loc[i]['PROVINCIA'].strip(),')')
            print('Mínimo',a,'; Índice',c,'; Máximo',b)
         #   print(i,df3.loc[i]['PROVINCIA'].strip(),j,b>=df3.loc[i]['DIPUTADOS'] and a<=df3.loc[i]['DIPUTADOS'])

# %%
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


# %%
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

# %%
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
#n_rep1 asocia para cada provincia el número de veces a elegir al azar

# %%
pr_alea

# %%
#comprobación del muestreo

# %%
import random
M=[[] for o in range(N_PROV)]
for o in range(N_PROV):
    try:
        m=[i for i in range(min(locations[o]),max(locations[o])+1)]
        M[o].append(m)
        print('POSICIONES A SORTEAR EN PROVINCIA:',o,';Número:',len(M[o]),';',M[o])
    except:
        continue


# %%
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


# %%
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


# %%
#función que cuenta el número de diputados que cada partido obtiene en función del orden en tabla dHondt
def CountFrequency(my_list):
    count = {}
    for i in my_list:
        count[i] = count.get(i, 0) + 1
    return count


# %%
import numpy as np
#es la función que localiza valores en DataFrame
M=np.array(dHondt[0],dtype=float)
i,j=np.where(np.isclose(M, 39357.3333333333,rtol=0,atol=0.01))
indices=list(zip(i,j))#tupla que da el número de fila y el de columna (f,c) de la tabla d'Hondt
print('Indices',indices)

# %%
i,j
#devuelve una tupla

# %%
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

# %%
num_part

# %%
#lista de candidaturas que recibirán diputados sin muestreo 
#ordenadas según la regla d'Hondt
S=0
for i in range (N_PROV):
    S=S+1
    print(df3.loc[i]['PROVINCIA'],dipus[i],len(dipus[i]))
print(S)

# %%
l=[]
for item in df2:
    l.append(str(item))
Dl=[]
for x in l:
    columna='DIPUTADOS'+x
    Dl.append(columna)

# %%
Dl

# %%
for j in range(N_PROV):
    for x in Dl:
        df3.loc[j,x]=0

# %%
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


# %%
#Asigno diputados a provincias donde no hay empates
df4=df3.copy()
P=[[] for k in range(N_PROV)]
for k in range(N_PROV):
    for j in list(pretty_dict[k]):
        P[k].append('DIPUTADOS'+str(j))
    if n_rep[k]==0:#si no hay duplicados en la provincia n_rep[k]==0
        
        for x in P[k]:
            df4.loc[k,x]=pretty_dict[k][int(x[9:])]

# %%
df4.loc[:]['DIPUTADOS3']

# %%
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


# %%
emp

# %%
nemp

# %%
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
            i,j=np.where(np.isclose(M,x))
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


# %%
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

# %%
df4.loc[:]['DIPUTADOS1']

# %%
elements_count1=[[] for k in range(N_PROV)]
for k in pr_alea:
    a=CountFrequency(dipus4[k])
    elements_count1[k].append(a)
    print(k,elements_count1[k][0])
# el diccionario elements1_count[k] nos da el par (PARTIDO, ESCAÑOS) para cada PROVINCIA k

# %%
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


# %%
print("---------------------------------------------------","TERMINADO:",guion+".py")

# %%
