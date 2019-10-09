import json

from graph import Graph


def run_project():
    with open('./config.json', 'r') as fichier:
        data = json.load(fichier)
    graph = Graph(data)


if __name__ == '__main__':
    run_project()