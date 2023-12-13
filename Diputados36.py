# ---
# jupyter:
#   jupytext:
#     formats: py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.15.2
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %%
#DIPUTADOS36: PARTE VI: SI HAY EMPATES

# %%
repeated=[[] for i in range(N_PROV)]
for i in range(N_PROV):
    my_set = {s for s in repitentes[i]}
    repeated[i]=list(my_set)
    repeated[i].sort(reverse=True)
#valores repetidos en cada provincia en la tabla d'Hondt (un solo valor)

# %%
#es la función que localiza valores en DataFrame
i,j=np.where(np.isclose(np.array(dHondt[0],dtype=float),91964))
indices=list(zip(i,j))#tupla que da el número de fila y el de columna (f,c) de la tabla d'Hondt
print(indices)
print(dHondt[0][dHondt[0]>0].dropna(axis=0, how='all'))

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
#devuelve el rango de las posiciones de lista_votos en que se repite el valor que ha de ser asignado
#a un partido aleatoriamente ya que el coeficiente de d'Hondt es el mismo para varios partidos.
locations=[[] for i in range(N_PROV)]
for i in range(N_PROV):
    for j in range (len(repeat_loc[i])):
        a=min([x for x in repeat_loc[i][j][1]])
        b=max([x for x in repeat_loc[i][j][1]])
        if(b>=df3.loc[i]['DIPUTADOS'] and a<=df3.loc[i]['DIPUTADOS']):
            #print(i,df3.loc[i]['PROVINCIA'].strip(),j,b>=df3.loc[i]['DIPUTADOS'] and a<=df3.loc[i]['DIPUTADOS'])
            print(i,df3.loc[i]['PROVINCIA'].strip(),'Escaños a sortear',j,'entre las candidaturas',repeat_loc[i][j][1])
            print('Mínimo',min([x for x in repeat_loc[i][j][1]]),'Máximo', max([x for x in repeat_loc[i][j][1]]))
            
            locations[i].append(a)
            locations[i].append(b)


# %%
if not any(locations):
    print("locations está vacío")
else:
    print(locations)
#donde la lista está vacía, no hay coeficientes d'Hondt duplicados.
#donde no está vacía muestra el rango [MIN,MAX] en el que se encuentran los coeficientes empatados y
#el intervalo siempre ha de cubrir el valor del número de diputados asignados a la provincia.

# %%
for i in range(N_PROV):
    if list(locations[i]):
        print(df3.loc[i]['PROVINCIA'].strip(),i,locations[i],'N_DIPUTADOS',int(df3.loc[i]['DIPUTADOS']))
#nos da el índice mínimo  y el máximo que comprende el número de DIPUTADOS


# %%
#el número de veces que se ha de elegir al azar en cada provincia
n_rep=[]
pr_alea=[]
for i in range(N_PROV):
    try:
        n=(+int(df3.loc[i]['DIPUTADOS'])-min(locations[i]))
        print('PROVINCIA ',df3.loc[i]['PROVINCIA'].strip(),i,' SELECCIONES ALEATORIAS ',n)
        n_rep.append(n)
        pr_alea.append(i)
    except:
        n_rep.append(0)

s=[(i,df3.loc[i]['PROVINCIA'].strip()) for i in range(N_PROV)]
n_rep1=list(zip(s,n_rep))       
#n_rep1 asocia para cada provincia el número de veces a elegir al azar

# %%
#comprobación del muestreo
M=[[] for o in range(N_PROV)]
for o in range(N_PROV):
    try:
        m=[i for i in range(min(locations[o]),max(locations[o]))]
        M[o].append(m)
        print('POSICIONES DE DUPLICADOS: ','PROVINCIA',o,M[o])
    except:
        continue
N=[[] for o in range(N_PROV)]
for i in range(100):
    
    for k in pr_alea:
        for j in range(len(M[k])):    
            r=random.sample(M[k][j], int(df3.loc[k]['DIPUTADOS'])-min(locations[k]))
            r.sort()
            
            #print ('pasada',i+1,'provincia',k,'muestra',r)
            N[k].append(r)
        
alea49 = pd.DataFrame(N[49], columns = ['alea'])
alea30=[elem for sublist in N[30] for elem in sublist]
alea30 = pd.DataFrame(alea30, columns = ['alea'])

# %%
alea30

# %%
counts30 = alea30['alea'].value_counts().to_dict()
counts49 = alea49['alea'].value_counts().to_dict()
counts30 = dict(sorted(counts30.items()))
counts49 = dict(sorted(counts49.items()))

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
#es el método para localizar en d'Hondt los valores de los coeficientes de la tabla
M=np.array(dHondt[0],dtype=float)
i,j=np.where(np.isclose(M,39036))

# %%
i,j
#devuelve una tupla

# %%
lista_votos

# %%
#provincias sin empates
dipus=[[] for k in range(N_PROV)]
num_part=[]
elements_count=[[] for k in range(N_PROV)]
for k in range(N_PROV):
    dipus[k]=[]
    if n_rep[k]==0:
        for x in lista_votos[k][0:int(df3.loc[k]['DIPUTADOS'])]:
            M=np.array(dHondt[k],dtype=float)
            i,j=np.where(np.isclose(M,x))
            dipus[k].append(i[0]+1)
        a=CountFrequency(dipus[k])
        elements_count[k].append(a)
    num_part.append(elements_count[k])    
# el diccionario elements_count[k] nos da el par (PARTIDO, ESCAÑOS) para cada PROVINCIA k
    #print(k,elements_count[k])

# %%
len(dipus[0])

# %%
elements_count

# %%
#lista de candidaturas que recibirán diputados ordenadas según la regla d'Hondt
S=0
for i in range (N_PROV):
    S=S+1
    print(df3.loc[i]['PROVINCIA'],dipus[i])
print(S)

# %%
df3.loc[0,'DIPUTADOS1']

# %%
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
 for x in Dl:
    print(x,elements_count[0][0][int(x[9:])])

# %%
#Asigno diputados a provincias donde no hay empates
df4=df3.copy()
for k in range(N_PROV):
    #print('PROV ',k)
    if n_rep[k]==0:#si no hay duplicados en la provincia n_rep[k]==0
        for x in DL:
           
            df4.loc[k,x]=elements_count[k][0][int(x[9:])]
                #print('PARTIDO',int(x),'DIPUS ', elements_count[k][0][int(x)])
           


# %%
df4['DIPUTADOS1']

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
            v=list(zip(i+1,j))
            print(k,x,v,i[0])
            dipus1[k].append(v)
            flat_list = [item for sublist in dipus1[k][:] for item in sublist]
            dipus2[k]= [item for item in flat_list[:min(locations[k])]]
            dipus3[k]=[item for item in flat_list[min(locations[k]):]]


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


# %%
elements_count1=[[] for k in range(N_PROV)]
for k in pr_alea:
    a=CountFrequency(dipus4[k])
    elements_count1[k].append(a)
    print(k,elements_count1[k][0])
# el diccionario elements1_count[k] nos da el par (PARTIDO, ESCAÑOS) para cada PROVINCIA k

# %%
#Asigno diputados a provincias donde hay empates
df5=df4.copy()
for k in pr_alea:
    for x in l:
        columna='DIPUTADOS'+x
        try:
            df5.loc[k,columna]=(elements_count1[k][0][int(x)])
            #print('PROV ',k,'PARTIDO',int(x),'DIPUS ', elements_count[k][0][int(x)])
        except:
            continue
df5 = df5.fillna(0)

# %%
