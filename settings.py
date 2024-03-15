"""
Key pour les settings json
"""
#sert a avoir un niveau de verbositer de pycsp3 plus ou moins grand 
#valeur entre -1 et 2
verbose_key="verbose"
#nom du répertoire dans lequelle sont stocker les instances
instance_repertory_key="nom_repertoire_instance"
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
Minimise_distance_parcourue="Minimise_distance_parcourue"


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
#cle pour savoir la presence des pdi dans la solutions 
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

#sert a savoir quelle type d'objectif on a choisie sur la solution
Type_objectif_key="type_objectif"

#sert a savoir quelle était le temps de timout au moment de la résolution
Timeout_solver_key="timeout_solver"

#sert a savoir si le timeout était actif
Timeout_activer_key="timeout_activer"
"""
Argument du script python
"""
#clé pour les argument cours
key_short_arg="short"
#clé pour les argument long
key_long_arg="long"

#tableau qui contien les arguments long et cours pour inclure les fichier csv de chaque instance
key_file_include={key_short_arg:"f",key_long_arg:"file"}