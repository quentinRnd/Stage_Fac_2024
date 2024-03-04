from pycsp3 import *
import numpy as np
import pandas as pd
import os 
import json
import re

from settings import *

#nom du répertoire ou sont les instances

def modele1(nom_instance
            ,solver_verbose
            ,instance_repertory
            ,timeout_solver
            ,nombre_solution
            ,fonction_objectif
            ,timeout_activer
            ,solver
):
    print(f"solving {nom_instance}")
    

    #catégorie de point d'interet permise dans la selection 
    #catégorie pour l'instance 14
    #categorie_permise = [1,2,3]
    categorie_permise= [i for i in range (1000)]

    #extension de fichier utiliser pour l'instance
    extension_instance=".csv"



    #dataFrame contenant l'instance 
    df=pd.read_csv(instance_repertory+"/"+nom_instance+extension_instance,sep=";")

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
     

    #temps de visite max allouer a la somme des temps de visite des points d'intérêt
    Temps_max_visite=3000
    #tableau ayant pour donnée les heure de depart de chaque viste de chaque point d'intérêt
    s = VarArray(size=N,dom=range(-1,Temps_max_visite+1))

    #tableau permettant de savoir si un point d'interêt est chosi dans le chemin 
    y = VarArray(size=N, dom=(0,1))

    #variable qui me sert a pas me tromper dans le parcours de mes pdi
    parcours_pdi=range(0, N)
    #Capacité max autoriser par l'utilisateur.ice
    capacite_max = 500
    #capacitée de chaque point d'intérêt
    capacite= df['capacidad'].values.astype(int).tolist()

    #catégorie des point d'intérêt
    categorie=df['categoria'].tolist()



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
    """
    pour l'instance 14
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
    """

    for i in categorie_df:
        valeur_ajout=100000000
        depense_max_categorie[i]=valeur_ajout

    """
    Pour les explications des contraintes voir le rapport 
    """

    """
    Contrainte 1
    """
    #attention le nombre de passage est en -1 a cause du < 
    nombre_passage_max=2
    satisfy(Sum (x[:, i]) <nombre_passage_max for i in parcours_pdi)
    satisfy(Sum (x[i, :]) <nombre_passage_max for i in parcours_pdi)
    """
    Contrainte 2
    """
    #satisfy( disjunction((s[i]+t[i]+distance[i,j]<=s[j]) , (x[i][j]==0))  for i in parcours_pdi for j in parcours_pdi if i!=j )
    satisfy( disjunction(((s[i]+t[i]+distance[i,j])<s[j]) , (x[i][j]==0))  for i in parcours_pdi for j in parcours_pdi if i!=j )

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
    satisfy(Sum(y[i] for i in parcours_pdi)<max_point_par_jour)

    """
    Contrainte 11
    """

    #point d'intéret a visiter au minimum
    #pour instacia14
    #mandatory=[7,2]
    mandatory=[]

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
    satisfy(disjunction(conjunction(y[i],s[i]>=0),conjunction(y[i]==0,s[i]==-1)))

    """
    Contrainte 15
    elle marche pas elle contraint juste faut voir pk mais a fixe
    """
    #V1
    #satisfy(disjunction(disjunction(conjunction(x[i,j]==1,x[j,k]==1) for i in parcours_pdi  for k in parcours_pdi),y[j]==0)for j in parcours_pdi)
    #V2
    #satisfy(disjunction( (x[i,j]==1)==0,x[j,k]==1)for i in parcours_pdi for j in parcours_pdi for k in parcours_pdi)
    #V3
    satisfy(disjunction(y[i]==0,s[i]==Minimum(s),s[i]==Maximum(s),conjunction(Maximum(x[i,:])==1,Maximum(x[:,i])==1))for i in parcours_pdi)
    """
    Contrainte 16
    """
    satisfy(disjunction(s[i]!=s[j],conjunction(y[i]==0,y[j]==0)) for i in parcours_pdi for j in parcours_pdi if i!=j)
    """
    Fonction objectif
    """
    #fonction objectif qui maximise la satisfaction utilisateur.ice
    match(fonction_objectif):
        case False:
            pass
        case True:
            maximize(Sum(y[i]*score_pdi[i] for i in parcours_pdi))
    #timout pour le solver
    solver_timeout_seconds=timeout_solver

    repertoire_solution="solution"

    match(solver):
        case "ACE":
            solver=ACE
        case "CHOCO":
            solver=CHOCO
        case other:
            solver=ACE
    
    resultat_recherche=solve(solver=solver 
                            ,sols=nombre_solution
                            ,verbose=solver_verbose
                            ,options=f"-t={solver_timeout_seconds}s" if timeout_activer else "")
    print(resultat_recherche)
    
    #tableau qui compile toute les valeurs résultat trouvé
    tab_res=[]
    fichier = open(f"{repertoire_solution}/solution_{nom_instance}.json", "w")

    if resultat_recherche is SAT or resultat_recherche is OPTIMUM is not UNSAT:
        print(f"Nombre de solutions: {n_solutions()} pour l'instance {nom_instance}" )

        for numero_solution in range(n_solutions()):
            #valeur des arcs relier entre les pdi 
            arc_res=values(x, sol=numero_solution)

            #valeur des pdi present dans la solution
            pdi_present=values(y, sol=numero_solution)

            #valeur des départ des visite des pdi 
            start_pdi=values(s, sol=numero_solution)
            tab_res.append({Arc_key:arc_res,Presence_pdi_key:pdi_present,Start_pdi_key:start_pdi})


    else:
        print(f"il n'y a pas de solutions pour l'instance {instance}")
    #objet qui contient toutes les donnée sur la recherche
    data={
            Status_key:
                    {
                        Fin_recherche_key:resultat_recherche.__str__()
                        ,Optimum_key:resultat_recherche is OPTIMUM
                    }
            ,Solutions_key:tab_res
            ,Coordonee_pdi_x_key:loc_x
            ,Coordonee_pdi_y_key:loc_y
            ,Temps_visite_key:t
            ,Score_pdi_key:score_pdi
        }
    json_data=json.dumps(data, indent=3)
    
    fichier.write(json_data)
    fichier.close()
    
    clear()

