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
#DIPUTADOS37: PARTE VII: ASIGNACIÓN DE ESCAÑOS DEFINITIVA

# %%
guion="Diputados37"

# %%
df5=df4.copy()

# %%
#votos por grupo político
df6=df5.copy()
for k in range(N_PROV):
    for x in grupos:
        df6.loc[k,x]=df6.loc[k][list_groups[x]].sum()


# %%
#diputados por grupo político
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
df=df0.copy()
for j in range(N_PROV):
    for x in l:
        df.loc[j,x]=df0.loc[j][x+'Votos']

# %%
for j in range (N_PROV):#provincias
    for x in vot_grupos:#grupos de partidos
        df7.loc[j,x]=df7.loc[j][list_vgroups[x]].sum()

# %%
df7.loc[0]['VDERECHA']

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
df71=df7.copy()
df71= df71.reindex(columns = df71.columns.tolist() 
                                  + dipugrupos)
df71=df71.fillna(0)

# %%
estructura(df71)

# %%
for j in range (N_PROV):#provincias
    for x in dipugrupos:#grupos de partidos
        df71.loc[j,x]=df71.loc[j][list_dipugroups[x]].sum()

# %%
new_l

# %%
new_d

# %%
Diputats = ['DIPUTADOS'+str(x) for x in list(df2.keys())]


# %%
Diputats

# %%
#en caso de que los nuevos datos de diputados no se compadezcan con los de la  Xunta (por haber cambiado
# el número de diputados por circunscripción, p.e) igualamos los diputados iniciales con los calculados.
DF71=df71.copy()
for j in range (N_PROV):#provincias
    for x in Diputats:
        DF71.loc[j,re.sub('DIPUTADOS','',x)+'Diputados']=DF71.loc[j,x]
for j in range (N_PROV):#provincias
    for x in dipugrupos:
        DF71.loc[j,'D'+re.sub('DIP','',x)]=DF71.loc[j,x]

# %%
estructura(DF71)

# %%
V0=[i for i in range(0,pos(DF71,'DIPUTADOS')+1)]
V1=[i for i in range(pos(DF71,'1Votos'),pos(DF71,'VDERECHA'))]
V2=[i for i in range(pos(DF71,'VDERECHA'),pos(DF71,'1'))]
V3=[i for i in range(pos(DF71,'1Diputados'),pos(DF71,'DDERECHA'))]
V4=[i for i in range(pos(DF71,'DDERECHA'),pos(DF71,'DIPUTADOS1'))]
V5=[i for i in range(pos(DF71,'1'),pos(DF71,'DERECHA'))]
V6=[i for i in range(pos(DF71,'DERECHA'),pos(DF71,'1Diputados'))]
V7=[i for i in range(pos(DF71,'DIPUTADOS1'),pos(DF71,'DIPDERECHA'))]
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
DF71.loc[0][vot_grupos]

# %%
resultados=DF71[NV]

# %%
print("---------------------------------------------------","TERMINADO:",guion+".py")
