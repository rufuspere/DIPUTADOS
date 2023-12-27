# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.15.2
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# +
#DIPUTADOS34: PARTE IV: TABLAS d'HONDT
# -

p=[[] for i in range(N_PROV)]
for i in range(N_PROV):
    c=df3.loc[j,ll]
    p[i]=[]
    
    for k in range (1,int(df3.loc[j]['DIPUTADOS'])+1):
        part_voto=c/k
        p[i].append(part_voto)
#p[I][J] es una lista de dimensión N_PROVINCIAS y donde cada elemento de la lista es 
#otra lista de longitud N_PARTIDOSxDIPUTADOS cuyo contenido es el número de votos de 
#cada partido dividido por 1,2,...DIPUTADOS.

# +
import numpy as np
q=[[] for i in range(N_PROV)]
r=[[] for i in range(N_PROV)]
dHondt=[[] for i in range(N_PROV)]
for i in range(N_PROV):
    r[i]=[]
    for j in range(int(df3.loc[i]['DIPUTADOS'])):
        A=p[i][j]
        r[i].append(A.values)
        q[i]=np.array((r[i])).T
        dHondt[i]=pd.DataFrame(q[i])
        
#dHondt es un array que representa la tabla d'Hondt  
# -

#lista_votos[I] es una lista de longitud N_PROVINCIAS que tiene los valores ordenados de la 
#tabla d'Hondt de cada provincia. Si no existen valores duplicados con lista_votos[I][DIPUTADOS-1]
#en lista_votos[I][>=DIPUTADOS] se eligen los primeros términos hasta DIPUTADOS y se asignan los escaños
#según las veces que aparezca cada partido. Si existen duplicados, se seleccionan aquellos partidos
#que tienen el mismo valor del índice que lista_votos[I][DIPUTADOS-1] y, enre ellos, se eligen al azar
#las candidaturas que deben completar el número de escaños. p.e. si hay DIPUTADOS=6 y 
#lista_votos[I][4]=lista_votos[I][5]=lista_votos[I][6]=lista_votos[I][7]=1000 elegiremos aleatoriamente
#dos de las cuatro empatadas para los dos escaños vacantes.
lista_votos=[[] for i in range(N_PROV)]
for i in range(N_PROV):
    lista_votos[i]=[]
    for j in range(int(df3.loc[i]['DIPUTADOS'])):
        lista_votos[i]=lista_votos[i]+list(p[i][j])
        
        lista_votos[i].sort(reverse=True)

#Exporto d'Hondt 
F=input("¿DESEA EXPORTAR LAS TABLAS d'HONDT? (Y/N)")
if F=='Y' or F=='Y'.lower():
    for i in range(N_PROV):
        A=dHondt[i][dHondt[i]>0].dropna(axis=0, how='all') 
        B=pd.DataFrame(lista_votos[i])
        B[B>0].dropna(axis=0, how='all') 
        Name='dHondt'+str(i)
        writer = pd.ExcelWriter(Name+'.xlsx')
        A.to_excel(writer,'dHondt')
        B.to_excel(writer,'lista_votos')
        writer.close()


