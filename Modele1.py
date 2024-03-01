from pycsp3 import *
import numpy as np
import pandas as pd

import json

#durée maximal de la visite peut être aussi vu comme une heure de fin
max_tiempo=2000

#catégorie de point d'interet permise dans la selection 
#catégorie pour l'instance 14
categorie_permise = [1,2,3]

#nom de l'instance utiliser pour trouver des solutions
nom_instance="Instancia14"
#extension de fichier utiliser pour l'instance
extension_instance=".csv"

#nom du répertoire ou sont les instances
nom_repertoire_instance="Instancias"

#dataFrame contenant l'instance 
df=pd.read_csv(nom_repertoire_instance+"/"+nom_instance+extension_instance,sep=";")

"""
Contrainte 6
"""
df = df[df["categoria"].isin(categorie_permise)]

#budget maximum alloué au visite
budget_max=2000

#Prix d'entrer pour chaque point d'interêt
b = df['entrada_k'].values.tolist()

#horaire d'ouverture des points d'interêts
e = df['open_k'].values.tolist()
#horaire de fermeture  des points d'interêts
c = df['close_k'].values.tolist()

#sert a savoir l'intérêt de l'utilisateur.ice envers les point d'interêt
score_pdi= df['score_k'].values.astype(int).tolist()

df = df.head(100).reset_index()

#nombre de point d'interêt dans l'instance 
N = len(df)

#sert a représenter les connection entre les differrent point d'intérêt 
#x[i][j] est égale a 1 si j est visiter après i 0 sinon
x = VarArray(size=[N, N], dom=lambda i, j: {0} if i == j else {0, 1})

#cordonnée x des différent point d'intérêt
loc_x = df['X_k'].astype(int).round().values.tolist()
#cordonnée y des différent point d'intérêt
loc_y = df['Y_k'].astype(int).round().values.tolist()

#Point d'intérêt
point=[i for i in range(N)] 
#arc relian les points d'intérêt
arc =[(i,j) for i in point for j in point if i!=j]

#distance entre tout les point d'intérêt
distance = {(i, j): round(np.hypot(loc_x[i]-loc_x[j], loc_y[i]-loc_y[j])) for i, j in arc}

#durée de la visite des points d'intérêt
t = df['duracion_k'].values.tolist()

#tableau ayant pour donnée les heure de depart de chaque viste de chaque point d'intérêt
s = VarArray(size=N,dom=range(0,max_tiempo+1))

#tableau permettant de savoir si un point d'interêt est chosi dans le chemin 
y = VarArray(size=N, dom=(0,1))

#variable qui me sert a pas me tromper dans le parcours de mes pdi
parcours_pdi=range(0, N)
#Capacité max autoriser par l'utilisateur.ice
capacite_max = 70
#capacitée de chaque point d'intérêt
capacite= df['capacidad'].values.astype(int).tolist()

#catégorie des point d'intérêt
categorie=df['categoria'].tolist()

#temps de visite max allouer a la somme des temps de visite des points d'intérêt
Temps_max_visite=3000

#distance minimum a parcourir
d_min = 10
#distance maximum a parcourir
d_max = 10000

#catégorie présente dans la dataframe
categorie_df=[]
for i in df["categoria"]:
    if i not in categorie_df:
        categorie_df.append(i)
categorie_df=sorted(categorie_df)

#dépense max par catégorie 
depense_max_categorie={}
for i in categorie_df:
    valeur_ajout=0
    match i:
        case 1:
            valeur_ajout=2000
        case 2:
            valeur_ajout=1000
        case 3:
            valeur_ajout=1500
    depense_max_categorie[i]=valeur_ajout


dossier_save_def="instance_solve"
df.to_csv(dossier_save_def+"/"+nom_instance+extension_instance)

"""
Pour les explications des contraintes voir le rapport 
"""

