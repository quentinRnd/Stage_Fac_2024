#modele qui va intergrer les chemin ayant des caractéristique

from pycsp3 import *
import numpy as np
import pandas as pd
import os 
import json
import re
import argparse
import time
from settings import *
import datetime

def creation_repertoire(nomrep):
    if not os.path.exists(nomrep): 
        os.makedirs(nomrep)

#retourne l'emplacement du fichier rechercher
def nom_fichier(instance_repertory,nom_instance,extension_instance):
    return instance_repertory+"/"+nom_instance+extension_instance

def optimisation_chemin(nom_instance
                        ,chemin_profile
                        ,profile_choisi
                        ):
    pass

def modele4_json(nom_instance
            ,solver_verbose
            ,instance_repertory
            ,timeout_solver
            ,nombre_solution
            ,fonction_objectif
            ,timeout_activer
            ,solver
            ,extension_instance
            ,type_objectif
            ,repertoire_solution
            ,repertoire_preference_util
            ,preference_util
            ,solution_inter
            ,timeout_sol_inter):
    #categorie permise par le modele
    categorie_permise= [i for i in range (1000)]
    with open(f"{instance_repertory}/{nom_instance}.json") as instance_json:
        #budget maximum alloué au visite
        budget_max=2000

        #temps de visite max allouer a la somme des temps de visite des points d'intérêt
        Temps_max_visite=3000

        #distance parcourue par les utilisateur.ice
        distance_parcourue_max=100
        distance_parcourue_min=10
        
        #capacité max des pdi
        capacite_max=500


        with open(f"{repertoire_preference_util}/{preference_util}") as preference_json:
            #objet json qui contient les préférence utilisteur.ice pour les chemins
            preference_util_data=json.load(preference_json)
            
            #objet json qui contient l'instance json 
            instance = json.load(instance_json)

            #tableau qui me permet de traiter les différente préférence utilisateur.ice
            preference_util_tab=[
                                    preference_util_data[preference_marche_key][nature_key]
                                    ,preference_util_data[preference_marche_key][ville_key]
                                    ,preference_util_data[preference_marche_key][élevation_key]
                                    ,preference_util_data[preference_marche_key][foret_key]
                                    ,preference_util_data[preference_marche_key][lac_key]
                                    ,preference_util_data[preference_marche_key][riviere_key]
                                ]
            #recuperation de l'interet utilisateur.ice
            interet_chemin=preference_util_data[interet_chemin_key]


            capacite_max=preference_util_data[capacite_max_key]

            budget_max=preference_util_data[budget_max_key]

            Temps_max_visite=preference_util_data[Temps_max_visite_key]

            distance_parcourue_max=preference_util_data[distance_parcourue_max_key]
            distance_parcourue_min=preference_util_data[distance_parcourue_min_key]
            Tranche_temps=preference_util_data[Tranche_temps_key]
            



            #variable qui va contenir les different chemin qui aura les valuation mixer 
            chemin_valuer=[]

            #je vais faire en sorte de mixer les interet preference util et les interet des chemin dans l'instance
            for i in range(len(instance[Categorie_chemin_pdi_key])):
                aux=[]
                for j in range(len(instance[Categorie_chemin_pdi_key][i])):
                    if instance[Categorie_chemin_pdi_key][i][j] is not None:
                        aux.append(
                                    int(
                                        sum(
                                            [
                                                instance[Categorie_chemin_pdi_key][i][j][k]*preference_util_tab[k]*interet_chemin
                                                    for k in range(max(len(instance[Categorie_chemin_pdi_key][i][j]),len(preference_util_tab)))
                                            ]
                                           )
                                      )
                                  )
                    else:
                        aux.append(0)
                chemin_valuer.append(aux)
            modele4(
                        nom_instance=nom_instance
                        ,solver_verbose=niveau_verbose
                        ,instance_repertory=instance_repertory
                        ,timeout_solver=timeout_solver
                        ,nombre_solution=nombre_solution
                        ,fonction_objectif=fonction_objectif
                        ,timeout_activer=timeout_activer
                        ,solver=solver
                        ,extension_instance=extension_instance
                        ,type_objectif=type_objectif
                        ,repertoire_solution=repertoire_solution
                        ,categorie_permise=categorie_permise
                        ,budget_max=budget_max
                        ,prix_entrer=instance[Cout_entrer_key]
                        ,ouverture_pdi=instance[Heure_ouverture_key]
                        ,fermeture_pdi=instance[Heure_fermeture_key]
                        ,interet_pdi=instance[Score_pdi_key]
                        ,coord_x=instance[X_PDI_key]
                        ,coord_y=instance[Y_PDI_key]
                        ,duree_visite=instance[Temps_visite_key]
                        ,capaciter_pdi=instance[Capacite_key]
                        ,categorie_pdi=instance[Categorie_key]
                        ,Temps_max_visite=Temps_max_visite
                        ,chemin_valuer=chemin_valuer

                        ,capacite_max=capacite_max
                        ,distance_parcourue_max=distance_parcourue_max
                        ,distance_parcourue_min=distance_parcourue_min
                        ,solution_inter=solution_inter
                        ,timeout_sol_inter=timeout_sol_inter
                        ,tranche_temps=Tranche_temps

                    )
                    #a faire 
                    #faire en sorte de passer les donnée preference utilisateur sur les feuille de la matrice des chemin
                    #crée une fonction objectif qui ce focus sur maximiser la somme du coup des chemins

