import os
import json
import shutil
import pydot

from settings import *

from pyvis.network import Network

class affiche_solution:
    def affiche_fichier(repertoire_fichier,nom_fichier):
        with open(f"{repertoire_fichier}/{nom_fichier}.json") as solution_json:
            
            solution = json.load(solution_json)
            
            representation_solution_repertoire="representation"
            nom_dossier_repre=f"{representation_solution_repertoire}/repre_{nom_fichier}"
            shutil.rmtree(nom_dossier_repre,ignore_errors=True)
            os.makedirs(nom_dossier_repre)
            Status=solution[Status_key]
            
            #tableau contenant mes solutions
            Solutions=solution[Solutions_key]
            if(len(Solutions)<=0):
                return 

            num_sol=0
            Solutions_choisi=[Solutions[len(Solutions)-1]]
            for soluce in Solutions_choisi:
                g = Network(height="1000px", width="100%", bgcolor="white", font_color="black")
                color=[ '#27a9ea' for i in range(len(soluce[Presence_pdi_key]))]
                #temps d'arriver au dernier pdi
                arriver=max(soluce[Start_pdi_key])
                #temps d'arriver au premier pdi
                depart=soluce[Start_pdi_key][0]
                for i in soluce[Start_pdi_key]:
                    if i!=-1 and i<depart:
                        depart=i
                for i in range(len(soluce[Start_pdi_key])):
                    if soluce[Start_pdi_key][i]==arriver:
                        color[i]='#00ff1e'
                    if soluce[Start_pdi_key][i]==depart:
                        color[i]='#dd4b39'
                    if not soluce[Presence_pdi_key][i]:
                        color[i]='#FFFFFF'
                    
                
                
                g.add_nodes([i  for i in range(len(soluce[Presence_pdi_key]))],
                         title=[f"temps de départ : {soluce[Start_pdi_key][i]}" for i in range(len(soluce[Presence_pdi_key]))],
                         x=[i*10 for i in solution[Coordonee_pdi_x_key]],
                         y=[i*10 for i in solution[Coordonee_pdi_y_key]],
                         label=[f"PDI : {i}"  for i in range(len(soluce[Presence_pdi_key]))],
                         color=  color
                        )
                for i in range(len(soluce[Arc_key])):
                    for j in range(len(soluce[Arc_key])):
                        if(soluce[Arc_key][i][j]==1):
                            g.add_edge(i,j)

                nom_graphe=f"{nom_dossier_repre}/visualisation_{nom_fichier}_solution_{num_sol}.html"
                #g.generate_html(name=f"{nom_dossier_repre}/visualisation_{nom_fichier}.html")
                g.toggle_physics(False)
                g.save_graph(nom_graphe)
                num_sol+=1


        
affiche_solution.affiche_fichier("solution_test","Instanciamoyenne")