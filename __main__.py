import json

from lib.graph import Graph


def load_config(config):
    with open('./cfg/' + config, 'r') as fichier:
        return json.load(fichier)


def print_menu():
    print("1. Choisir la config (Defaut : graph1.json)")
    print("2. Lancer l'algorithme TempsDeParcoursMinimal")
    print("3. Lancer l'algorithme NombreDeCheminsMinimal\n")
    print("h pour acceder à l'aide")
    print("q pour Quitter")


def print_menu_config():
    print("Configurations disponibles :\n")
    print("graph1.json")
    print("graph_sujet.json")


def run_project():
    config = "graph1.json"
    print_menu()
    ans = True
    while ans:
        ans = input("")
        if ans == "1":
            print_menu_config()
            config = input("Configuration choisie?\n")
        elif ans == "2":
            config = Graph(load_config(config))
            config.rdv_optimal()
            ans = None
        elif ans == "3":
            config = Graph(load_config(config))
            config.rdv_optimal()
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
