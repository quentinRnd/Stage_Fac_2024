import random
import json
from settings import * 
from utils import creation_repertoire
import os
import re

def calcul_densiter_graphe(graphe=None,nom_fichier=None,nom_repertoire_instance=None):
    if nom_fichier is not None and nom_repertoire_instance is not None:
        with open(f"{nom_repertoire_instance}/{nom_fichier}.json") as solution_json:
            graphe = json.load(solution_json)
    chemin=graphe[Categorie_chemin_pdi_key]
    densiter=0
    for i in range(len(chemin)):
        densiter+=sum([1 for j in range(len(chemin[i])) if chemin[i][j]!=None])
    densiter/=(len(chemin)**2)
    return densiter
def calcul_taille_graphe(graphe):
    return len(graphe[Categorie_chemin_pdi_key])
def gestion_densiter_graphe(densiter_rechercher,repertoire_fichier=None,nom_fichier=None,graphe_default=None):
    graphe=graphe_default
    if graphe_default is None:
        with open(f"{repertoire_fichier}/{nom_fichier}.json") as solution_json:
            graphe = json.load(solution_json)
    taille_graphe=calcul_taille_graphe(graphe)
    chemin=graphe[Categorie_chemin_pdi_key]
    #densiter du graphe 
    densiter_graphe=calcul_densiter_graphe(graphe=graphe)
    #nombre d'arc rechercher dans le 
    nombre_arc_rechercher=(taille_graphe**2)*densiter_rechercher
    nombre_arc_rajout=(taille_graphe**2)*densiter_graphe
    if(nombre_arc_rajout<nombre_arc_rechercher):
        chemin_vide=[[i,j] for i in range(taille_graphe)for j in range(taille_graphe)  if chemin[i][j]==None]
        changement=random.sample(chemin_vide,int(nombre_arc_rechercher-nombre_arc_rajout))
        chemin_disponible=[
            #des chemin plutot de entre ville et nature
            [0.3,0.8,0.1,0,0,0.6]
            # des chemin plutot de grande nature
            ,[1,0,0.3,0.8,0.5,0.8]
            #des chemin de ville
            ,[0,1,0.5,0,0,0]
            #des chemin pres de rivière et de lacs
            ,[1,0,0.4,1,1,1]
            #des chemin de ville avec des lacs
            ,[0.2,1,0.3,0,1,0.3]
            #avec de l'élevation en ville
            ,[0.2,1,0.8,0,1,0.3]
            #avec de l'élevation en nature
            ,[1,0,0.8,0.4,0.6,0.6]
            #chemin de nature dans la forêt avec certain lac et rivière
            ,[1,0,0.3,1,0.5,0.8]
        ]
        changement=[[i,chemin_disponible[random.randint(0,len(chemin_disponible)-1)]]for i in changement]
        for i in changement:
            chemin[i[0][0]][i[0][1]]=i[1]
        graphe[Categorie_chemin_pdi_key]=chemin
    else:
        chemin_valuer=[[i,j] for i in range(taille_graphe)for j in range(taille_graphe)  if chemin[i][j]!=None]
        changement=random.sample(chemin_valuer,int(nombre_arc_rajout-nombre_arc_rechercher))
        for i in changement:
            chemin[i[0]][i[1]]=None
        
        graphe[Categorie_chemin_pdi_key]=chemin
    return graphe

"""
repertoire_instance="Instance_json"
repertoire_instance_destination="Instance_json_densiter_0_7"
#recupere toute les instance du dossier des instances
instances=os.listdir(repertoire_instance)
pattern=r'\w+'
#permet de récuperer uniquement les nom des fichier 
instances=sorted([re.findall(pattern, i)[0] for i in instances])
creation_repertoire(repertoire_instance_destination)

densiter_rechercher=0.7

for instance in instances:
    instance_final=gestion_densiter_graphe(repertoire_fichier=repertoire_instance,nom_fichier=instance,densiter_rechercher=densiter_rechercher)
    fichier = open(f"{repertoire_instance_destination}/{instance}.json", "w")
    json_data=json.dumps(instance_final, indent=3)
    
    fichier.write(json_data)
    fichier.close()

print(calcul_densiter_graphe(nom_fichier="Instancia1",nom_repertoire_instance=repertoire_instance_destination))

"""