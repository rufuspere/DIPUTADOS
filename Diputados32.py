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
#DIPUTADOS32: PARTE II: INTRODUCIR GRUPOS

# %%
guion="Diputados32"

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
#votos por grupos por provincias
df1= df1.reindex(columns = df1.columns.tolist() 
                                  + dgrupos)


# %%
#extraigo los diputados a cada candidatura y provincia
diputados=df1.copy()
diputados=diputados[diputados.columns.intersection(Z)]    

# %%
for j in range (N_PROV):#provincias
    for x in dgrupos:#grupos de partidos
        df1.loc[j,x]=df1.loc[j][list_dgroups[x]].sum()

# %%
#votos por grupos por provincias
for j in range (N_PROV):#provincias
    print('\n','PROVINCIA',df1.loc[j]['PROVINCIA'].strip(),f'{j:,.0f}','\n')
    S=0
    for x in vot_grupos:#grupos de partidos
        print(x, f'{df1.loc[j][list_vgroups[x]].sum():,.0f}')
        S=S+df1.loc[j][list_vgroups[x]].sum()
    print('--TOTAL VOTOS ',f'{S:,.0f}')

# %%
#diputados por grupos por provincias
for j in range (N_PROV):#provincias
    print('\n','PROVINCIA',df1.loc[j]['PROVINCIA'].strip(),f'{j:,.0f}','\n')
    S=0
    for x in dgrupos:#grupos de partidos
        print(x, f'{df1.loc[j][list_dgroups[x]].sum():,.0f}')
        S=S+df1.loc[j][list_dgroups[x]].sum()
    print('--TOTAL DIPUTADOS ',f'{S:,.0f}')

# %%
df1=df1.rename(columns=Var)

# %%
U0=[i for i in range(0,pos(df1,'1'))]
U1=[i for i in range(pos(df1,'1'),pos(df1,'1Diputados'))]
U3=[i for i in range(pos(df1,'1Diputados'),pos(df1,'DDERECHA'))]
U2=[i for i in range(pos(df1,'DDERECHA'),pos(df1,'DOTROS')+1)]


# %%
VV=[]
UU0=list(df1.loc[0][U0].keys())
UU1=list(df1.loc[0][U1].keys())
UU2=list(df1.loc[0][U2].keys())
UU3=list(df1.loc[0][U3].keys())
UU=UU0+UU1+UU2+UU3



# %%

df1=pd.concat([df1[UU0],df1[UU1],df1[UU2],df1[UU3]], axis=1)

# %%
#votos por grupos por provincias
for j in range (N_PROV):#provincias
    S=0
    for x in vot_grupos:#grupos de partidos
        try:
            df1.loc[j,x]=df1.loc[j][list_vgroups[x]].sum()
        except:
            continue

# %%
print("---------------------------------------------------",
     "---------------------------------------------------",
     "TERMINADO:",guion+".py")
