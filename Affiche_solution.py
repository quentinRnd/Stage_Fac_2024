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
            nom_dossier_repre=f"repre_{nom_fichier}"
            shutil.rmtree(nom_dossier_repre,ignore_errors=True)
            os.makedirs(nom_dossier_repre)
            Status=solution[Status_key]
            #tableau contenant mes solutions
            Solutions=solution[Solutions_key]

            num_sol=0
            for soluce in Solutions:
                g = Network(height="1000px", width="100%", bgcolor="white", font_color="black")
                g.add_nodes([i  for i in range(len(soluce[Presence_pdi_key]))],
                         #title=['I am node 1', 'node 2 here', 'and im node 3'],
                         x=solution[Coordonee_pdi_x_key],
                         y=solution[Coordonee_pdi_y_key],
                         label=[f"PDI : {i}"  for i in range(len(soluce[Presence_pdi_key]))],
                         #color=['#00ff1e', '#162347', '#dd4b39']
                        )
                for i in range(len(soluce[Arc_key])):
                    for j in range(len(soluce[Arc_key])):
                        if(soluce[Arc_key][i][j]==1):
                            g.add_edge(i,j)

                nom_graphe=f"{nom_dossier_repre}/visualisation_{nom_fichier}_solution_{num_sol}.html"
                #g.generate_html(name=f"{nom_dossier_repre}/visualisation_{nom_fichier}.html")
                g.save_graph(nom_graphe)
                num_sol+=1
                exit(1)


        
affiche_solution.affiche_fichier("solution","solution_Instanciapetite")