import json

from graph import Graph


def run_project():
    with open('./cfg/graph1.json', 'r') as fichier:
        data = json.load(fichier)
    graph = Graph(data)
    graph.rdv_optimal()


if __name__ == '__main__':
    run_project()