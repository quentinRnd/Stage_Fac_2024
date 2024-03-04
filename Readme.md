# Dépot pour le projet de Stage 2024 
# Titre: Optimisation d’itinéraire de randonnée
# Encadrants: <a href="mailto:frederic.lardeux@univ-angers.fr">Frédéric Lardeux</a>  et <a href="mailto:eric.monfroy@univ-angers.fr">Eric Monfroy</a>

# Intitulé
Le Slow Tourisme est une nouvelle forme de voyage qui est apparue dans les années 2000. Découvrir
des paysages tout en prenant son temps, s’imprégner pleinement de la nature et de la faune,
gastronomie, expériences culinaires et hébergement atypique ou de charme, sont les principes
majeurs du slow tourisme.


Un GPS calcule un itinéraire en optimisant (minimisant) des poids associés aux arcs d’un graphe: les
nœuds de ce graphe représentent des points/villes et les arcs, des distances ou temps entre deux
points.
D’un autre côté, le problème du calcul d’itinéraire a pour objectif de sélectionner un sous-ensemble
de nœuds d’un graphe maximisant une récompense. En quelque sorte, les “poids” sont ici sur les
nœuds du graphe.


Toutefois, le calcul d’itinéraire de randonnée pédestre dans le cadre du slow tourisme se démarque
des deux approches précédentes. En effet, il faut à la fois utiliser des critères sur arcs
(distance/temps de marche, difficulté de la marche, intérêt du paysage) et des critères sur les
nœuds (site touristique à visiter, faune à observer, repas, …).


Une première modélisation du problème a déjà été effectuée et est disponible.


L’objectif de ce stage est dans un premier temps d’enrichir cette modélisation avec de nouvelles
contraintes. Ensuite, il faudra réaliser un ensemble de tests afin de montrer la puissance des
modifications apportées. Et finalement développer une interface graphique.

# paquet python requis pour éxécuter le code suivant
- [PyCSP3](https://pypi.org/project/pycsp3/2.2/) installer la version 2.2 avec la commande 
```bash
pip install pycsp3==2.2  
```
- [NumPy](https://pypi.org/project/numpy/1.26.4/) installer la version 1.26 avec la commande suivante 
```bash
pip install numpy==1.26.4
```

- [pandas](https://pypi.org/project/pandas/2.2.1/) installer la version 2.2.1 avec la commande suivante 

```bash
pip install pandas==2.2.1
```

- [Pyvis](https://pypi.org/project/pyvis/0.3.2/) installer la version 0.3.2 avec la commande suivante 
```bash
pip install pyvis==0.3.2
```

