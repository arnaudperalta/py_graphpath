import json

from lib.graph import Graph


def load_config(config):
    with open('./cfg/' + config, 'r') as fichier:
        return json.load(fichier)


def run_project():
    graph = "graph1.json"
    print("1. Choisir la config (Defaut : graph1.json)")
    print("2. Lancer l'algorithme TempsDeParcoursMinimal")
    print("3. Lancer l'algorithme NombreDeCheminsMinimal\n")
    print("h pour acceder à l'aide")
    print("q pour Quitter")
    ans = True
    while ans:
        ans = input("")
        if ans == "1":
            print("Configurations disponibles :\n")
            print("graph1.json")
            print("graph_sujet.json")
            graph = input("Configuration choisie?\n")
        elif ans == "2":
            graph = Graph(load_config(graph))
            graph.rdv_optimal()
            ans = None
        elif ans == "3":
            graph = Graph(load_config(graph))
            graph.rdv_optimal()
            ans = None
        elif ans == "h":
            print("AIDE A COMPLETER\n")
        elif ans == "q":
            print("Fin du programme\n")
            ans = None
        else:
            print("Commande non reconnue\n")


if __name__ == '__main__':
    run_project()
