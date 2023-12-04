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
import os, pandas as pd
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
dfprov=pd.read_pickle(dire+"\\dfprov.pkl")



# %%
dfprov.head()


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
def Resumen_Prov(dataFrame):#df0 es el inicial   
    for x in range (N_PROV):
        print('Provincia:',x,',',dataFrame.loc[x]['PROVINCIA'].strip(),';','Votos:', f"{df0.loc[x][New_l].sum():,.0f}",',','Diputados:',f"{df0.loc[x][New_d].sum():,.0f}")


# %%
#lista de votos por grupo político
def Votos_y_Escaños_Grupos(dataFrame):
    for x in range (N_PROV):
        print('Provincia:',x,',',dataFrame.loc[x]['PROVINCIA'].strip())
        print('-Grupo:')
        for y in vot_grupos:
            if dataFrame.loc[x][list_vgroups[y]].sum()!=0:
                print(' ',y[1:],'Votos:', f"{dataFrame.loc[x][list_vgroups[y]].sum():,.0f}"
                      ,'. Diputados:', f"{dataFrame.loc[0][list_dgroups[y[1:]]].sum():,.0f}")


# %%
#lista de votos y escaños por partido político
def Votos_y_Escaños(dataFrame):
    for x in range (N_PROV):
        print('Provincia:',x,',',dataFrame.loc[x]['PROVINCIA'].strip())

        for y in (df2.loc[2][:]):
            if df0.loc[x][str(y)+'Votos'].sum()!=0:
                
                print(' -Partido:',df2.loc[0][y],'(Grupo:',party_grupo[str(y)+'Votos'],')','; Votos:',f"{dataFrame.loc[x][str(y)+'Votos'].sum():,.0f}",'; Diputados:',f"{dataFrame.loc[x][str(y)+'Diputados'].sum():,.0f}")


# %%
#lista de votos y escaños por CA
def Votos_y_Diputados(Com):
    for x in CA[Com]:
        print('Provincia:',x,df0.loc[x]['PROVINCIA'])
        for z in range(N_PARTIDOS):
            if df0.loc[x][str(z+1)+'Votos'].sum()!=0 and df0.loc[x][str(z+1)+'Diputados'].sum()!=0:

                print(' -Partido:',df2.loc[0][z+1],'(',party_grupo[str(z+1)+'Votos'],')','; Votos:',f"{df0.loc[x][str(z+1)+'Votos'].sum():,.0f}",'; Diputados:',f"{df0.loc[x][str(z+1)+'Diputados'].sum():,.0f}")


# %%
#lista de votos y escaños por provincia
def VotEscaño_Prov(dataFrame,x):
    
    print('Provincia:',x,',',dataFrame.loc[x]['PROVINCIA'].strip())

    for y in (df2.loc[2][:]):
        if dataFrame.loc[x][str(y)+'Votos'].sum()!=0:
                
            print(' -Partido:',df2.loc[0][y],'(Grupo:',party_grupo[str(y)+'Votos'],')','; Votos:',f"{dataFrame.loc[x][str(y)+'Votos'].sum():,.0f}",'; Diputados:',f"{dataFrame.loc[x][str(y)+'Diputados'].sum():,.0f}")


# %%
#listar comunidades con sus provincias
def Com_Aut():
    print(list(CA.keys()))
    print (CA)


# %%
#permiten recuperar datos que pueden ser necesarrios en 
#cualquier celda del cuaderno de notas
def Lista_Funciones():
    print('identificar partido:\n partido(codigo)')
    print('listar nombre, índice, código y comunidad de una provincia:\n provincia(codigo)')
    print('lista de votos y escaños por provincia:\n Resumen_Prov(dataFrame)')
    print('lista de votos por grupo político:\n Votos_y_Escaños_Grupos(dataFrame)')
    print('lista de votos y escaños por CA:\n Votos_y_Diputados(Com)')
    print('lista de votos y escaños por provincia:\n VotEscaño_Prov(dataFrame,x)')
    print('lista comunidades con sus provincias:\n Com_Aut()')

# %%
