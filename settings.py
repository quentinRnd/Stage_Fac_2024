"""
Key pour les settings json
"""
#sert a avoir un niveau de verbositer de pycsp3 plus ou moins grand 
#valeur entre -1 et 2
verbose_key="verbose"
#nom du répertoire dans lequelle sont stocker les instances csv
instance_repertory_csv_key="nom_repertoire_instance_csv"
#nom du répertoire dans lequelle sont stocker les instances json
nom_repertoire_instance_json_key="nom_repertoire_instance_json"
#timeout du solver 
timeout_solver_key="timout_solver"
#nombre de solution a chercher 
nombre_solution_key="nombre_solution"
#repertoire dans lequel sont stocker les solutions 
repertoire_solution_key="repertoire_solution"
#savoir si on cherche la fonction objectif
fonction_objectif_key="fonction_objectif"
#permet de desactiver/activer le timeout de la recherche
timeout_actif_key="timeout_actif"
#cle pour choisir quelle solveur on utilise lors de la recherche
solver_key="solver"

#extension de fichier utiliser pour l'instance
extension_instance_key="extension_instance"

# c'est le paramètre qui gére quelle fonction objectif est choisie 
type_objectif_key="type_objectif"
#il y'a plusieurs objectif qui sont les suivants
#objectif qui permet de maximiser la somme des score des pdi
Maximise_score_pdi="Maximise_score_pdi"

Mix_distance_score_pdi="Mix_distance_score_pdi"

Maximise_score_chemin="Maximise_score_chemin"
#clé servant a savoir ou les profile de marcheureuse sont stocker
repertoire_profile_marcheureuse_key="repertoire_profile_marcheureuse"

#cle servant a savoir quelle profile on a selectionner dans le repertoire
profile_marcheureuse_choisie_key="profile_marcheureuse_choisie"

#clé permettant de savoir si on génère des solution intermediaire ou pas 
inter_solution_key="inter_solution"

#clé pour le timeout des solution intermediaire 
timout_solution_inter_key="timout_solution_inter"
"""
Key pour les solution json
"""
#cle pour le status de fin de recherche
Status_key="Status"
#cle pour savoir dans quelle état est la din de recherche
Fin_recherche_key="Fin_recherche"
#Savoir si le solver a atteind l'optimum
Optimum_key="Optimum"
#cle pour récupérer les solution du modèle
Solutions_key="Solutions"
#cle pour recupéré les arc des differente solution
Arc_key="Arc"
#cle pour savoir si on a visiter le pdi
Presence_pdi_key="Presence_pdi"
#cle pour savoir l'heure de départ des pdi
Start_pdi_key="Start_pdi"
#cle pour les coordonée x des pdi
Coordonee_pdi_x_key="coordonee_pdi_x"
#cle pour les coordonée y des pdi
Coordonee_pdi_y_key="coordonee_pdi_y"
#cle pour les temps de visite de chaque pdi
Temps_visite_key="Temps_visite"
#cle pour les score des pdi
Score_pdi_key="Score_pdi"

#clé pour la valeur de la fonction objectif
Bound_key="Bound"

#clé pour le teableau des bound des différente solution
Bound_tab_key="Bound_tab"

#sert a savoir quelle type d'objectif on a choisie sur la solution
Type_objectif_key="type_objectif"

#sert a savoir quelle était le temps de timout au moment de la résolution
Timeout_solver_key="timeout_solver"

#sert a savoir si le timeout était actif
Timeout_activer_key="timeout_activer"

#sert a savoir quelle sont les horaire d'ouverture et de fermeture des différent point d'intérêt
Closing_pdi_key="Closing_pdi"
Opening_pdi_key="Opening_pdi"

#sert a savoir les evaluation des chemin des pdi
Evaluation_path_key="Evaluation_path"

#sert a récuperer le cicuit généré par pycsp3
Circuit_key="Circuit"

#sert a savoir la distance minimal a parcourir
Distance_min_key="d_min"
#sert a savoir la distance maximal a parcourir
Distance_max_key="d_max"

#sert a savoir le nombre de vsite maximal par jour
Max_visite_pdi_key="Max_visite_pdi"

#sert a savoir le nombre de visite maximal par jour 
Min_visite_pdi_key="Min_visite_pdi"

"""
Argument du script python
"""
#clé pour les argument cours
key_short_arg="short"
#clé pour les argument long
key_long_arg="long"

#tableau qui contien les arguments long et cours pour inclure les fichier csv de chaque instance
key_file_include={key_short_arg:"f",key_long_arg:"file"}

#paramètre qui sert a savoir combien de thread de test sont lancer en parallèle 
key_num_thread={key_short_arg:"t",key_long_arg:"num_thread"}
#identifiant qui sert a savoir quelle est le numero du thread 
key_id_thread={key_short_arg:"i",key_long_arg:"id_thread"}

#paramètre pour nommer le modele 
key_id_name_model={key_short_arg:"output",key_long_arg:"output"}


"""
key for the instance json
"""
#clé pour les coordonée x des pdi
X_PDI_key="X_PDI"
#clé pour les coordonée y des pdi
Y_PDI_key="Y_PDI"
#cle pour les score des pdi 
Score_pdi_key="Score_pdi"
#cle pour les temps de visite de chaque pdi
Temps_visite_key="Temps_visite"
#cout e euro de l'entrer du pdi
Cout_entrer_key="Cout_entrer"
#heure d'ouverture du pdi
Heure_ouverture_key="Heure_ouverture"
#heure de fermeture du pdi
Heure_fermeture_key="Heure_fermeture"
#categorie des pdi
Categorie_key="Categorie"
#capacite des pdi signifie si on veut oui ou non aller dans des pdi qui peuvent acceuillir plus ou moins de monde
Capacite_key="Capacite"
#sert a savoir dans quelle catégorie sont les chemins entre les pdi
Categorie_chemin_pdi_key="Categorie_chemin_pdi"

"""
Key pour les profile de marcheur.euse
"""
#sert a savoir si une personne a besoin d'amenagement PMR
handi_key="handi"
#sert a savoir le niveau de marche d'une personne 
niveau_marche_key="niveau marche"
#sert a recuperer un objet qui contient différente préférence utilisateur.ice
preference_marche_key="préférence marche"
# sert a savoir les préférence en terme de nature de la personne 
nature_key="nature"
# sert a savoir les préférence en terme de ville de la personne 
ville_key="ville"
# sert a savoir les préférence en terme d'élévation des chemin emprintée de la personne 
élevation_key="élevation"
# sert a savoir les préférence en terme de forêt de la personne 
foret_key="foret"
#sert a savoir les préférence en terme de lac de la personne
lac_key="lac"
#sert a savoir les préférence en terme de rivière de la personne
riviere_key="rivière"
#sert a savoir l'interêt de l'utilisateur.ice envers les chemin 
interet_chemin_key="interet_chemin"
#représente le nombre de persone max autorisé dans un point d'interêt
capacite_max_key="capacite max"
#représente la distance minimum a parcourir par les personnes
distance_parcourue_min_key="distance parcourue min"
#représente la distance maximum a parcourir par les personnes
distance_parcourue_max_key="distance parcourue max"
#représente le budget maximum a dépenser dans les point d'intérêt visiter
budget_max_key="budget max"
#représente le temps max de visite de tout les point d'intérêt dans le chemin
Temps_max_visite_key="Temps max visite"
#représente les tranche de temps dans lequelle les départ sont découper
Tranche_temps_key="Tranche de temps"