import os
import json
import shutil
import pydot
import re
from settings import *

from pyvis.network import Network

class affiche_solution:
    def affiche_instance(repertoire_instance,nom_fichier):
        with open(f"{repertoire_instance}/{nom_fichier}.json") as solution_json:

            solution = json.load(solution_json)
            
            representation_solution_repertoire="representation/instance"
            nom_dossier_repre=f"{representation_solution_repertoire}/repre_{nom_fichier}"
            shutil.rmtree(nom_dossier_repre,ignore_errors=True)
            os.makedirs(nom_dossier_repre)
            
            #tableau contenant mes solutions


            g = Network(height="1000px", width="100%", bgcolor="white", font_color="black",directed =True)
            
            
            
            
            g.add_nodes([i  for i in range(len(solution[X_PDI_key]))],
                     
                     x=[i*10 for i in solution[X_PDI_key]],
                     y=[i*10 for i in solution[Y_PDI_key]],
                     label=[f"PDI : {i}"  for i in range(len(solution[X_PDI_key]))],
                     title=[f"""
                    Score : {solution[Score_pdi_key][i]}
                    Temps visite : {solution[Temps_visite_key][i]}
                    Cout entrer : {solution[Cout_entrer_key][i]}
                    Heure ouverture : {solution[Heure_ouverture_key][i]}
                    Heure fermeture : {solution[Heure_fermeture_key][i]}
                    Categorie : {solution[Categorie_key][i]}
                    Capacitée : {solution[Capacite_key][i]}
                     """
                     for i in range(len(solution[X_PDI_key]))
                     ]
                    )
            for i in range(len(solution[Categorie_chemin_pdi_key])):
                    for j in range(len(solution[Categorie_chemin_pdi_key])):
                        if(solution[Categorie_chemin_pdi_key][i][j]!=None):
                            g.add_edge(i,j)
            nom_graphe=f"{nom_dossier_repre}/visualisation_instance_{nom_fichier}.html"
            #g.generate_html(name=f"{nom_dossier_repre}/visualisation_{nom_fichier}.html")
            g.toggle_physics(False)
            g.save_graph(nom_graphe)

    def affiche_fichier(repertoire_fichier,nom_fichier):
        #print(f"display {repertoire_fichier}/{nom_fichier}")
        with open(f"{repertoire_fichier}/{nom_fichier}.json") as solution_json:

            solution = json.load(solution_json)
            
            representation_solution_repertoire="representation/solution"
            nom_dossier_repre=f"{representation_solution_repertoire}/repre_{nom_fichier}"
            shutil.rmtree(nom_dossier_repre,ignore_errors=True)
            os.makedirs(nom_dossier_repre)
            Status=solution[Status_key]
            chemin=solution[Evaluation_path_key]
            
            #tableau contenant mes solutions
            Solutions=solution[Solutions_key]
            if(len(Solutions)<=0):
                return 

            num_sol=len(Solutions)-1
            Solutions_choisi=[Solutions[num_sol]]
            for soluce in Solutions_choisi:
                presence_pdi=soluce[Presence_pdi_key]
                g = Network(height="1000px", width="100%", bgcolor="white", font_color="black",directed =True)
                color=[ '#27a9ea' for i in range(len(soluce[Presence_pdi_key]))]
                #temps d'arriver au dernier pdi
                arriver=soluce[Start_pdi_key][0]
                #temps d'arriver au premier pdi
                depart=soluce[Start_pdi_key][0]
                for i in range(len(soluce[Start_pdi_key])):
                    if soluce[Start_pdi_key][i]<depart and (presence_pdi[i] or max(soluce[Arc_key][i])==1 or max(soluce[Arc_key][:][i])==1 ):
                        depart=soluce[Start_pdi_key][i]
                    if soluce[Start_pdi_key][i]>arriver and (presence_pdi[i] or max(soluce[Arc_key][i])==1 or max(soluce[Arc_key][:][i])==1 ):
                        arriver=soluce[Start_pdi_key][i]
                for i in range(len(soluce[Start_pdi_key])):
                    if soluce[Start_pdi_key][i]==arriver:
                        color[i]='#00FF1E'
                    else:
                        if soluce[Start_pdi_key][i]==depart and (presence_pdi[i] or max(soluce[Arc_key][i])==1):
                            color[i]='#DD4B39'
                        else:
                            if max(soluce[Arc_key][i])==1 and not soluce[Presence_pdi_key][i]:
                                color[i]='#FFFFFF'
                            else:
                                if soluce[Presence_pdi_key][i]:
                                    color[i]='#C0C0C0'
                
                facteur=10
                g.add_nodes([i  for i in range(len(soluce[Presence_pdi_key]))],
                         title=[f"""
                                    temps de départ : {soluce[Start_pdi_key][i]}
                                    Intéressement : {solution[Score_pdi_key][i]}
                                    Visité : {"oui" if soluce[Presence_pdi_key][i]==1 else "non"}
                                """ 
                                    for i in range(len(soluce[Presence_pdi_key]))],
                         x=[i*facteur for i in solution[Coordonee_pdi_x_key]],
                         y=[i*facteur for i in solution[Coordonee_pdi_y_key]],
                         label=[f"PDI : {i}"  for i in range(len(soluce[Presence_pdi_key]))],
                         color=  color
                         
                        )
                
                for i in range(len(soluce[Arc_key])):
                    for j in range(len(soluce[Arc_key])):
                        if(soluce[Arc_key][i][j]==1):
                            g.add_edge(i,j,title="" if  chemin[i][j]==[0] else f"score chemin : {chemin[i][j]}"
                            )

                nom_graphe=f"{nom_dossier_repre}/visualisation_{nom_fichier}_solution_{num_sol}.html"
                #g.generate_html(name=f"{nom_dossier_repre}/visualisation_{nom_fichier}.html")
                g.toggle_physics(False)
                g.save_graph(nom_graphe)
                num_sol+=1
    #affiche les soltion du modèle 4
    def affiche_solution_circuit(repertoire_fichier,nom_fichier):
        with open(f"{repertoire_fichier}/{nom_fichier}.json") as solution_json:

            solution = json.load(solution_json)
            
            intervale_temps=solution[Tranche_temps_key]

            representation_solution_repertoire="representation/solution"
            nom_dossier_repre=f"{representation_solution_repertoire}/repre_{nom_fichier}"
            shutil.rmtree(nom_dossier_repre,ignore_errors=True)
            os.makedirs(nom_dossier_repre)
            Status=solution[Status_key]
            chemin=solution[Evaluation_path_key]
            
            #tableau contenant mes solutions
            Solutions=solution[Solutions_key]
            if(len(Solutions)<=0):
                return 

            num_sol=len(Solutions)-1
            Solutions_choisi=[Solutions[num_sol]]
            for soluce in Solutions_choisi:
                circuit=soluce[Circuit_key]
                presence_pdi=soluce[Presence_pdi_key]
                g = Network(height="1000px", width="100%", bgcolor="white", font_color="black",directed =True)
                color=[ '#FFFFFF' for i in range(len(soluce[Presence_pdi_key]))]
                
                #temps d'arriver au dernier pdi
                arriver=circuit[0][0]
                #temps d'arriver au premier pdi
                depart=circuit[0][0]
                start_pdi=soluce[Start_pdi_key]
                circuit_aux=[i[0] for i in circuit]
                for k in circuit:
                    i=k[0]
                    if start_pdi[i]<start_pdi[depart]:
                        depart=i
                    if start_pdi[i]>start_pdi[arriver] :
                        arriver=i
                
                for i in  range(len(soluce[Start_pdi_key])):
                    if i in circuit_aux and not soluce[Presence_pdi_key][i]:
                        color[i]='#27a9ea'
                    else:
                        if soluce[Presence_pdi_key][i]:
                            color[i]='#C0C0C0'
                color[arriver]='#00FF1E'
                color[depart]='#DD4B39'
                facteur=10
                g.add_nodes([i  for i in range(len(soluce[Presence_pdi_key]))],
                         title=[f"""
                                    temps de départ : {soluce[Start_pdi_key][i]*intervale_temps}
                                    Intéressement : {solution[Score_pdi_key][i]}
                                    Visité : {"oui" if soluce[Presence_pdi_key][i]==1 else "non"}
                                """ 
                                    for i in range(len(soluce[Presence_pdi_key]))],
                         x=[i*facteur for i in solution[Coordonee_pdi_x_key]],
                         y=[i*facteur for i in solution[Coordonee_pdi_y_key]],
                         label=[f"PDI : {i}"  for i in range(len(soluce[Presence_pdi_key]))],
                         color=  color
                         
                        )
                
                for k in circuit:
                    i=k[0]
                    j=k[1]
                    g.add_edge(i,j,title="" if  chemin[i][j]==[0] else f"score chemin : {chemin[i][j]}")

                nom_graphe=f"{nom_dossier_repre}/visualisation_{nom_fichier}_solution_{num_sol}.html"
                #g.generate_html(name=f"{nom_dossier_repre}/visualisation_{nom_fichier}.html")
                g.toggle_physics(False)
                g.save_graph(nom_graphe)
                num_sol+=1


        

dossier_solution="solution/test_modele4"
pattern=r'\w+'

fichiers=os.listdir(dossier_solution)
fichiers=[fichier  for fichier in fichiers if os.path.isfile(f"{dossier_solution}/{fichier}")]
fichiers=[re.findall(pattern, i)[0] for i in fichiers]

for fichier in fichiers:
    affiche_solution.affiche_solution_circuit(dossier_solution,fichier)

dossier_instance="Instance_json"
pattern=r'\w+'

fichiers=os.listdir(dossier_instance)
fichiers=[re.findall(pattern, i)[0] for i in fichiers]

for fichier in fichiers:
    affiche_solution.affiche_instance(dossier_instance,fichier)