import numpy.matlib
import numpy as np
import sys
numpy.set_printoptions(threshold=sys.maxsize)


class Graph:
    def __init__(self, data):
        self.size = data["nbNoeuds"]
        self.sommetsList = list(data["nomSommets"])
        self.rdvList = list(data["nomRdv"])
        self.sommetsIniList = list(data["nomSommetsInitiaux"])
        self.arcs = list(data["arcs"])

        if self.sommetsList.__len__() != data["nbNoeuds"]:
            print("Erreur dans le fichier configuration (nbNoeuds/nomSommets)\n")

        if self.rdvList.__len__() != data["nbLieuxRdv"]:
            print("Erreur dans le fichier configuration (nbLieuxRdv/nomRdv)\n")

    def mat_graph(self):
        mat = np.full((self.size, self.size), np.inf)
        for arc in self.arcs:
            mat[self.pos_sommet(arc["sommetInitial"])
                , self.pos_sommet(arc["sommetTerminal"])] = arc["duree"]
        return mat

    def pos_sommet(self, char):
        return self.sommetsList.index(char)

    def transform(self, mat):
        size_pair = self.size * self.size
        mat_pair = np.full((size_pair , size_pair), np.inf)

        for i in range(self.size):
            for j in range(self.size):
                for k in range(self.size):
                    for l in range(self.size):
                        if i == k and j == l :
                            mat_pair[i * self.size + j, k * self.size + l] \
                                = np.inf
                        elif i == k :
                            mat_pair[i * self.size + j, k * self.size + l] \
                                = mat[j, l]
                        elif j == l :
                            mat_pair[i * self.size + j, k * self.size + l] \
                                = mat[i, k]
        print(mat_pair)

    def rdv_optimal(self):
        self.transform(self.mat_graph())
