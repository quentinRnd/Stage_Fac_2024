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
            
            representation_solution_repertoire="representation"
            nom_dossier_repre=f"{representation_solution_repertoire}/repre_{nom_fichier}"
            shutil.rmtree(nom_dossier_repre,ignore_errors=True)
            os.makedirs(nom_dossier_repre)
            
            #tableau contenant mes solutions


            g = Network(height="1000px", width="100%", bgcolor="white", font_color="black",directed =True)
            
            
            
            
            g.add_nodes([i  for i in range(len(solution[X_PDI_key]))],
                     
                     x=[i*10 for i in solution[X_PDI_key]],
                     y=[i*10 for i in solution[Y_PDI_key]],
                     label=[f"PDI : {i}"  for i in range(len(solution[X_PDI_key]))],
                    )
            nom_graphe=f"{nom_dossier_repre}/visualisation_isntance_{nom_fichier}.html"
            #g.generate_html(name=f"{nom_dossier_repre}/visualisation_{nom_fichier}.html")
            g.toggle_physics(False)
            g.save_graph(nom_graphe)

    def affiche_fichier(repertoire_fichier,nom_fichier):
        #print(f"display {repertoire_fichier}/{nom_fichier}")
        with open(f"{repertoire_fichier}/{nom_fichier}.json") as solution_json:
            repertoire_instance="Instance_json"

            solution = json.load(solution_json)
            
            representation_solution_repertoire="representation"
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
            Solutions_choisi=[Solutions[len(Solutions)-1]]
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
                        color[i]='#00ff1e'
                    if soluce[Start_pdi_key][i]==depart:
                        color[i]='#dd4b39'
                    if not soluce[Presence_pdi_key][i]:
                        color[i]='#FFFFFF'
                    if max(soluce[Arc_key][i])==1 and not soluce[Presence_pdi_key][i]:
                        color[i]='f40fff'
                
                
                
                g.add_nodes([i  for i in range(len(soluce[Presence_pdi_key]))],
                         title=[f"""
                                    temps de départ : {soluce[Start_pdi_key][i]}
                                    Intéressement : {solution[Score_pdi_key][i]}
                                """ 
                                    for i in range(len(soluce[Presence_pdi_key]))],
                         x=[i*10 for i in solution[Coordonee_pdi_x_key]],
                         y=[i*10 for i in solution[Coordonee_pdi_y_key]],
                         label=[f"PDI : {i}"  for i in range(len(soluce[Presence_pdi_key]))],
                         color=  color
                        )
                
                for i in range(len(soluce[Arc_key])):
                    for j in range(len(soluce[Arc_key])):
                        if(soluce[Arc_key][i][j]==1):
                            g.add_edge(i,j,title="" if  chemin[i][j]==[0] else f"""
                                nature : {chemin[i][j][0]}
                                ville : {chemin[i][j][1]}
                                élévation : {chemin[i][j][2]}
                                forêt : {chemin[i][j][3]}
                                lac : {chemin[i][j][4]}
                                rivière : {chemin[i][j][5]}
                            """
                            )

                nom_graphe=f"{nom_dossier_repre}/visualisation_{nom_fichier}_solution_{num_sol}.html"
                #g.generate_html(name=f"{nom_dossier_repre}/visualisation_{nom_fichier}.html")
                g.toggle_physics(False)
                g.save_graph(nom_graphe)
                num_sol+=1


        

dossier_solution="Instance_json"
pattern=r'\w+'

fichiers=os.listdir(dossier_solution)
fichiers=[re.findall(pattern, i)[0] for i in fichiers]

for fichier in fichiers:
    affiche_solution.affiche_instance(dossier_solution,fichier)
