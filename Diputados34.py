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
#DIPUTADOS34: PARTE IV: TABLAS d'HONDT
# -

guion="Diputados34"

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

print("---------------------------------------------------","TERMINADO:",guion+".py")
