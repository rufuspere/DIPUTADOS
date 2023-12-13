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
#DIPUTADOS33:PARTE III: ELIMINAR CANDIDATURAS <barrera

# %%
guion="Diputados33"

# %%
df3=df1.copy()
for x in l:
    columna='%'+x
    df3[columna]=df3[x]/df3['VOTOS_VÁLIDOS']


# %%
df3.loc[0]['%1']

# %%
for j in range (N_PROV):#provincias
    Su=0
    for x in D:#partidos que superan la barrera
        if df3.loc[j][x].any()!=0:
            Su=Su+1
    df3.loc[j,'PARTIDOS>']=Su

# %%
ll=[]
for j in range (N_PROV):
    for x in l:
        if df3.loc[j]['%'+x] < barrera:
            df3.loc[j,x]=0
            ll.append(x)


# %%
ll=list(set(l)-set(ll))

# %%
df3.insert(loc = 5,
          column = 'VOTOS_REPARTIR',
          value =df3[ll].sum(axis=1))

# %%
print("---------------------------------------------------",
     "---------------------------------------------------",
     "TERMINADO:",guion+".py")
