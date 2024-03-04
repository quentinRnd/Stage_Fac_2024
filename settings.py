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