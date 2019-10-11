import json

from lib.graph import Graph


# Import the necessary packages

def run_project():
    config = 'graph1'
    algo = 0;
    print("""
    1. Choisir la config (Defaut : graph1.json)
    2. Lancer l'algorithme TempsDeParcoursMinimal
    3. Lancer l'algorithme NombreDeCheminsMinimal

    h pour acceder à l'aide
    q pour Quitter
    """)
    ans = True
    while ans:
        ans = input("")
        if ans == "1":
            print("Configurations disponibles :\n\n"
                  "graph1\n"
                  "graph_sujet")
            ans2 = input("Configuration choisie?")
            config = ans2
        elif ans == "2":
            algo = 1
            ans = None
        elif ans == "3":
            algo = 2
            ans = None
        elif ans == "h":
            print("AIDE A COMPLETER")
        elif ans == "q":
            print("Fin du programme")
            ans = None
        else:
            print("Commande non reconnue")

    with open('./cfg/' + config + '.json', 'r') as fichier:
        data = json.load(fichier)
    graph = Graph(data)
    if (algo == 1):
        graph.rdv_optimal()


# A decommenter quand l'algo 2 sera implenté
# if(algo == 2):
# graph.ALGO2()


if __name__ == '__main__':
    run_project()
