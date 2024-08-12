import matplotlib.pyplot as plt
import matplotlib
import os 
import json
import re
from settings import *
from utils import creation_repertoire

import numpy as np

#fonction qui sert a extraire les entier des nom de fichier des instances
def tri(x):
    #on extrait les digit de la chaine de caractère
    temp = re.findall(r'\d+', x)
    res = list(map(int, temp))
    ret=0
    for i in range(len(res)):
        ret+=res[i]*(10**i)

    return ret

if __name__ == "__main__":
    #les deux chose a comparé
    choix1="model4_POI_chemin"
    choix2="model4_POI_chemin"
    
    
    
    #savoir si c'est le modele custom ou base que l'on compare
    type_model_choix1="base"
    type_model_choix2="custom"
    
    type_model="comparaison"

    #permet de savoir ou les solution sont prise dans le projet, ne pas mettre des /
    type_solution="modele4_sol"


    data=[f"solution/{type_solution}/{choix1}/{type_model_choix1}/",f"solution/{type_solution}/{choix2}/{type_model_choix2}/"]

    rep_graphe=f"graphe/difference_{type_solution}"
    nom_graphe=f"diff-{choix1}-{choix2}"

    instance_exclu=["Instanciamoyenne.json","Instanciapetite.json"]

    #variable qui va stocker les résultat des donnée
    scores_data=[]
    for rep in data:
        #récupere les instance dans le répertoire
        instances = [f for f in os.listdir(rep) if os.path.isfile(rep+f) and f not in instance_exclu]

        #pattern qui permet de supprimer les instances
        pattern=r'\w+'
        #permet de récuperer uniquement les noms des fichiers 
        instances=sorted([re.findall(pattern, i)[0] for i in instances],key=lambda x: tri(x))
        #tableau qui stockent les score avec le nom des instance associer
        score=[]
        for instance in instances:
            #ouverture des instances pour récuperer leur score final
            with open(f"{rep}/{instance}.json") as instance_bin:
                #objet json qui contient le resultat de ACE d'une recherche
                instance_data = json.load(instance_bin)
                #ajoute une entré au tableau de score local a rep
                score.append({"nom_instance":instance,"score":instance_data[Bound_key]})
        scores_data.append(score)
    ind_1=0
    ind_2=0
    difference_score=[]
    data_diff_1=scores_data[0]
    data_diff_2=scores_data[1]
    for i in range(max(len(data_diff_1),len(data_diff_2))):
        if(data_diff_1[ind_1]["nom_instance"]==data_diff_2[ind_2]["nom_instance"]):
            difference_score.append(
                                    {"nom_instance":data_diff_2[ind_2]["nom_instance"]
                                    ,"score":data_diff_2[ind_2]["score"]-data_diff_1[ind_1]["score"]
                                    }
                                    )
            ind_1+=1
            ind_2+=1
        else:
            if(tri(data_diff_1[ind_1]["nom_instance"])<tri(data_diff_2[ind_2]["nom_instance"])):
                ind_1+=1
            else:
                ind_2+=1
    

    nom_instance_diff=[]
    resultat_diff=[]
    for i in difference_score:
        numero_instance=tri(i["nom_instance"])
        nom_instance_diff.append(f"in{numero_instance}")
        resultat_diff.append(i["score"])


    rep_png=rep_graphe+f"/{type_model}/png"
    rep_svg=rep_graphe+f"/{type_model}/svg"
    creation_repertoire(rep_png)
    creation_repertoire(rep_svg)

    matplotlib.use('Agg')

    taille_figure=(8, 6)
    
    plt.figure(figsize=taille_figure)

    x = np.array(nom_instance_diff)
    y = np.array(resultat_diff)

    plt.plot(x, y)

    plt.xlabel("Nom instance")
    plt.ylabel("différence de Bound entre les instances")
    plt.axhline(y=0, color='r', linestyle='--')

    plt.savefig(rep_svg+"/"+nom_graphe+".svg")
    plt.savefig(rep_png+"/"+nom_graphe+".png")
    
