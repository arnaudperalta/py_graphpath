# coding: utf-8
import json

from graph import Graph
from os import listdir
from os.path import isfile, join

CONFIG_DEFAUT = "graph1.json"


# Fonction main du projet
def run_project():
    config = CONFIG_DEFAUT
    # Affichage du menu principal
    print_menu(config)
    while True:
        s = input()
        for c in s:
            if c == "c":
                # Affichage du menu de configuration avec recupération du fichier
                config = menu_config()
            elif c == "t" or c == "n":
                # Création de l'objet Graph avec en paramètre la configuration choisie
                graph = Graph(load_config(config))
                # Execution du premier algo
                start_algo(graph, c)
            elif c == "h":
                # Affichage de l'aide
                print_help()
            elif c == "m":
                # Affichage du menu
                print_menu(config)
            elif c == "q":
                # Fin du programme
                return


# Fonction d'affichage de l'aide
def print_menu(config):
    print("py_graphpath")
    print("-----------------------------------------------------")
    print("c : Choisir la configuration (Actuel : " + config + ")")
    print("t : Lancer l'algorithme Point de rendez-vous optimal par le temps")
    print("n : Lancer l'algorithme Point de rendez-vous optimal par les déplacements")
    print("h : pour acceder à l'aide")
    print("m : pour afficher le menu")
    print("q : pour arrêter le programme.")


# Fonction du système de configuration du programme
def menu_config():
    config = ""
    print("Configurations disponibles :")
    list_cfg = [f for f in listdir('./cfg') if isfile(join('./cfg', f))]
    for i in range(0, len(list_cfg)):
        print(list_cfg[i])
    while True:
        config = raw_input("").rstrip()
        if list_cfg.__contains__(config):
            print("Configuration changée avec succès.")
            break
        else:
            print("Cette configuration n'existe pas.")
    return config


# Fonction d'affichage de l'aide
def print_help():
    print("Aide")
    print("Pour un exemple de la syntaxe de configuration, voir graph_sujet.json")
    print("Le premier algorithme calcul le point de rendez-vous le plus optimal")
    print("pour que les deux personnes se rencontrent sur ce point en temps minimum.")
    print("Le second algorithme calcul le pooint de rendez-vous le plus optimal")
    print("pour que les deux personnes se rencontrent sur ce point en un nombre")
    print("de déplacements minimum.")
    print("Il est possible de saisir plusieurs caractères à la suite dans le menu du programme.")


# Fonction de lancement des deux algorithmes du programme
def start_algo(g, c):
    if g.error != 0:
        if g.error == 1:
            print("Erreur dans le fichier configuration (nbNoeuds/nomSommets)")
        elif g.error == 2:
            print("Erreur dans le fichier configuration (nbLieuxRdv/nomRdv)")
    if c == "t":
        resultat = g.rdv_optimal()
        if resultat != "":
            print ("Le point de rendez-vous le plus optimal par le temps est : " + resultat)
        else:
            print("Pas de point de rendez-vous compatible")
    elif c == "n":
        resultat = g.rdv_optimal2()
        if resultat != "":
            print ("Le point de rendez-vous le plus optimal par les déplacements est : " + resultat)
        else:
            print("Pas de point de rendez-vous compatible")


# Fonction du chargement de la configuration JSON en mémoire
def load_config(config):
    with open('./cfg/' + config, 'r') as fichier:
        return json.load(fichier)


# Lancement du main
if __name__ == '__main__':
    run_project()
