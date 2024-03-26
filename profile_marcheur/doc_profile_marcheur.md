# explication des mots clé dans le fichier json
- __handi__ sert a savoir si la personne a besoin de dispositif PMR
- __niveau marche__ savoir sur une echelle combien de kilomètre les personnes veulent marcher
    - 0 peut marcher au maximum 2 km 
    - 1 peut marcher au maximum 4 km
    - 2 peut marcher au maximum 6 km
    - 3 peut marcher au maximum 8 km
    - 4 peut marcher au maximum 12 km
    - 5 peut marcher au maximum 16 km    
- __interet_chemin__ savoir quelle interet l'utilisateur.ice porte sur passer par des chemin definie selon ces préférence. Ce paramètre a une valeur entre 0 et 20. 
- __préférence marche__ sert a définir plusieur préference dont les valeur indicative sont situé entre 0 et 1. 
    - __nature__ besoin en environement nature de la personne
    - __ville__ besoin de faire des balade en ville
    - __élevation__ préference pour faire des marche ou il y'a du dénivelé
    - __foret__ préference pour passer par des forêts dans les différent chemin 
    - __lac__  préference pour passer par des lacs dans les différent chemin
    - __rivière__ préference pour passer par des rivières dans les différent chemin

pour le paramètre __préférence marche__ pour un besoin de maintanebilité et d'utilisation de ceux ci en pycsp3 les instance json seront augmenter de la forme suivante :
- dans le json je rajoute une matrice de tableau qui représente les valeur des different paramètre par connexion entre point d'interet
- ce tableau qui représente une connexion entre 2 pdi est de la forme suivante
    1. le premier élément représentge le paramètre __nature__
    1. le premier élément représentge le paramètre __ville__
    1. le premier élément représentge le paramètre __élevation__
    1. le premier élément représentge le paramètre __foret__
    1. le premier élément représentge le paramètre __lac__
    1. le premier élément représentge le paramètre __rivière__

les valeur dans ce tableau sont également entre 0 et 1
    
 