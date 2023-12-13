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
#DIPUTADOS34: PARTE IV: TABLAS d'HONDT
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
        lista_votos[i].sort(reverse=True)
       
      
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


