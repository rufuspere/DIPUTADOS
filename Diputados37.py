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
#DIPUTADOS37: PARTE VII: ASIGNACIÓN DE ESCAÑOS DEFINITIVA

# %%
guion="Diputados37"

# %%
#votos por grupo político
df6=df5.copy()
for k in range(N_PROV):
    for x in dgrupos:
        df6.loc[k,x]=df6.loc[k][list_dgroups[x]].sum()


# %%
df7=df6.copy()
import warnings
warnings.filterwarnings("ignore")
for k in range(N_PROV):
    for x in grupos:
        df7.loc[k,x]=df7.loc[k][list_groups[x]].sum()
df7 = df7.fillna(0)


# %%
for x in range (N_PROV):
    df7.loc[x,'PARTIDOS>']=df7.loc[x][l].astype(bool).sum()


# %%
df71=pd.concat([df7,df0[new_l]],axis=1)

# %%
df71= df71.reindex(columns = df71.columns.tolist() 
                                  + vot_grupos)

# %%
for j in range (N_PROV):#provincias
    for x in vot_grupos:#grupos de partidos
        df71.loc[j,x]=df71.loc[j][list_vgroups[x]].sum()

# %%
#grupos para diputados
dipugrupos=['DIPDERECHA',
'DIPCENTRO',
'DIPIZQUIERDA',
'DIPNACIONALISTAS',
'DIPOTROS']

# %%
#asignar a cada grupo sus partidos para escaños
list_dipugroups = {key: None for key in dipugrupos}
for x in dipugrupos:#nombres de los grupos (CENTRO, DERECHA,...)
    D=[]
    
    for i in df2.loc[2][:]:#nombres de los partidos (1,2,...NPARTIDOS)
        if df2.loc[1][i] ==re.sub('DIP', '', x):
            D.append('DIPUTADOS'+str(i))
    #print(x,C)
    list_dipugroups[x]=D

# %%
df71= df71.reindex(columns = df71.columns.tolist() 
                                  + dipugrupos)

# %%
for j in range (N_PROV):#provincias
    for x in dipugrupos:#grupos de partidos
        df71.loc[j,x]=df71.loc[j][list_dipugroups[x]].sum()

# %%
df71.loc[7]['DIPDERECHA']

# %%
DF71=df71.copy()

# %%
l

# %%
V0=[i for i in range(0,pos(DF71,'DIPUTADOS')+1)]
V1=[i for i in range(pos(DF71,'1Votos'),pos(DF71,'VDERECHA'))]
V2=[i for i in range(pos(DF71,'VDERECHA'),pos(DF71,'VOTROS')+1)]
V3=[i for i in range(pos(DF71,'1Diputados'),pos(DF71,'%1'))]
V4=[i for i in range(pos(DF71,'DDERECHA'),pos(DF71,'DOTROS')+1)]
V5=l
V6=[i for i in range(pos(DF71,'DERECHA'),pos(DF71,'OTROS')+1)]
V7=[i for i in range(pos(DF71,'DIPUTADOS1'),pos(DF71,'DERECHA'))]
V8=[i for i in range(pos(DF71,'DIPDERECHA'),pos(DF71,'DIPOTROS')+1)]


# %%
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

# %%
NV

# %%
DF72=DF71[NV]
A=[]
M=list(DF72.loc[0][NV].keys())
for y in M:
    if (DF72[y].all() == 0):
        A.append(y)

# %%
DF72.loc[7]['DIPDERECHA']

# %%
for i in range(len(df3)):
    print('-PROVINCIA',i,'(',df1.loc[i]['PROVINCIA'].strip(),')','\n --DIPUTADOS:')
    print('   DERECHA',DF72.loc[i]['DIPDERECHA'])
    print('   IZQUIERDA',DF72.loc[i]['DIPIZQUIERDA'])
    print('   CENTRO',DF72.loc[i]['DIPCENTRO'])
    print('   NACIONALISTAS',DF72.loc[i]['DIPNACIONALISTAS'])
    print('   OTROS',DF72.loc[i]['DIPOTROS'])

# %%
print("---------------------------------------------------",
     "---------------------------------------------------",
     "TERMINADO:",guion+".py")

# %%
