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
#DIPUTADOS33:PARTE III: ELIMINAR CANDIDATURAS <barrera

# %%
guion="Diputados33"

# %%
df3=df12.copy()


# %%
df1.loc[:]['%1']

# %%
l_barr=[[] for j in range(N_PROV)]
for j in range (N_PROV):
    for x in l:
        if df1.loc[j]['%'+x] < barrera:
            df3.loc[j,x]=0
            l_barr[j].append(x)
        else:
            df3.loc[j,x]=df1.loc[j][x+'Votos']

# %%
for j in range (N_PROV):#provincias
    Su=0
    for x in l:
        if df1.loc[j]['%'+x] >= barrera:#partidos que superan la barrera
            Su=Su+1
        df3.loc[j,'PARTIDOS>']=Su


# %%
df3.loc[0,'PARTIDOS>']

# %%
df3.insert(loc = 5,
          column = 'VOTOS_REPARTIR',
          value =df3[l].sum(axis=1))

# %%

# %%
print("---------------------------------------------------","TERMINADO:",guion+".py")
    
