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
import math
from utils import *
from algocustom import algo_custom_solution


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
            ,timeout_sol_inter
            ,solution_custom
            ,preference_recherche
            ,type_objectif_inter_solution
            ,nom_fichier_custom=None):
    #categorie permise par le modele
    categorie_permise= [i for i in range (1000)]

    instance_custom=None
    if nom_fichier_custom is not None:
        with open(f"{repertoire_solution}/custom_sol/{nom_fichier_custom}.json") as instance_json:
            instance_custom=json.load(instance_json)

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
            
            Max_visite_pdi=preference_util_data[Max_visite_pdi_key]
            Min_visite_pdi=preference_util_data[Min_visite_pdi_key]

            pdi_mandatory=preference_util_data[pdi_obligatoire_key]



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
            circuit_default=None
            y_default=None
            s_default=None
            solve_time_default=None
            if instance_custom is not None:
                solution_choisie=instance_custom[Solutions_key][0]
                parcour_pdi=range(len(instance[Score_pdi_key]))
                circuit=solution_choisie[Circuit_key]
                circuit_default=[i for i in parcour_pdi ]
                for i in circuit:
                    circuit_default[i[0]]=i[1]
                y_default=solution_choisie[Presence_pdi_key]
                s_default=solution_choisie[Start_pdi_key]
                solve_time_default=0


            modele4(
                        nom_instance=nom_instance
                        ,solver_verbose=niveau_verbose
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
                        ,solution_inter=solution_inter and instance_custom is  None
                        ,timeout_sol_inter=timeout_sol_inter
                        ,tranche_temps=Tranche_temps
                        ,Max_visite_pdi=Max_visite_pdi
                        ,Min_visite_pdi=Min_visite_pdi
                        ,solution_custom=solution_custom and instance_custom is  None
                        ,pdi_mandatory=pdi_mandatory
                        ,circuit_default=circuit_default
                        ,y_default=y_default
                        ,s_default=s_default
                        ,solve_time_default=solve_time_default
                        ,desactive_contrainte=[]
                        ,preference_utilisateur=preference_util_data
                        ,preference_recherche=preference_recherche
                        ,type_objectif_inter_solution=type_objectif_inter_solution
                    )
                    #a faire 
                    #faire en sorte de passer les donnée preference utilisateur sur les feuille de la matrice des chemin
                    #crée une fonction objectif qui ce focus sur maximiser la somme du coup des chemins

