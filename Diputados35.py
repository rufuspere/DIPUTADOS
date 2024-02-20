# ---
# jupyter:
#   jupytext:
#     formats: py:hydrogen
#     text_representation:
#       extension: .py
#       format_name: hydrogen
#       format_version: '1.3'
#       jupytext_version: 1.16.0
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %%
#DIPUTADOS35:PARTE V: COMPROBAR SI HAY EMPATES

# %%
guion="Diputados35"

# %%
#vemos la lista de los valores repetidos en cada provincia:  repitentes[I] extaídos de lista_votos[I]
repitentes=[[] for i in range(N_PROV) ]
S=0
PR=[]
for i in range(N_PROV):
    D=([x for x in lista_votos[i] if lista_votos[i].count(x) >= 2])
    D.sort(reverse=True)
    
    for j in range(len(D)):
        if D[j]!=0:
            repitentes[i].append(D[j])
            a=repitentes[i][j]
            S=S+1
            PR.append(i)
    if len(repitentes[i])>0:       
        print('provincia: ', df3.loc[i]['PROVINCIA'],i,'\n',repitentes[i])

if S==0:
    print('NO HAY CANDIDATURAS EMPATADAS')
    Empates=0
    
else:
    print('Hay candidaturas empatadas en provincias',set(PR))
    Empates=1

# %%
print("---------------------------------------------------","TERMINADO:",guion+".py")
