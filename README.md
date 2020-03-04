# py_graphpath
Projet de licence 3 en Python 3.7 portant sur des algorithmes de plus court chemin dans un graphe.

[![Run on Repl.it](https://repl.it/badge/github/arnaudperalta/py_graphpath)](https://repl.it/github/arnaudperalta/py_graphpath)
## Présentation
La réalisation de ce projet a eu pour objectif d'implémenter en langage Python 3.7 deux algorithmes sur des graphes représentant une situation dans laquelle deux personnes cherchent à se rejoindre.

Ce programme se présente sous formes de deux algorithmes :

- Le premier algorithme doit calculer les trajets les plus courts en terme de temps (la somme des valeurs de chaque arcs empruntés) pour que les deux amis se rejoignent à un point de rendez-vous.
- Le second algorithme quant à lui doit calculer les plus courts chemins en terme de distance (le nombre d'arcs parcourus).

L'utilisateur a la possibilité de choisir un graphe sur lequel exécuter ces algorithmes, ces graphes doit être écrit dans fichiers JSON dans le dossier cfg selon la structure décrite ci-dessous.

## Structure de données (JSON)

Pour ce graphe ci-dessous :

![image](https://i.imgur.com/Qd9LMoz.png)

On obtiendra ce json :

    {
      "nbNoeuds": 7,
      "nomSommets": "abcdefg",
      "nbLieuxRdv": 3,
      "nomRdv": "bdg",
      "nomSommetsInitiaux": "de",
      "arcs": [
        {
          "sommetInitial": "a",
          "sommetTerminal": "b",
          "duree": 1
        },
        ...
      ]
    }
    
## Résultat
Affichage lors de l'exécution de l'algorithme Point de rendez-vous optimal par le temps:

Le point de rendez-vous le plus optimal par le temps est : b

Affichage lors de l'exécution de l'algorithme Point de rendez-vous optimal par les déplacements:

Le point de rendez-vous le plus optimal par les déplacements est : d

## Librairies
- numpy : création de matrice et utilisation des fonctions de calcul matricielle.
- json : lecture des fichiers json pour la mise en mémoire de la configuration.
- os : lecture du dossier de configuration afin de proposer un choix à l'utilisateur
