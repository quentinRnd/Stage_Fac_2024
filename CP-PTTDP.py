from pycsp3 import *
import numpy as np
import pandas as pd

#Ahora crearemos las cordenadas para cada ciudad.

max_tiempo=2000
nom_instance="Instancia14.csv"
nom_repertoire_instance="Instancias"
df=pd.read_csv(nom_repertoire_instance+"/"+nom_instance,sep=";")
df = df.head(100).reset_index()
n = len(df)
#df=df.drop(df.tail(52).index)
loc_x = df['X_k'].astype(int).round().values.tolist()
loc_y = df['Y_k'].astype(int).round().values.tolist()
e = df['open_k'].values.tolist()
l = df['close_k'].values.tolist()
pdi= df['score_k'].values.astype(int).tolist()
t = df['duracion_k'].values.tolist()
b = df['entrada_k'].values.tolist()
categoria= df['categoria'].values.astype(int).tolist()
capacidad= df['capacidad'].values.astype(int).tolist()

together = [[1,21], [12,16], [7,5]]
separate = [[1,3], [3, 5]]
obligatorios=[45, 31, 47, 12, 2, 35, 38, 21, 32, 7]

puntos=[i for i in range(n)] 
arcos =[(i,j) for i in puntos for j in puntos if i!=j]

distancia = {(i, j): round(np.hypot(loc_x[i]-loc_x[j], loc_y[i]-loc_y[j])) for i, j in arcos}
time = {(i, j): np.hypot(loc_x[i]-loc_x[j], loc_y[i]-loc_y[j]) for i, j in arcos}

from sklearn.metrics import pairwise_distances
distancia2=pd.DataFrame(pairwise_distances(df[['X_k','Y_k']]))
distancia2=distancia2.values.astype(int).tolist()



categoria=df['categoria'].tolist()
capacidad=df['capacidad'].tolist()

#Variables:
y = VarArray(size=n, dom=(0,1))
x = VarArray(size=[n, n], dom=lambda i, j: {0} if i == j else {0, 1})
s = VarArray(size=n,dom=range(0,max_tiempo+1))

categoria=pd.get_dummies(categoria)
categoria[12]=categoria[6]+categoria[7]

categoria_1=pd.DataFrame(categoria[12],columns = [12])
categoria_1=categoria_1[12].tolist()
c = VarArray(size=n, dom=categoria_1)


capacidad_var = VarArray(size=n, dom=capacidad)

aux = df.groupby('categoria')['categoria'].sum()

#colores = ["#EE6055","#60D394","#AAF683","#FFD97D","#FF9B85"]
#aux.plot.bar()

#import matplotlib.pyplot as plt
#aux.plot(label="Total Income")
#plt.show()

#model = Model()
# VARIANT 1

satisfy(
#RESTRICCIOn 2
    [Sum (x[:, i] for i in range(1, n)) == 1],
    [Sum (x[i, :] for i in range(1, n)) == 1]
    )
#Restriccion 3
satisfy(
        [(s[i]+ t[i] + distancia[i,j]-s[j]) <= (l[i]+t[i]+distancia[i,j])*(1-x[i,j]) for i in range(n) for j in range(n)if i!=j]
    )
#Restriccion 4
satisfy(
        [Sum (b[i]  * y [i] for i in range(n)) <= 2000]
   )

# Restricción 5
table_5 = [(s[i] - e[i], y[i], 0) for i in range(n)]
satisfy(
    [s_i >= e_i * y_i for s_i, y_i, e_i in table_5]
)

# Restricción 6
table_6 = [(l[i] - s[i], y[i], 0) for i in range(n)]
satisfy(
     [s_i <= l_i * y_i for s_i, y_i, l_i in table_6]
    #[l_i <= s_i + max_tiempo * (1 - y_i) for l_i, s_i, y_i in table_6]
)
#Restriccion 7
capacidad_max = 70
table= {(i,capacidad[i]) for i in range(n)}
if(capacidad_var[i]<=capacidad_max for i in range (n)):
  satisfy(
          (y[i],capacidad_var[i]) in table for i in range (n)
      )
# Restricción 8
categorias_permitidas = [1]  # agregar las categorias permitidas aquí
table_8 = [(y[i], categoria_1[i]) for i in range(n) if c[i] in categorias_permitidas]
satisfy(
    [(y_i, categoria_i) in table_8 for y_i, categoria_i in table_8]
)
#Restriccion 9
max_tiempo_total=3000
table_10 = [(t[i], y[i]) for i in range(n)]
satisfy(
    [Sum(t_i * y_i for t_i, y_i in table_10) <= max_tiempo_total]
)

#Restriccion 10
presupuesto_max = {
    1: 2000,
    2: 1000,
    3: 1500,
    # agregar más categorías con sus respectivos presupuestos máximos
}
for categoria in presupuesto_max:
    tabla = [(y[i], categoria_1, b[i]) for i in range(n) if c[i] == 1]
    satisfy(
        [Sum(b * y for y, categoria_1, b in tabla) <= presupuesto_max[categoria]]
    )

#Restriccion 11 con límites mínimo y máximo
d_min = 10
d_max = 10000
satisfy(
        [Sum(distancia[i,j]*y[i]  for i in range (n) for j in range (n) if i!=j)>=d_min],
        [Sum(distancia[i,j]*y[i]  for i in range (n) for j in range (n) if i!=j)<=d_max] # limitando el tiempo de las visitas
    )

#Restriccion 12
[(y[i] for i in obligatorios) ==1]

max_puntos_por_dia = 20
min_puntos_por_dia=3
table_12 = [(y[i]) for i in range(n) if y[i]==1]
satisfy(
    [Sum(y_i for y_i in table_12) <= max_puntos_por_dia],
    [Sum(y_i for y_i in table_12) >= min_puntos_por_dia],
)

#-----------------DEPENDIENDO DEL MODELO ES LA FUNCION OBJETIVO A USAR---------
# maximize(
#     Sum(y*pdi)
# )
# minimize(
#     Sum(distancia[i,j]*y[i] for i in range(n) for j in range(n) if i!=j)
# )
# minimize(
#     Sum(b[i]*y[i] for i in range(n))
# )


from pycsp3.tools.utilities import Stopwatch

import signal

class TimeoutException(Exception):
    pass

def timeout_handler(signum, frame):
    raise TimeoutException("Time is up!")

# Establecer una alarma para que se active después de 5 segundos
signal.signal(signal.SIGALRM, timeout_handler)
signal.alarm(6000)

try:
    # Hacer algo que pueda tardar más de 5 segundos
    instance = compile()
    ace = solver(ACE)
    result = ace.solve(instance)
    print("Result:", result)
    if result is OPTIMUM:
      print("The prime-looking number is: ", values(y))
    if result is SAT:
      print("The prime-looking number is: ", values(y))
    # Cancelar la alarma si la tarea se completa antes de tiempo
    signal.alarm(0)
except TimeoutException as ex:
    print(ex)
    print("Result:", result)
    # Terminar el programa si se activa la alarma
    sys.exit(1)

if result is OPTIMUM:
    solution = solution()
    print("Solution: ", solution)
    print("Solution Root: ", solution.root)
    print("Solution Variables: ", solution.variables)
    print("Solution Values: ", solution.values)
    print("Pretty Solution: ", solution.pretty_solution)

solutions = []
if solve(sols=ALL) :
    for i in range(n_solutions()):
       print(f"Solution {i+1}: {values(y,sol=i)}--->{values(s,sol=i)}---->{values(y[i],sol=i)}")
       solutions.append(values(y,sol=i))