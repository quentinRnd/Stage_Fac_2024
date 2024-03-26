import pandas as pd

import os 
import re
import json

from settings import * 

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
            "X_PDI":[i for i in csv["X_k"]]
            ,"Y_PDI":[i for i in csv["Y_k"]]
            ,"Score_pdi":[i for i in csv["score_k"]]
            ,"Temps_visite":[i for i in csv["duracion_k"]]
            ,"Cout_entrer":[i for i in csv["entrada_k"]]
            ,"Heure_ouverture":[i for i in csv["open_k"]]
            ,"Heure_fermeture":[i for i in csv["close_k"]]
            ,"Categorie":[i for i in csv["categoria"]]
            ,"Capacite":[i for i in csv["capacidad"]]
        }
        json_data=json.dumps(data, indent=3)
        fichier.write(json_data)
        fichier.close()

def ajout_chemin_pdi():
    repertoire_instance="Instance_json"
    instances=["Instancia1"]
    ajout_chemin={
                    #des chemin plutot de entre ville et nature
                    (9,37):[0.3,0.8,0.1,0,0,0.6],(9,35):[0.3,0.8,0.1,0,0,0.6],(9,39):[0.3,0.8,0.1,0,0,0.6]
                    ,(9,44):[0.3,0.8,0.1,0,0,0.6],(9,32):[0.3,0.8,0.1,0,0,0.6],(9,32):[0.3,0.8,0.1,0,0,0.6]
                    ,(9,35):[0.3,0.8,0.1,0,0,0.6]
                    # des chemin plutot de grande nature
                    ,(36,31):[1,0,0.3,0.8,0.5,0.8],(0,31):[1,0,0.3,0.8,0.5,0.8],(9,35):[1,0,0.3,0.8,0.5,0.8]
                    ,(36,41):[1,0,0.3,0.8,0.5,0.8],(31,41):[1,0,0.3,0.8,0.5,0.8],(0,36):[1,0,0.3,0.8,0.5,0.8]
                    #des chemin de ville
                    ,(47,12):[0,1,0.5,0,0,0],(12,24):[0,1,0.5,0,0,0],(47,24):[0,1,0.5,0,0,0]
                    ,(21,12):[0,1,0.5,0,0,0],(38,12):[0,1,0.5,0,0,0],(38,21):[0,1,0.5,0,0,0]
                    ,(38,47):[0,1,0.5,0,0,0],(40,38):[0,1,0.5,0,0,0]

                    #des chemin pres de rivière et de lacs
                    ,(42,43):[1,0,0.4,1,1,1],(42,11):[1,0,0.4,1,1,1],(42,45):[1,0,0.4,1,1,1],(11,45):[1,0,0.4,1,1,1]
                    ,(11,10):[1,0,0.4,1,1,1],(10,34):[1,0,0.4,1,1,1],(10,37):[1,0,0.4,1,1,1],(10,45):[1,0,0.4,1,1,1]
                    ,(10,37):[1,0,0.4,1,1,1],(34,22):[1,0,0.4,1,1,1],(34,7):[1,0,0.4,1,1,1],(34,35):[1,0,0.4,1,1,1]

                    #des chemin de ville avec des lacs
                    ,(23,36):[0.2,1,0.3,0,1,0.3],(23,25):[0.2,1,0.3,0,1,0.3],(23,15):[0.2,1,0.3,0,1,0.3]
                    ,(23,26):[0.2,1,0.3,0,1,0.3],(23,18):[0.2,1,0.3,0,1,0.3],(23,16):[0.2,1,0.3,0,1,0.3]
                    ,(18,26):[0.2,1,0.3,0,1,0.3],(18,36):[0.2,1,0.3,0,1,0.3],(18,17):[0.2,1,0.3,0,1,0.3]
                    ,(18,15):[0.2,1,0.3,0,1,0.3],(41,36):[0.2,1,0.3,0,1,0.3],(36,31):[0.2,1,0.3,0,1,0.3]
                    ,(36,25):[0.2,1,0.3,0,1,0.3],(36,23):[0.2,1,0.3,0,1,0.3],(36,25):[0.2,1,0.3,0,1,0.3]
                    
                    #avec de l'élevation en ville
                    ,(6,45):[0.2,1,0.8,0,1,0.3],(6,3):[0.2,1,0.8,0,1,0.3],(6,27):[0.2,1,0.8,0,1,0.3]
                    ,(6,45):[0.2,1,0.8,0,1,0.3],(6,22):[0.2,1,0.8,0,1,0.3],(6,11):[0.2,1,0.8,0,1,0.3]
                    ,(3,27):[0.2,1,0.8,0,1,0.3],(3,11):[0.2,1,0.8,0,1,0.3],(3,45):[0.2,1,0.8,0,1,0.3]
                    ,(27,45):[0.2,1,0.8,0,1,0.3],(27,10):[0.2,1,0.8,0,1,0.3],(27,7):[0.2,1,0.8,0,1,0.3]

                    #avec de l'élevation en nature
                    ,(40,30):[1,0,0.8,0.4,0.6,0.6],(40,15):[1,0,0.8,0.4,0.6,0.6],(40,25):[1,0,0.8,0.4,0.6,0.6]
                    ,(40,17):[1,0,0.8,0.4,0.6,0.6],(40,18):[1,0,0.8,0.4,0.6,0.6],(40,23):[1,0,0.8,0.4,0.6,0.6]
                    ,(40,2):[1,0,0.8,0.4,0.6,0.6],(32,0):[1,0,0.8,0.4,0.6,0.6],(32,23):[1,0,0.8,0.4,0.6,0.6]
                    ,(32,11):[1,0,0.8,0.4,0.6,0.6]
                }
    extension_instance=".json"
    #Chargement des setting json pour la recherche 
    with open(f"{repertoire_instance}/{instances[0]}{extension_instance}") as instance_file:
        #objet json qui contient les settings de la recherche
        instance = json.load(instance_file)
        categorie_chemin=[[None for j in range(len(instance[X_PDI_key]))]for i in range(len(instance[X_PDI_key]))]
        for i in ajout_chemin:
            categorie_chemin[i[0]][i[1]]=ajout_chemin[i]
            categorie_chemin[i[1]][i[0]]=ajout_chemin[i]
        
        fichier = open(f"{repertoire_instance}/{instances[0]}{extension_instance}", "w")
        instance[Categorie_chemin_pdi_key]=categorie_chemin

        json_data=json.dumps(instance, indent=3)
        fichier.write(json_data)
        fichier.close()
    
    
ajout_chemin_pdi()