import json

from lib.graph import Graph

# Import the necessary packages

#Le graph1 est celui utilisé par defaut
graphe_name = 'graph1'


def run_project():
    with open('./cfg/' + graphe_name + '.json', 'r') as fichier:
        data = json.load(fichier)
    graph = Graph(data)
    graph.rdv_optimal()


if __name__ == '__main__':

    ans = True
    while ans:
        print("""
        1. Lancer le programme
        2. Choix du graphe
        3. Aide
        4. Quitter
        """)
        ans = input("Que faire ?")
        if ans == "1":
            run_project()
        elif ans == "2":
            print("""
            Graphes disponibles :
            
            Graph1
            Graph_sujet
            """)
            ans2 = input("Nom du graphe?")
            graphe_name = ans2
        elif ans == "3":
            print("\n AIDE A COMPLETER")
        elif ans == "4":
            print("\n Fin du programme")
            ans = None
        else:
            print("\n Choix non valide, essayez autre chose")
