import pandas as pd

import os 
import re
import json


from settings import * 
from Chemin_ajout_instance import *


def traduction_instance():
    repertoire_csv="Instancias"
    extension_fichier_base=".csv"
    instances=os.listdir(repertoire_csv)
    repertoire_instance_json="Instance_json"


    if not os.path.exists(repertoire_instance_json): 
        os.makedirs(repertoire_instance_json) 

    pattern=r'\w+'
    #permet de récuperer uniquement les nom des fichier 
    instances=sorted([re.findall(pattern, i)[0] for i in instances])

    for instance in instances:
        fichier = open(f"{repertoire_instance_json}/{instance}.json", "w")
        csv=pd.read_csv(repertoire_csv+"/"+instance+extension_fichier_base,sep=";")
        data={
            X_PDI_key:[i for i in csv["X_k"]]
            ,Y_PDI_key:[i for i in csv["Y_k"]]
            ,Score_pdi_key:[i for i in csv["score_k"]]
            ,Temps_visite_key:[i for i in csv["duracion_k"]]
            ,Cout_entrer_key:[i for i in csv["entrada_k"]]
            ,Heure_ouverture_key:[i for i in csv["open_k"]]
            ,Heure_fermeture_key:[i for i in csv["close_k"]]
            ,Categorie_key:[i for i in csv["categoria"]]
            ,Capacite_key:[i for i in csv["capacidad"]]
            ,Categorie_chemin_pdi_key:[[None for j in range(len(csv["X_k"]))] for i in range(len(csv["X_k"]))]
        }
        json_data=json.dumps(data, indent=3)
        fichier.write(json_data)
        fichier.close()

def ajout_chemin_pdi():
    repertoire_instance="Instance_json"
    pattern=r'\w+'

    instances=os.listdir(repertoire_instance)
    instances=[re.findall(pattern, i)[0] for i in instances]

    ajout_chemin_instance_data=ajout_chemin_instance()
    for instance_nom in instances:
        ajout_chemin=ajout_chemin_instance_data[instance_nom]
        extension_instance=".json"
        #Chargement des setting json pour la recherche 
        with open(f"{repertoire_instance}/{instance_nom}{extension_instance}") as instance_file:
            #objet json qui contient les settings de la recherche
            instance = json.load(instance_file)
            categorie_chemin=[[None for j in range(len(instance[X_PDI_key]))]for i in range(len(instance[X_PDI_key]))]
            for i in ajout_chemin:
                categorie_chemin[i[0]][i[1]]=ajout_chemin[i]
                categorie_chemin[i[1]][i[0]]=ajout_chemin[i]

            fichier = open(f"{repertoire_instance}/{instance_nom}{extension_instance}", "w")
            instance[Categorie_chemin_pdi_key]=categorie_chemin

            json_data=json.dumps(instance, indent=3)
            fichier.write(json_data)
            fichier.close()




#traduction_instance()
#ajout_chemin_pdi()