#nom du répertoire ou sont les instances
def modele4(nom_instance
            ,solver_verbose
            ,instance_repertory
            ,timeout_solver
            ,nombre_solution
            ,fonction_objectif
            ,timeout_activer
            ,solver
            ,extension_instance
            ,type_objectif
            ,repertoire_solution
            ,categorie_permise
            ,budget_max
            ,prix_entrer
            ,ouverture_pdi
            ,fermeture_pdi
            ,interet_pdi
            ,coord_x
            ,coord_y
            ,duree_visite
            ,capaciter_pdi
            ,categorie_pdi
            ,Temps_max_visite
            #les chemin de l'instance ayant des valuation sur les chemin 
            ,chemin_valuer
            ,capacite_max
            ,distance_parcourue_max
            ,distance_parcourue_min
            #est ce que l'on produit des solution intermédiaire
            ,solution_inter
            ,timeout_sol_inter
            ,tranche_temps
):
    clear()
    print(f"solving {nom_instance}")
    
    #Prix d'entrer pour chaque point d'interêt
    b=[]

    #horaire d'ouverture des points d'interêts
    e=[]

    #horaire de fermeture  des points d'interêts
    c=[]

    #sert a savoir l'intérêt de l'utilisateur.ice envers les point d'interêt
    score_pdi=[]

    #cordonnée x des différent point d'intérêt
    loc_x=[]

    #cordonnée y des différent point d'intérêt
    loc_y=[]

    #durée de la visite des points d'intérêt
    t=[]

    #capacitée de chaque point d'intérêt
    capacite=[]
    #catégorie des point d'intérêt
    categorie=[]
    """
    Contrainte 5
    """
    #chemin valuer en fonction des catégorie des pdi
    chemin_valuer_aux=[]
    pdi_accepter=[i for i in range(len(prix_entrer)) if categorie_pdi[i] in categorie_permise]
    for i in range(len(categorie_pdi)):
        if categorie_pdi[i] in categorie_permise:
            b.append(prix_entrer[i])
            e.append(ouverture_pdi[i])
            c.append(fermeture_pdi[i])
            score_pdi.append(interet_pdi[i])
            loc_x.append(coord_x[i])
            loc_y.append(coord_y[i])
            t.append(duree_visite[i])
            capacite.append(capaciter_pdi[i])
            categorie.append(categorie_pdi[i])
            chemin_valuer_aux.append([chemin_valuer[i][j] for j in pdi_accepter]) 
    chemin_valuer=chemin_valuer_aux

    #nombre de point d'interêt dans l'instance 
    N = len(loc_x)


    #variable qui me sert a pas me tromper dans le parcours de mes pdi
    parcours_pdi=range(0, N)

    #sert a représenter les connection entre les differrent point d'intérêt 
    #x[i][j] est égale a 1 si j est visiter après i 0 sinon
    #x = VarArray(size=[N, N], dom=lambda i, j: {0} if i == j or chemin_valuer[i][j]==0 else {0, 1})

    #variable qui contient le circuits
    circuit = VarArray(size=N, dom=lambda i: {j for j in parcours_pdi if chemin_valuer[i][j]!=0 or i==j })



    #distance entre tout les point d'intérêt
    distance = {(i, j): round(np.hypot(loc_x[i]-loc_x[j], loc_y[i]-loc_y[j])) for i in parcours_pdi for j in parcours_pdi }
    #variable qui contient les même valeur que distance ça sert juste pour acceder a ses valeur avec le systeme de suscesseur de circuit 
    distance_var=VarArray(size=[N, N], dom=lambda i, j: {distance[i,j]}  )
    #pareille mais pour les chemin 
    chemin_valuer_var=VarArray(size=[N, N], dom=lambda i, j: {chemin_valuer[i][j]}  )
    #pareille pour les score des pdi
    score_pdi_var=VarArray(size=N, dom=lambda i: {score_pdi[i]}  )
    #tableau ayant pour donnée les heure de depart de chaque viste de chaque point d'intérêt
    s = VarArray(size=N,dom=range(0,int((Temps_max_visite+1)/tranche_temps)))

    #tableau permettant de savoir si un point d'interêt est visité 
    y = VarArray(size=N, dom=(0,1))

    




    #distance minimum a parcourir
    d_min = distance_parcourue_min
    #distance maximum a parcourir
    d_max = distance_parcourue_max

    #catégorie présente dans la dataframe
    categorie_df=[]
    for i in categorie:
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
        valeur_ajout=100
        depense_max_categorie[i]=valeur_ajout

    """
    Pour les explications des contraintes voir le rapport 
    """
    """
    Contrainte 1
    """
    
    #satisfy( disjunction(((s[i]*tranche_temps)+(t[i]*y[i])+distance[i,j]<=(s[j]*tranche_temps)) ,s[j]==Minimum(s), (x[i][j]==0))  for i in parcours_pdi for j in parcours_pdi if i!=j )
    if not solution_inter:    
        satisfy( disjunction(
                            (
                                (s[i]*tranche_temps)+(t[i]*y[i])+distance_var[i][circuit[i]]<=(s[circuit[i]]*tranche_temps)
                            ) 
                            ,s[circuit[i]]==Minimum(s)
                            ,(circuit[i]==i))  
                                for i in parcours_pdi )
    """
    Contrainte 2
    """
    satisfy(Sum(b[i]*y[i] for i in parcours_pdi)<=budget_max)

    """
    Contrainte 3
    """
    satisfy((s[i]*tranche_temps) >= (e[i]*y[i]) for i in parcours_pdi)
    satisfy((((s[i]*tranche_temps)+t[i])*y[i]) <= c[i] for i in parcours_pdi)
    """
    Contrainte 4
    """
    satisfy((capacite[i] * y[i]) <=capacite_max for i in parcours_pdi)

    """
    Contrainte 5
    """
    satisfy(Sum(t[i]*y[i] for i in parcours_pdi)<=Temps_max_visite)

    """
    Contrainte 7
    """
    satisfy(Sum(b[i]*y[i]*(categorie[i]==j) for i in parcours_pdi)<=depense_max_categorie[j] for j in categorie_df)

    """
    Contrainte 8
    """
    satisfy(Sum((circuit[i]!=i)*distance_var[i][circuit[i]]  for i in parcours_pdi  )>d_min )
    satisfy(Sum((circuit[i]!=i)*distance_var[i][circuit[i]]  for i in parcours_pdi  )<d_max )

    """
    Contrainte 9
    """
    #nombre de point par jour a visiter au maximum
    max_point_par_jour = 20
    #nombre de poutn par jour a visiter au minimum
    min_point_par_jour = 3

    satisfy(Sum(y[i] for i in parcours_pdi)>min_point_par_jour)
    satisfy(Sum(y[i] for i in parcours_pdi)<max_point_par_jour)

    """
    Contrainte 10
    """

    #point d'intéret a visiter au minimum
    #pour instacia14
    #mandatory=[7,2]
    mandatory=[]

    satisfy(y[i]==1 for i in mandatory)

    """
    Contrainte 11
    """
    satisfy( disjunction(y[i]==0,circuit[i]!=i) for i in parcours_pdi )
    """
    Contrainte 12
    """
    satisfy(Circuit(circuit))

    """
    Contrainte 13
    """
    satisfy(AllDifferent(s))
    """
    Fonction objectif
    """
    #fonction objectif qui maximise la satisfaction utilisateur.ice
    if(fonction_objectif):    
        if(type_objectif==Maximise_score_pdi):
            maximize(Sum(y[i]*score_pdi[i] for i in parcours_pdi))
        if(type_objectif==Mix_distance_score_pdi):
            maximize(Sum(y[i]*score_pdi[i] for i in parcours_pdi))
            minimize((Sum((circuit[i]!=i)*distance_var[i][circuit[i]] for i in parcours_pdi)))
        if(type_objectif==Maximise_score_chemin):
            maximize(Sum((circuit[i]!=i)*(chemin_valuer_var[i][circuit[i]]+(score_pdi[i]+score_pdi_var[circuit[i]])) for i in parcours_pdi))
    #timout pour le solver
    solver_timeout_seconds=timeout_solver

    solver_effectif=ACE
    if(solver=="ACE"):
        solver_effectif=ACE
    else: 
        if solver=="CHOCO":
            solver_effectif=CHOCO
        else:
            solver_effectif=ACE
    
    #tableau contenant les different solution 
    tab_res=[]
    #tableau contenant les different solution intermediaire
    tab_res_inter=[]

    boundmax=0
    #sert a savoir quand on a commencer le solve 
    debut_solve=int(time.time())

    print("start of the solve ",datetime.datetime.now())

    resultat_recherche=solve(solver=solver_effectif 
                            ,sols=nombre_solution
                            ,verbose=solver_verbose
                            ,options=f"-t={int(timeout_sol_inter) if solution_inter else int(solver_timeout_seconds)}s" if timeout_activer else "")
    #sert a savoir quand on a fini le solve
    print("ending of the solve ",datetime.datetime.now())
    fin_solve=int(time.time())


    p_recherche=None
    if resultat_recherche is SAT or resultat_recherche is OPTIMUM is not UNSAT:
        print(f"Nombre de solutions: {n_solutions()} pour l'instance {nom_instance}" )
        boundmax=bound()
        for numero_solution in range(n_solutions()):
            #valeur des arcs relier entre les pdi 
            #arc_res=values(x, sol=numero_solution)

            #valeur des pdi present dans la solution
            pdi_present=values(y, sol=numero_solution)

            #valeur des départ des visite des pdi 
            start_pdi=values(s, sol=numero_solution)

            #valeur du circuit créé
            circuit_res=values(circuit,sol=numero_solution)
            circuit_res=[[i,circuit_res[i]] for i in range(len(circuit_res)) if i !=circuit_res[i]]
            
            p_recherche=circuit_res
            
            tab_res.append({Presence_pdi_key:pdi_present,Start_pdi_key:start_pdi,Circuit_key:circuit_res})
    


    else:
        print(f"il n'y a pas de solutions pour l'instance {nom_instance}")
    #objet qui contient toutes les donnée sur la recherche
    
    data={
            Status_key:
                    {
                        Fin_recherche_key:resultat_recherche.__str__()
                        ,Optimum_key:resultat_recherche is OPTIMUM
                    }
            ,Bound_key:boundmax
            ,Distance_max_key:d_max
            ,Distance_min_key:d_min
            ,Tranche_temps_key: tranche_temps
            ,Type_objectif_key:type_objectif
            ,Timeout_solver_key:solver_timeout_seconds
            ,Timeout_activer_key:timeout_activer
            ,Solutions_key:tab_res
            ,Coordonee_pdi_x_key:loc_x
            ,Coordonee_pdi_y_key:loc_y
            ,Temps_visite_key:t
            ,Score_pdi_key:score_pdi
            ,Closing_pdi_key:c
            ,Opening_pdi_key:e
            ,Evaluation_path_key:chemin_valuer
        }
    json_data=json.dumps(data, indent=3)
    fichier=None
    repertoire_inter=f"{repertoire_solution}/sol_inter"
    if solution_inter:
        creation_repertoire(repertoire_inter)
        fichier = open(f"{repertoire_inter}/{nom_instance}.json", "w")
    else:
        fichier = open(f"{repertoire_solution}/{nom_instance}.json", "w")
    fichier.write(json_data)
    fichier.close()
    print(f"solution saved in {repertoire_inter if solution_inter else repertoire_solution}/{nom_instance}.json")
        

    #clear toute les contraintes précédement poster 
    clear()

    if solution_inter and p_recherche != None:
        indice_sol=[i[0] for i in p_recherche]
        capaciter_pdi_sol=[]
        categorie_pdi_sol=[]
        chemin_valuer_sol=[]
        coord_x_sol=[]
        coord_y_sol=[]
        duree_visite_sol=[]
        fermeture_pdi_sol=[]
        interet_pdi_sol=[]
        ouverture_pdi_sol=[]
        prix_entrer_sol=[]

        for i in indice_sol:
            capaciter_pdi_sol.append(capacite[i])
            categorie_pdi_sol.append(categorie[i])
            chemin_aux=[]
            for j in indice_sol:
                chemin_aux.append(chemin_valuer[i][j])
            chemin_valuer_sol.append(chemin_aux)
            coord_x_sol.append(loc_x[i])
            coord_y_sol.append(loc_y[i])
            duree_visite_sol.append(t[i])
            fermeture_pdi_sol.append(c[i])
            interet_pdi_sol.append(score_pdi[i])
            ouverture_pdi_sol.append(e[i])
            prix_entrer_sol.append(b[i])




        modele4(nom_instance=nom_instance
                ,solver_verbose=solver_verbose
                ,instance_repertory=instance_repertory
                ,budget_max=budget_max
                ,capacite_max=capacite_max
                ,capaciter_pdi=capaciter_pdi_sol
                ,categorie_pdi=categorie_pdi_sol
                ,categorie_permise=categorie_permise
                ,chemin_valuer=chemin_valuer_sol
                ,coord_x=coord_x_sol
                ,coord_y=coord_y_sol
                ,distance_parcourue_max=distance_parcourue_max
                ,distance_parcourue_min=distance_parcourue_min
                ,duree_visite=duree_visite_sol
                ,extension_instance=extension_instance
                ,fermeture_pdi=fermeture_pdi_sol
                ,fonction_objectif=fonction_objectif
                ,interet_pdi=interet_pdi_sol
                ,nombre_solution=nombre_solution
                ,ouverture_pdi=ouverture_pdi_sol
                ,prix_entrer=prix_entrer_sol
                ,repertoire_solution=repertoire_solution
                ,solution_inter=False
                ,solver=solver
                ,Temps_max_visite=Temps_max_visite
                ,timeout_activer=timeout_activer
                ,timeout_solver=timeout_solver+abs(timeout_sol_inter-(fin_solve-debut_solve))
                ,type_objectif=type_objectif
                ,timeout_sol_inter=timeout_sol_inter
                ,tranche_temps=tranche_temps)


