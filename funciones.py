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
import os, pandas as pd,re
dire=os.getcwd()
print('Directorio de trabajo: ',os.getcwd())

# %%
import pickle
h = open(dire+'\\variables.pkl','rb')
variables = pickle.load(h)
h.close()
N_PROV=variables['N_PROV']
N_PARTIDOS=variables['N_PARTIDOS']


# %%
d=open(dire+"\\new_l.pkl","rb")
new_l=pickle.load(d)
d.close()
e=open(dire+"\\new_d.pkl","rb")
new_d=pickle.load(e)
e.close()

# %%

n=open(dire+"\\party_grupo.pkl","rb")
party_grupo=pickle.load(n)
n.close()
s = open(dire+"\\CA.pkl","rb")
CA = pickle.load(s)
s.close()
u=open(dire+"\\dfprov.pkl","rb")
dfprov=pickle.load(u)
u.close()
t = open(dire+"\\vot_grupos.pkl","rb")
vot_grupos= pickle.load(t)
t.close()
v=open(dire+"\\list_vgroups.pkl","rb")
list_vgroups=pickle.load(v)
v.close()
w=open(dire+"\\list_dgroups.pkl","rb")
list_dgroups=pickle.load(w)
w.close()
df0=pd.read_pickle(dire+"\\df0.pkl")
df2=pd.read_pickle(dire+"\\df2.pkl")
dfd=pd.read_pickle(dire+"\\dfd.pkl")
dfprov=pd.read_pickle(dire+"\\dfprov.pkl")



# %%
#identificar partido
def partido(codigo):
    n=str(codigo)+'Votos'
    a=df2.loc[2][(codigo)]
    b=df2.loc[0][codigo]
    print ('Partido Nº:',a,'\n','- Siglas:',b,'\n','- Grupo:',party_grupo[n],)


# %%
def provincia(x):
    if x in dfprov['NPROVINCIA']:
        print ('A) Orden de provincia:',x,'\n -Código :'
           ,dfprov.loc[x]['NPROVINCIA'],'\n -Nombre:'
           ,dfprov.loc[x]['PROVINCIA'])


# %%
#lista de votos y escaños por provincia
def Resumen_Prov():#df0 es el inicial   
    for x in range (N_PROV):
        print('Provincia:',x,',',df0.loc[x]['PROVINCIA'].strip(),';','Votos:', f"{df0.loc[x][new_l].sum():,.0f}",',','Diputados:',f"{df0.loc[x][new_d].sum():,.0f}")


# %%
#lista de votos por grupo político
def Votos_y_Escaños_Grupos():
    for x in range (N_PROV):
        print('Provincia:',x,',',df0.loc[x]['PROVINCIA'].strip())


        for y in (df2.loc[2][:]):
            if df0.loc[x][str(y)+'Votos'].sum()!=0:

                print(' -Partido:',df2.loc[0][y],'(Grupo:',party_grupo[str(y)+'Votos'],')','; Votos:',f"{df0.loc[x][str(y)+'Votos'].sum():,.0f}",'; Diputados:',f"{df0.loc[x][str(y)+'Diputados'].sum():,.0f}")


# %%
#lista de votos y escaños por partido político
def Votos_y_Escaños():
    for x in range (N_PROV):
        print('Provincia:',x,',',df0.loc[x]['PROVINCIA'].strip())

        for y in (df2.loc[2][:]):
            if df0.loc[x][str(y)+'Votos'].sum()!=0:
                
                print(' -Partido:',df2.loc[0][y],'(Grupo:',party_grupo[str(y)+'Votos'],')','; Votos:',f"{df0.loc[x][str(y)+'Votos'].sum():,.0f}",'; Diputados:',f"{df0.loc[x][str(y)+'Diputados'].sum():,.0f}")


# %%
#lista de votos y escaños por provincia
def VotEscaño_Prov(provincia):
    
    print('Provincia:',provincia,',',df0.loc[provincia]['PROVINCIA'].strip())

    for y in (df2.loc[2][:]):
        if df0.loc[provincia][str(y)+'Votos'].sum()!=0:
                
            print(' -Partido:',df2.loc[0][y],'(Grupo:',party_grupo[str(y)+'Votos'],')','; Votos:',f"{df0.loc[provincia][str(y)+'Votos'].sum():,.0f}",'; Diputados:',f"{df0.loc[provincia][str(y)+'Diputados'].sum():,.0f}")


# %%
#listar comunidades con sus provincias
def Com_Aut():
    print(list(CA.keys()))
    print (CA)


# %%
#lista de votos y escaños por CA
def Votos_y_Diputados(Com):
    if Com=="Baleares":
        Com="Illes Balears"
    if Com=="Castilla":
        region=input("La Mancha o León")
        if region=="La Mancha":
            Com="Castilla - La Mancha"
        if region=="León":
            Com="Castilla y León"
    for j in range(len(CA)):
        index = list(CA.keys())[j].find(Com)
        if index !=-1:
            Com=list(CA.keys())[j]
            print(Com)
    for x in CA[Com]:
        print('Provincia:',x,df0.loc[x]['PROVINCIA'])
        S=0
        for z in range(N_PARTIDOS):
            if df0.loc[x][str(z+1)+'Votos'].sum()!=0 and df0.loc[x][str(z+1)+'Diputados'].sum()!=0:
                S=S+df0.loc[x][str(z+1)+'Votos'].sum()
                print(' -Partido:',df2.loc[0][z+1],'(',party_grupo[str(z+1)+'Votos'],')','; Votos:',f"{df0.loc[x][str(z+1)+'Votos'].sum():,.0f}",'; Diputados:',f"{df0.loc[x][str(z+1)+'Diputados'].sum():,.0f}")
        print('--Diputados totales:',f"{df0.loc[x][new_d].sum():,.0f}")
        print(' Votos totales:',f"{df0.loc[x][new_l].sum():,.0f}",'. Votos usados para escaños:',f"{S:,.0f}")
        print(' Difrencia de votos:',f"{df0.loc[x][new_l].sum()-S:,.0f}")


# %%
#permiten recuperar datos que pueden ser necesarrios en 
#cualquier celda del cuaderno de notas
def Lista_Funciones():
    print('identificar partido:\n aux.partido(codigo)')
    print('listar nombre, índice, código y comunidad de una provincia:\n provincia(codigo)')
    print('lista de votos y escaños por provincia:\n Resumen_Prov()')
    print('lista de votos por grupo político:\n Votos_y_Escaños_Grupos()')
    print('lista comunidades con sus provincias:\n Com_Aut()')
    print('lista de votos y escaños por CA:\n Votos_y_Diputados(Com)')
    print('lista de votos y escaños por provincia:\n VotEscaño_Prov(provincia)')



# %%
