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
#DIPUTADOS32: PARTE II: INTRODUCIR GRUPOS

# %%
guion="Diputados32"

# %%
df11=df1.copy()

# %%
#agrupaciones para votos
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
    #print(x,C)
    list_vgroups[x]=C

# %%
list_vgroups

# %%
#grupos para votos >barrera
grupos=['DERECHA',
'CENTRO',
'IZQUIERDA',
'NACIONALISTAS',
'OTROS']

# %%
list_groups = {key: None for key in grupos}
for x in grupos:#nombres de los grupos (CENTRO, DERECHA,...)
    C=[]
    
    for i in df2.loc[2][:]:#nombres de los partidos (1,2,...NPARTIDOS)
        if df2.loc[1][i] ==re.sub('V', '', x):
            C.append(str(i))
    #print(x,C)
    list_groups[x]=C

# %%
list_groups

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
list_dgroups


# %%
#votos por grupos por provincias
df11= df11.reindex(columns = df11.columns.tolist() 
                                  + vot_grupos)


# %%
#diputados por grupos por provincias
df11= df11.reindex(columns = df11.columns.tolist() 
                                  + dgrupos)

# %%

# %%
for j in range(N_PROV):
    for x in dgrupos:
        df11.loc[j,list_dgroups[x]]=0

# %%
#extraigo los diputados a cada candidatura y provincia
diputados=df11.copy()
diputados=diputados[diputados.columns.intersection(Z)]    

# %%
diputados

# %%
#votos por grupos por provincias
for j in range (N_PROV):#provincias
    print('\n','PROVINCIA',df11.loc[j]['PROVINCIA'].strip(),f'{j:,.0f}','\n')
    S=0
    for x in vot_grupos:#grupos de partidos
        print(x, f'{df11.loc[j][list_vgroups[x]].sum():,.0f}')
        S=S+df11.loc[j][list_vgroups[x]].sum()
    print('--TOTAL VOTOS ',f'{S:,.0f}')
#los diputados habrán de asignarse por el método d'Hondt

# %%
#votos>barrera por grupos por provincias
df11= df11.reindex(columns = df11.columns.tolist() 
                                  + grupos)


# %%
df=df1.rename(columns=Var)

# %%
estructura(df11)

# %%
U0=[i for i in range(0,pos(df11,'1Votos'))]
U1=[i for i in range(pos(df11,'1Votos'),pos(df11,'1Diputados'))]
U2=[i for i in range(pos(df11,'VDERECHA'),pos(df11,'VOTROS')+1)]
U3=[i for i in range(pos(df,'1'),pos(df,'1Diputados'))]
U4=[i for i in range(pos(df11,'DERECHA'),pos(df11,'OTROS')+1)]
U5=[i for i in range(pos(df11,'1Diputados'),pos(df11,'%1'))]
U6=[i for i in range(pos(df11,'DDERECHA'),pos(df11,'DOTROS')+1)]

# %%
VV=[]
UU0=list(df11.loc[0][U0].keys())
UU1=list(df11.loc[0][U1].keys())
UU2=list(df11.loc[0][U2].keys())
UU3=list(df.loc[0][U3].keys())
UU4=list(df11.loc[0][U4].keys())
UU5=list(df11.loc[0][U5].keys())
UU6=list(df11.loc[0][U6].keys())
UU=UU0+UU1+UU2+UU3+UU4+UU5+UU6

# %%

df12=pd.concat([df11[UU0],df11[UU1],df11[UU2],df[UU3],df11[UU4],df11[UU5],df11[UU6]], axis=1)
df12=df12.fillna(0)

# %%
print("---------------------------------------------------","TERMINADO:",guion+".py")