if __name__ == "__main__":

    #dossier ou sont stocker les settings json
    dossier_settings_json="settings_recherche"

    #fichier choisie pour aller chercher les settings json
    fichier_settings_json="settings_default.json"
    
    #Chargement des setting json pour la recherche 
    with open(f"{dossier_settings_json}/{fichier_settings_json}") as settings_json:
        #objet json qui contient les settings de la recherche
        settings = json.load(settings_json)
        #niveau de verbose que l'on autorise au solver
        niveau_verbose=settings[verbose_key]
        #repertoire ou on trouve les instance csv
        instance_repertory=settings[instance_repertory_key]
        #timout du solver 
        timeout_solver=settings[timeout_solver_key]
        #nombre de solution que le solver va chercher 
        nombre_solution=settings[nombre_solution_key]
        if(nombre_solution=="ALL"):
            nombre_solution=ALL
        repertoire_solution=settings[repertoire_solution_key]
        fonction_objectif=settings[fonction_objectif_key]
        solver=settings[solver_key]
        #timeout activer 
        timeout_activer=settings[timeout_actif_key] 

        if not os.path.exists(repertoire_solution): 
            os.makedirs(repertoire_solution) 

        #recupere toute les instance du dossier des instances
        instances=os.listdir(instance_repertory)
        pattern=r'\w+'
        #permet de récuperer uniquement les nom des fichier 
        instances=sorted([re.findall(pattern, i)[0] for i in instances])
        #instances=["Instanciapetite"]
        for instance in instances:
            modele1(instance
                    ,solver_verbose=niveau_verbose
                    ,instance_repertory=instance_repertory
                    ,timeout_solver=timeout_solver
                    ,nombre_solution=nombre_solution
                    ,fonction_objectif=fonction_objectif
                    ,timeout_activer=timeout_activer
                    ,solver=solver
            )