#nom du répertoire ou sont les instances
def modele4(nom_instance
            ,solver_verbose
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
            ,Max_visite_pdi
            ,Min_visite_pdi
            ,solution_custom
            ,preference_recherche
            ,preference_utilisateur
            ,type_objectif_inter_solution
            #sert a force certaine valeur du circuit après notament une première pré-solution
            ,circuit_forcer=None
            ,pdi_mandatory=[]

            #ces variable serve a verifier les résultat de mon algo personalisé
            ,y_default=None
            ,s_default=None
            ,circuit_default=None
            ,solve_time_default=None
            ,status_fin_recherche_default=None
            ,desactive_contrainte=[]
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
    if solution_inter:
        desactive_contrainte.append(1)
        desactive_contrainte.append(3)
        desactive_contrainte.append(13)

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
    circuit=None
    if circuit_forcer is None:
        if circuit_default is not None:
            circuit = VarArray(size=N,dom=lambda i: {circuit_default[i] })
        else:
            circuit = VarArray(size=N, dom=lambda i: {j for j in parcours_pdi if chemin_valuer[i][j]!=0 or i==j })
    else:
        circuit = VarArray(size=N,dom=lambda i: {circuit_forcer[i] })


    #distance entre tout les point d'intérêt
    distance = {(i, j): round(np.hypot(loc_x[i]-loc_x[j], loc_y[i]-loc_y[j])) for i in parcours_pdi for j in parcours_pdi }
    #variable qui contient les même valeur que distance ça sert juste pour acceder a ses valeur avec le systeme de suscesseur de circuit 
    distance_var=VarArray(size=[N, N], dom=lambda i, j: {distance[i,j]}  )
    #pareille mais pour les chemin 
    chemin_valuer_var=VarArray(size=[N, N], dom=lambda i, j: {chemin_valuer[i][j]}  )
    #pareille pour les score des pdi
    score_pdi_var=VarArray(size=N, dom=lambda i: {score_pdi[i]}  )
    #tableau ayant pour donnée les heure de depart de chaque viste de chaque point d'intérêt
    s=None
    #temps maximum autoriser
    Temps_max_tranche=int((Temps_max_visite+1)/tranche_temps)+1
    if circuit_forcer is None:
        if s_default is not None:
            s = VarArray(size=N,dom=lambda i: {s_default[i] })
        else:    
            s = VarArray(size=N,dom=range(0,Temps_max_tranche))
    else:
        s = VarArray(size=N,dom=lambda i:range(0,Temps_max_tranche)if circuit_forcer[i]!=i else {Temps_max_tranche-1})
        
    #tableau permettant de savoir si un point d'interêt est visité 
    y=None
    if circuit_forcer is None:
        if y_default is not None:
            y = VarArray(size=N,dom=lambda i: {y_default[i] })
        else:
            y = VarArray(size=N, dom={0,1})
    else:
        y=VarArray(size=N, dom=lambda i:{0,1}if circuit_forcer[i]!=i else {0} )

    




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
        valeur_ajout=budget_max
        depense_max_categorie[i]=valeur_ajout

    """
    Pour les explications des contraintes voir le rapport 
    """
    """
    Contrainte 1
    """
    
    #satisfy( disjunction(((s[i]*tranche_temps)+(t[i]*y[i])+distance[i,j]<=(s[j]*tranche_temps)) ,s[j]==Minimum(s), (x[i][j]==0))  for i in parcours_pdi for j in parcours_pdi if i!=j )
    if  1 not in desactive_contrainte:
        print("contrainte 1 use")    
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
    if  2 not in desactive_contrainte:
        print("contrainte 2 use")
        satisfy(Sum(b[i]*y[i] for i in parcours_pdi)<=budget_max)

    """
    Contrainte 3
    """
    if  3 not in desactive_contrainte:
        print("contrainte 3 use")  
        satisfy((s[i]*tranche_temps) >= (e[i]*y[i]) for i in parcours_pdi)
        satisfy((((s[i]*tranche_temps)+t[i])*y[i]) <= c[i] for i in parcours_pdi)
    
    """
    Contrainte 4
    """
    if  4 not in desactive_contrainte:
        print("contrainte 4 use")
        satisfy((capacite[i] * y[i]) <=capacite_max for i in parcours_pdi)

    """
    Contrainte 5
    """
    if  5 not in desactive_contrainte:
        print("contrainte 5 use")
        satisfy(Sum(t[i]*y[i] for i in parcours_pdi)<=Temps_max_visite)

    """
    Contrainte 7
    """
    if  7 not in desactive_contrainte:
        print("contrainte 7 use")
        satisfy(Sum(b[i]*y[i]*(categorie[i]==j) for i in parcours_pdi)<=depense_max_categorie[j] for j in categorie_df)

    """
    Contrainte 8
    """
    if  8 not in desactive_contrainte:
        print("contrainte 8 use")
        satisfy(Sum((circuit[i]!=i)*distance_var[i][circuit[i]]  for i in parcours_pdi  )>d_min )
        satisfy(Sum((circuit[i]!=i)*distance_var[i][circuit[i]]  for i in parcours_pdi  )<d_max )
    
    """
    Contrainte 9
    """
    if  9 not in desactive_contrainte:
        print("contrainte 9 use")
        satisfy(Sum(y[i] for i in parcours_pdi)>Min_visite_pdi-1)
        satisfy(Sum(y[i] for i in parcours_pdi)<Max_visite_pdi+1)
    
    """
    Contrainte 10
    """

    #point d'intéret a visiter au minimum
    #pour instacia14
    #mandatory=[7,2]
    if  10 not in desactive_contrainte:
        print("contrainte 10 use")
        satisfy(y[i]==1 for i in pdi_mandatory)

    """
    Contrainte 11
    """
    if  11 not in desactive_contrainte:
        print("contrainte 11 use")
        satisfy( disjunction(y[i]==0,circuit[i]!=i) for i in parcours_pdi )
    """
    Contrainte 12
    """
    if  12 not in desactive_contrainte:
        print("contrainte 12 use")
        satisfy(Circuit(circuit))

    """
    Contrainte 13
    """
    if  13 not in desactive_contrainte:
        print("contrainte 13 use")
        #satisfy(AllDifferent(s,excepting=Temps_max_tranche-1 if tranche_temps!=1 else Temps_max_visite-1))
        satisfy( disjunction(s[i]!=s[j],disjunction(circuit[i]==i,circuit[j]==j)) for i in parcours_pdi for j in parcours_pdi if i!=j)
   
    """
    Contrainte 14
    """
    if  14 not in desactive_contrainte:
        print("contrainte 14 use")
        
        satisfy(Knapsack(y, weights=[1 for i in parcours_pdi],wcondition=ge(Min_visite_pdi), profits=score_pdi)>=0)
    """
    Fonction objectif
    """
    #fonction objectif qui maximise la satisfaction utilisateur.ice
    objectif=type_objectif
    if(solution_inter):
        objectif=type_objectif_inter_solution

    
    if(objectif):    
        if(objectif==Maximise_score_pdi):
            maximize(Sum(y[i]*score_pdi[i] for i in parcours_pdi))
        if(objectif==Mix_distance_score_pdi):
            maximize(Sum(y[i]*score_pdi[i] for i in parcours_pdi))
            minimize((Sum((circuit[i]!=i)*distance_var[i][circuit[i]] for i in parcours_pdi)))
        if(objectif==Maximise_score_chemin):
            maximize(Sum((circuit[i]!=i)*(chemin_valuer_var[i][circuit[i]]+(score_pdi[i]+score_pdi_var[circuit[i]])) for i in parcours_pdi))
        if(objectif==Maximise_chemin_pdi):
            maximize(Sum(((circuit[i]!=i)*(chemin_valuer_var[i][circuit[i]]))+(score_pdi[i]*y[i]) for i in parcours_pdi))    
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

    #temps de résolution en seconde
    solve_time=fin_solve-debut_solve

    if solve_time_default is not None:
        solve_time=solve_time_default
    p_recherche=None
    circuit_forcer=None
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
            circuit_forcer=values(circuit,sol=numero_solution)
            
            tab_res.append({Presence_pdi_key:pdi_present,Start_pdi_key:start_pdi,Circuit_key:circuit_res})
    


    else:
        print(f"il n'y a pas de solutions pour l'instance {nom_instance}")
    #objet qui contient toutes les donnée sur la recherche
    
    if status_fin_recherche_default is not None:
        resultat_recherche=status_fin_recherche_default
    
    data={
            Status_key:
                    {
                        Fin_recherche_key:resultat_recherche.__str__()
                        ,Optimum_key:resultat_recherche is OPTIMUM
                    }
            ,Bound_key:boundmax
            ,solve_time_key:solve_time
            ,preference_recherche_key:preference_recherche
            ,preference_utilisateur_key:preference_utilisateur
            
            ,Distance_max_key:d_max
            ,Distance_min_key:d_min
            ,Max_visite_pdi_key:Max_visite_pdi
            ,Min_visite_pdi_key:Min_visite_pdi
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

    if solution_inter and p_recherche != None and not solution_custom:
        modele4(nom_instance=nom_instance
                ,solver_verbose=solver_verbose
                ,budget_max=budget_max
                ,capacite_max=capacite_max
                ,capaciter_pdi=capaciter_pdi
                ,categorie_pdi=categorie_pdi
                ,categorie_permise=categorie_permise
                ,chemin_valuer=chemin_valuer
                ,coord_x=coord_x
                ,coord_y=coord_y
                ,distance_parcourue_max=distance_parcourue_max
                ,distance_parcourue_min=distance_parcourue_min
                ,duree_visite=duree_visite
                ,extension_instance=extension_instance
                ,fermeture_pdi=fermeture_pdi
                ,fonction_objectif=fonction_objectif
                ,interet_pdi=interet_pdi
                ,nombre_solution=nombre_solution
                ,ouverture_pdi=ouverture_pdi
                ,prix_entrer=prix_entrer
                ,repertoire_solution=repertoire_solution
                ,solution_inter=False
                ,solver=solver
                ,type_objectif_inter_solution=type_objectif_inter_solution
                ,Temps_max_visite=Temps_max_visite
                ,timeout_activer=timeout_activer
                ,timeout_solver=timeout_solver+abs(timeout_sol_inter-(fin_solve-debut_solve))
                ,type_objectif=type_objectif
                ,timeout_sol_inter=timeout_sol_inter
                ,tranche_temps=tranche_temps
                ,Max_visite_pdi=Max_visite_pdi
                ,Min_visite_pdi=Min_visite_pdi
                ,solution_custom=solution_custom
                ,circuit_forcer=circuit_forcer
                ,pdi_mandatory=pdi_mandatory
                ,preference_recherche=preference_recherche
                ,preference_utilisateur=preference_utilisateur)
    
    if solution_custom and p_recherche != None and solution_inter:
        print(resultat_recherche)
        i=len(tab_res)-1
        tranche_temps=1
        solution_custom_res=False
        while(not solution_custom_res and i>=0):
            resultat_custom=algo_custom_solution(nom_instance=nom_instance
                ,solver_verbose=solver_verbose
                ,budget_max=budget_max
                ,capacite_max=capacite_max
                ,capaciter_pdi=capaciter_pdi
                ,categorie_pdi=categorie_pdi
                ,categorie_permise=categorie_permise
                ,chemin_valuer=chemin_valuer
                ,coord_x=coord_x
                ,coord_y=coord_y
                ,distance_parcourue_max=distance_parcourue_max
                ,distance_parcourue_min=distance_parcourue_min
                ,duree_visite=duree_visite
                ,extension_instance=extension_instance
                ,fermeture_pdi=fermeture_pdi
                ,fonction_objectif=fonction_objectif
                ,interet_pdi=interet_pdi
                ,nombre_solution=nombre_solution
                ,ouverture_pdi=ouverture_pdi
                ,prix_entrer=prix_entrer
                ,repertoire_solution=repertoire_solution
                ,solution_inter=False
                ,solver=solver
                ,Temps_max_visite=Temps_max_visite
                ,timeout_activer=timeout_activer
                ,timeout_solver=timeout_solver+abs(timeout_sol_inter-(fin_solve-debut_solve))
                ,type_objectif=type_objectif
                ,timeout_sol_inter=timeout_sol_inter
                ,tranche_temps=tranche_temps
                ,Max_visite_pdi=Max_visite_pdi
                ,Min_visite_pdi=Min_visite_pdi
                ,circuit_fixer=tab_res[i][Circuit_key]
                ,boundmax=boundmax
                ,pdi_mandatory=pdi_mandatory
                ,resultat_recherche_csp=resultat_recherche
                ,instance_repertory=instance_repertory)
            
            if resultat_custom is not None:
                modele4(nom_instance=nom_instance
                ,solver_verbose=solver_verbose
                ,budget_max=budget_max
                ,type_objectif_inter_solution=type_objectif_inter_solution
                ,capacite_max=capacite_max
                ,capaciter_pdi=capaciter_pdi
                ,categorie_pdi=categorie_pdi
                ,categorie_permise=categorie_permise
                ,chemin_valuer=chemin_valuer
                ,coord_x=coord_x
                ,coord_y=coord_y
                ,distance_parcourue_max=distance_parcourue_max
                ,distance_parcourue_min=distance_parcourue_min
                ,duree_visite=duree_visite
                ,extension_instance=extension_instance
                ,fermeture_pdi=fermeture_pdi
                ,fonction_objectif=fonction_objectif
                ,interet_pdi=interet_pdi
                ,nombre_solution=nombre_solution
                ,ouverture_pdi=ouverture_pdi
                ,prix_entrer=prix_entrer
                ,repertoire_solution=repertoire_solution
                ,solution_inter=False
                ,solver=solver
                ,Temps_max_visite=Temps_max_visite
                ,timeout_activer=False
                ,timeout_solver=timeout_solver+abs(timeout_sol_inter-(fin_solve-debut_solve))
                ,type_objectif=type_objectif
                ,timeout_sol_inter=timeout_sol_inter
                ,tranche_temps=tranche_temps
                ,Max_visite_pdi=Max_visite_pdi
                ,Min_visite_pdi=Min_visite_pdi
                ,solution_custom=True
                ,pdi_mandatory=pdi_mandatory
                ,circuit_default=resultat_custom[0]
                ,y_default=resultat_custom[1]
                ,s_default=resultat_custom[2]
                ,solve_time_default=resultat_custom[3]+solve_time
                ,status_fin_recherche_default=resultat_custom[4]
                ,desactive_contrainte=[]
                ,preference_recherche=preference_recherche
                ,preference_utilisateur=preference_utilisateur)
                solution_custom_res=True
            i-=1


if __name__ == "__main__":

    #permet de remetre le dossier d'execution du script ou est le script 
    os.chdir(os.path.dirname(__file__))

    #dossier ou sont stocker les settings json
    dossier_settings_json="settings_recherche"

    #fichier choisie pour aller chercher les settings json
    fichier_settings_json="settings_default.json"

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
    
    parser.add_argument(f"--{settings_choosing[key_short_arg]}", type=str,default=None,
                help='choosing where the settings for the search is')
    parser.add_argument(f"--{solution_custom_reex[key_short_arg]}", type=str,default=None,
                help='sert a réexecuter un solution custom')
        
    args = parser.parse_known_args()
    if(args[0].s is not None):
        fichier_settings_json=args[0].s
    
    



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

        #solution qui utilise un algo custom pour affecter les visite des pdi
        solution_custom=settings[solution_algo_custom_key]
        type_objectif_inter_solution=settings[type_objectif_inter_solution]

        if args[0].f is not None:
            #fichier que j'ai passer en paramètre de mon programme
            file_a_traiter=args[0].f
        if args[0].t is not None:
            num_thread=int(args[0].t)
        if  args[0].i is not None:
            decalage_thread=int(args[0].i)
        nom_fichier_iter=None
        if(args[0].c is not None):
            nom_fichier_iter=args[0].c
            print(args[0].c)
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
                        ,solution_custom=solution_custom
                        ,nom_fichier_custom=nom_fichier_iter
                        ,preference_recherche=settings
                        ,type_objectif_inter_solution=type_objectif_inter_solution
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
                        ,solution_custom=solution_custom
                        ,preference_recherche=settings
                        ,type_objectif_inter_solution=type_objectif_inter_solution
                    )
                instance_traiter+=num_thread
                nombre_instance_traiter+=1
            print(f"fin du traitement du process {decalage_thread}")
    
