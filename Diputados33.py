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


# %%
estructura(df3)

# %%
df3.loc[0]['%1']

# %%
l_barr=[[] for j in range(N_PROV)]
for j in range (N_PROV):
    for x in l:
        if df3.loc[j]['%'+x] < barrera:
            df3.loc[j,x]=0
            l_barr[j].append(x)

# %%
for j in range (N_PROV):#provincias
    Su=0
    if df3.loc[j]['%'+x] >= barrera:#partidos que superan la barrera
        Su=Su+1
    df3.loc[j,'PARTIDOS>']=Su

# %%
#anulo valores de votos <barrera
for j in range (N_PROV):
    for x in l_barr[j]:
        if df3.loc[j]['%'+x] < barrera:
            df3.loc[j,x]=0
            


# %%
df3.insert(loc = 5,
          column = 'VOTOS_REPARTIR',
          value =df3[l].sum(axis=1))

# %%
df3.loc[7]['VOTOS_REPARTIR']

# %%
print("---------------------------------------------------",
     "---------------------------------------------------",
     "TERMINADO:",guion+".py")
