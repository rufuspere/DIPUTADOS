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
#DIPUTADOS38: PARTE VIII: ARCHIVO DE SALIDA EXCEL

# %%
guion="Diputados38"

# %%
#salida con ceros de datos MinInt
output1=resultados.copy()

# %%
estructura(output1)

# %%
list(output1.loc[0].keys())

# %%
A=[]
M1=[i for i in range(pos(output1,'1Votos'),pos(output1,'DDERECHA'))]
M=list(output1.loc[0][M1].keys())
for y in M:
    if (output1[y] == 0).all():
        A.append(y)

# %%
common=set(A).intersection(set(output1.loc[0].keys()))
#salida sin ceros
output2=output1.drop(columns=list(common),axis=1)

# %%
#salida con ceros de asignaciones
output3=pd.concat([DF71[VV0],DF71[VV1],DF71[VV2],DF71[VV7],DF71[VV8]],axis=1)

# %%
B=[]
M1=[i for i in range(pos(output3,'1Votos'),pos(output3,'DIPDERECHA'))]
M=list(output3.loc[0][M1].keys())
for y in M:
    if (output3[y] == 0).all():
        B.append(y)

# %%
common=set(B).intersection(set(output3.loc[0].keys()))
#salida sin ceros de asignaciones
output4=output3.drop(columns=list(common),axis=1)

# %%
#salida de >barrera con ceros
output5=pd.concat([DF71[VV0],DF71[VV5],DF71[VV6],DF71[VV7],DF71[VV8]],axis=1)

# %%
U=[]
U=VV5+VV7
C=[]
M=list(output5.loc[0][U].keys())
for y in M:
    if (output5[y] == 0).all():
        C.append(y)

# %%
common=set(C).intersection(set(output5.loc[0].keys()))
#salida sin ceros de >barrera
output6=output5.drop(columns=list(common),axis=1)

# %%

F=input("¿DESEA EXPORTAR LOS RESULTADOS? (Y/N)\n")
if F=='Y' or F=='Y'.lower():
    Res=input("¿Qué nombre desea concatenar con 'Resultados'\n")
    Name='Resultados'+str(Res)
    G=input("¿DESEA ELIMINAR VALORES NULOS DE VOTOS?\n\
    (no es conveniente si se desea comparación con resultados iniciales\n(Y/N)\n") 
    if G=='Y' or G=='Y'.lower():
        writer = pd.ExcelWriter(Name+'.xlsx')
        results=output2
        results.to_excel(writer,sheet_name='DatosRealesMint')
        results=output4
        results.to_excel(writer,sheet_name='VotosReasignados')
        results=output6
        results.to_excel(writer,sheet_name='Datos>barrera')
        writer.close()
    if G=='N' or G=='N'.lower():
        writer = pd.ExcelWriter(Name+'.xlsx')
        results=output1
        results.to_excel(writer,sheet_name='DatosRealesMint')
        results=output3
        results.to_excel(writer,sheet_name='VotosReasignados')
        results=output5
        results.to_excel(writer,sheet_name='Datos>barrera')
        writer.close()