if __name__ == "__main__":

    #permet de remetre le dossier d'execution du script ou est le script 
    os.chdir(os.path.dirname(__file__))

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
        instance_repertory=settings[nom_repertoire_instance_json_key]
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
        #extension pour les instances csv
        extension_instance=settings[extension_instance_key]

        #type d'objectif rechercher
        type_objectif=settings[type_objectif_key]

        #repertoire ou sont stocker les préférence utilisateur.ice
        repertoire_preference_util=settings[repertoire_profile_marcheureuse_key]

        #fichier preference utilisateur.ice choisie
        preference_util=settings[profile_marcheureuse_choisie_key]
        
        #savoir si oui ou non on produit des solution intermediaire
        solution_inter=settings[inter_solution_key]

        #savoir  quelle est le timeout pour les solution intermediaire
        timeout_sol_inter=settings[timout_solution_inter_key]

        #identifiant processus
        num_thread=1
        #identifiant du nombre de procesus en parrallèle
        decalage_thread=0
        #fichier a traiter en solo
        file_a_traiter=""
        
        

        parser = argparse.ArgumentParser(description='Optional app description')

        # Optional argument
        parser.add_argument(f"--{key_file_include[key_short_arg]}", type=str,default=None,
                    help='add file tout solve')
        parser.add_argument('-output', type=str,
                    help='allow to name your output xml for pycsp3 ')
        parser.add_argument(f"--{key_num_thread[key_short_arg]}", type=int,default=None,
                    help='select how much there is thread concurent')
        parser.add_argument(f"--{key_id_thread[key_short_arg]}", type=int,default=None,
                    help='identifie the thread')
        
        args = parser.parse_known_args()
        if args[0].f is not None:
            #fichier que j'ai passer en paramètre de mon programme
            file_a_traiter=args[0].f
        if args[0].t is not None:
            num_thread=int(args[0].t)
        if  args[0].i is not None:
            decalage_thread=int(args[0].i)
        
        creation_repertoire(repertoire_solution)
        #recupere toute les instance du dossier des instances
        instances=os.listdir(instance_repertory)
        pattern=r'\w+'
        #permet de récuperer uniquement les nom des fichier 
        instances=sorted([re.findall(pattern, i)[0] for i in instances])
                
        if(file_a_traiter!=""):
            if(os.path.exists(nom_fichier
                                        (
                                            extension_instance=".json"
                                            ,instance_repertory=instance_repertory
                                            ,nom_instance=file_a_traiter
                                        )
                             )
              ):
                instances=[file_a_traiter]
            else:
                #sort du programme parce que le fichier est instrouvable
                print(f"file {file_a_traiter} does not exists")
                
                exit(0)
        #instance déjà traiter 

        instance_exclu=[]
        if num_thread==1:
            for instance in instances:
                if instance not in instance_exclu:
                    modele4_json(instance
                        ,solver_verbose=niveau_verbose
                        ,instance_repertory=instance_repertory
                        ,timeout_solver=timeout_solver
                        ,nombre_solution=nombre_solution
                        ,fonction_objectif=fonction_objectif
                        ,timeout_activer=timeout_activer
                        ,solver=solver
                        ,extension_instance=extension_instance
                        ,type_objectif=type_objectif
                        ,repertoire_solution=repertoire_solution
                        ,repertoire_preference_util=repertoire_preference_util
                        ,preference_util=preference_util
                        ,solution_inter=solution_inter
                        ,timeout_sol_inter=timeout_sol_inter
                )
                    
        else:
            instance_traiter=decalage_thread
            nombre_instance_traiter=0
            instance_deja_solve=-1
            while instance_traiter < len(instances):
                if nombre_instance_traiter>instance_deja_solve:    
                    
                    modele4_json(instances[instance_traiter]
                        ,solver_verbose=niveau_verbose
                        ,instance_repertory=instance_repertory
                        ,timeout_solver=timeout_solver
                        ,nombre_solution=nombre_solution
                        ,fonction_objectif=fonction_objectif
                        ,timeout_activer=timeout_activer
                        ,solver=solver
                        ,extension_instance=extension_instance
                        ,type_objectif=type_objectif
                        ,repertoire_solution=repertoire_solution
                        ,repertoire_preference_util=repertoire_preference_util
                        ,preference_util=preference_util
                        ,solution_inter=solution_inter
                        ,timeout_sol_inter=timeout_sol_inter
                    )
                instance_traiter+=num_thread
                nombre_instance_traiter+=1
            print(f"fin du traitement du process {decalage_thread}")
    
