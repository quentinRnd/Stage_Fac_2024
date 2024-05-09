import os
def creation_repertoire(nomrep):
    if not os.path.exists(nomrep): 
        os.makedirs(nomrep)

#retourne l'emplacement du fichier rechercher
def nom_fichier(instance_repertory,nom_instance,extension_instance):
    return instance_repertory+"/"+nom_instance+extension_instance
