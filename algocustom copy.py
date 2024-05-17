import numpy as np
from pycsp3 import SAT,UNSAT,OPTIMUM
from settings import *
import json

import time

from utils import *
import datetime

#le vecteur est binaire et je vais faire ++ sur celui-ci
def plus_un(vecteur):
    i=0
    while(i<len(vecteur)and vecteur[i]==1  ):
        vecteur[i]=0
        i+=1
    if i<len(vecteur):
        vecteur[i]=1
    else:
        vecteur=None
    return vecteur

#calcul le nombre de un dans le vecteur
def nombre_un(vecteur):
    return sum(vecteur)

# cette fonction sert a affecter les visites des pdi  
#cette fonction ne modifie pas le chemin pré généré il va juste calculer les y
def algo_custom_solution(nom_instance
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
            ,Max_visite_pdi
            ,Min_visite_pdi
            ,circuit_fixer
            ,boundmax
            ,pdi_mandatory
            ,resultat_recherche_csp):
    start_solve=int(time.time())
    print("start of the solve with custom algorithm ",datetime.datetime.now())
    #nombre de pdi que l'on veux visiter
    nombre_visite_pdi=Min_visite_pdi
    tranche_temps=1
    #point d'interet classer en fonction de leur intérêt
    pdi_classer= [circuit_fixer[i][0] for i in range(len(circuit_fixer))]

    pdi_classer=sorted(pdi_classer,key=lambda i:-interet_pdi[i])
    
    circuit_fixer_aux=[]

    depart=circuit_fixer[0][0]

    for i in range(len(circuit_fixer)):
        aux=None
        for i in range(len(circuit_fixer)):
            if(circuit_fixer[i][0]==depart):
                aux=circuit_fixer[i]
        circuit_fixer_aux.append(aux)
        depart=aux[1]
    circuit_fixer=circuit_fixer_aux

    #vecteur qui contient les point d'interet qui sont dans le chemin
    vecteur_directeur=[0 for i in range(len(pdi_classer))]
    
    parcours_pdi=range(len(coord_x))
    
    #distance entre tout les point d'intérêt
    distance = {(i, j): round(np.hypot(coord_x[i]-coord_x[j], coord_y[i]-coord_y[j])) for i in parcours_pdi for j in parcours_pdi }

    solution=False
    pdi_selectionner=None

    while(vecteur_directeur!=None and not solution):
        
        if( sum(vecteur_directeur)<nombre_visite_pdi or sum(vecteur_directeur)>Max_visite_pdi ):
            vecteur_directeur=plus_un(vecteur_directeur)
            
        else:
            fin_recherche=False
            pdi_selectionner=[pdi_classer[i] for i in range(len(pdi_classer)) if vecteur_directeur[i]==1]
            somme_visite=sum([duree_visite[i] for i in pdi_selectionner])
            start_pdi=[Temps_max_visite-1 for i in coord_x]
            offset_pdi=0
            somme_prix_pdi=sum([prix_entrer[i] for i in pdi_selectionner])
            
            mandatory_correct=True
            for i in pdi_mandatory:
                if vecteur_directeur[i]!=1:
                    mandatory_correct=False


            while(not fin_recherche and not solution and somme_visite<Temps_max_visite and somme_prix_pdi<budget_max and mandatory_correct):
                
                i=offset_pdi
                pdi_depart=circuit_fixer[i][0]
                
                pas_solution=False

                if pdi_depart in pdi_selectionner:
                    start_pdi[pdi_depart]=ouverture_pdi[pdi_depart]
                    if  start_pdi[pdi_depart] <Temps_max_visite:
                        if pdi_depart in pdi_selectionner and  start_pdi[pdi_depart] < ouverture_pdi[pdi_depart]:
                            start_pdi[pdi_depart]=ouverture_pdi[pdi_depart]+1
                        if pdi_depart in pdi_selectionner and start_pdi[pdi_depart]+duree_visite[pdi_depart] > fermeture_pdi[pdi_depart]:
                            pas_solution=True
                    else:
                        pas_solution=True

                else:
                    start_pdi[pdi_depart]=0
                
                

                j=0
                while j in range(len(circuit_fixer)-1) and not pas_solution:
                    j+=1 
                    pdi_depart=circuit_fixer[i][0]
                    pdi_arriver=circuit_fixer[i][1]

                    start_pdi[pdi_arriver]=start_pdi[pdi_depart]+distance[pdi_depart,pdi_arriver]+(duree_visite[pdi_depart]if pdi_depart in pdi_selectionner else 0)
                    
                    if  start_pdi[pdi_arriver] <Temps_max_visite:
                        if pdi_arriver in pdi_selectionner and  start_pdi[pdi_arriver] < ouverture_pdi[pdi_arriver]:
                            start_pdi[pdi_arriver]=ouverture_pdi[pdi_arriver]+1
                        if pdi_arriver in pdi_selectionner and start_pdi[pdi_arriver]+duree_visite[pdi_arriver] > fermeture_pdi[pdi_arriver]:
                            pas_solution=True
                    else:
                        pas_solution=True
                    i+=1
                    i=i%len(circuit_fixer)
                
                if pas_solution:
                    offset_pdi+=1
                    if offset_pdi>=len(circuit_fixer):
                        fin_recherche=True
                else:
                    solution=True
                    
            vecteur_directeur=plus_un(vecteur_directeur)
    end_solve= int(time.time())
    resultat_recherche_inter=UNSAT
    tab_res=[]
    retour=None
    duree_solve=end_solve-start_solve
    if solution:
        resultat_recherche=resultat_recherche_csp
        y=[ 1  if i in pdi_selectionner else 0 for i in parcours_pdi]
        tab_res.append({Presence_pdi_key:y,Start_pdi_key:start_pdi,Circuit_key:circuit_fixer}) 
        

        

        circuit=[i for i in parcours_pdi]

        for i in circuit_fixer:
            circuit[i[0]]=i[1]

        print("found solution custom")
        retour= circuit,y,start_pdi,duree_solve,resultat_recherche
    
    
    data={
            Status_key:
                    {
                        Fin_recherche_key:resultat_recherche_csp.__str__()
                        ,Optimum_key:resultat_recherche_csp is OPTIMUM
                    }
            ,Bound_key:boundmax
            ,Distance_max_key:distance_parcourue_max
            ,Distance_min_key:distance_parcourue_min
            ,Tranche_temps_key: tranche_temps
            ,Type_objectif_key:type_objectif
            ,Timeout_solver_key:timeout_solver
            ,Timeout_activer_key:timeout_activer
            ,Solutions_key:tab_res
            ,Coordonee_pdi_x_key:coord_x
            ,Coordonee_pdi_y_key:coord_y
            ,Temps_visite_key:duree_visite
            ,Score_pdi_key:interet_pdi
            ,Closing_pdi_key:fermeture_pdi
            ,Opening_pdi_key:ouverture_pdi
            ,Evaluation_path_key:chemin_valuer
        }
    json_data=json.dumps(data, indent=3)

    repertoire_custom=f"{repertoire_solution}/custom_sol"

    creation_repertoire(repertoire_custom)
    nom_fichier=f"{repertoire_custom}/{nom_instance}.json"
    fichier = open(nom_fichier, "w")

    fichier.write(json_data)    
    print(f"solution saved in {nom_fichier}")
    print(f"nombre solution {len(tab_res)}")
    print("time to solve this instance ",duree_solve)
    
    
    return retour
    