"""
Contrainte 1
"""
satisfy(Sum (x[:, i]) <2 for i in parcours_pdi)
satisfy(Sum (x[i, :]) <2 for i in parcours_pdi)
"""
Contrainte 2
"""
satisfy( disjunction((s[i]+t[i]+distance[i,j]-s[j]<=0) , (1-x[i][j]))  for i in parcours_pdi for j in parcours_pdi if i!=j )


"""
Contrainte 3
"""
satisfy(Sum(b[i]*y[i] for i in parcours_pdi)<=budget_max)

"""
Contrainte 4
"""
satisfy(s[i] >= (e[i]*y[i]) for i in parcours_pdi)
satisfy(((s[i]+t[i])*y[i]) <= c[i] for i in parcours_pdi)
"""
Contrainte 5
"""
satisfy((capacite[i] * y[i]) <=capacite_max for i in parcours_pdi)

"""
Contrainte 7
"""
satisfy(Sum(t[i]*y[i] for i in parcours_pdi)<=Temps_max_visite)

"""
Contrainte 8
"""
satisfy(Sum(b[i]*y[i]*(categorie[i]==j) for i in parcours_pdi)<=depense_max_categorie[j] for j in categorie_df)

"""
Contrainte 9
"""
satisfy(Sum(x[i,j]*distance[i,j] for j in parcours_pdi for i in parcours_pdi if i!=j )>d_min )
satisfy(Sum(x[i,j]*distance[i,j] for j in parcours_pdi for i in parcours_pdi if i!=j )<d_max )

"""
Contrainte 10
"""
#nombre de point par jour a visiter au maximum
max_point_par_jour = 20
#nombre de poutn par jour a visiter au minimum
min_point_par_jour = 3

satisfy(Sum(y[i] for i in parcours_pdi)>min_point_par_jour)
satisfy(Sum(y[i] for i in parcours_pdi)>max_point_par_jour)

"""
Contrainte 11
"""

#point d'intéret a visiter au minimum
mandatory=[7,2]

satisfy(y[i]==1 for i in mandatory)

"""
Contrainte 12
"""

satisfy(disjunction(conjunction(y[i]==1,y[j]==1,x[i,j]==1),x[i,j]==0) for i in parcours_pdi for j in parcours_pdi)

"""
Contrainte 13
"""

satisfy(disjunction(conjunction(y[i]==1,Maximum(x[i,:])==1),conjunction(y[i]==1,Maximum(x[:,i])==1),y[i]==0) for i in parcours_pdi)

"""
Contrainte 14
"""
satisfy(disjunction(conjunction(y[i],s[i]>=0),conjunction(y[i]==0,s[i]==0)))

"""
Fonction objectif
"""
#fonction objectif qui maximise la satisfaction utilisateur.ice
#maximize(Sum(y[i]*score_pdi[i] for i in parcours_pdi))

repertoire_solution="solution"
resultat_recherche=solve(sols=100)
if resultat_recherche is SAT or resultat_recherche is OPTIMUM is not UNSAT:
    print(f"Nombre de solutions: {n_solutions()}" )
    
    fichier = open(f"{repertoire_solution}/solution_{nom_instance}.json", "w")
    
    #tableau qui compile toute les valeurs résultat trouvé
    tab_res=[]
    
    for numero_solution in range(n_solutions()):
        #valeur des arcs relier entre les pdi 
        arc_res=values(x, sol=numero_solution)

        #valeur des pdi present dans la solution
        pdi_present=values(y, sol=numero_solution)

        #valeur des départ des visite des pdi 
        start_pdi=values(s, sol=numero_solution)
        tab_res.append([arc_res,pdi_present,start_pdi])
    
    json_data=json.dumps(tab_res, indent=3)
    
    fichier.write(json_data)
    sol=0
    for ligne in tab_res:
        arc=ligne[0]
        print(f"solution {sol}")
        for i in range(len(arc)):
            for j in range(len(arc[i])):
                if(arc[i,j]==1):
                    print(i,j)
        sol+=1
        

    fichier.close()
else:
    print("il n'y a pas de solutions")

