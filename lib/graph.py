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
        return mat_pair

    def rdv_optimal(self):
        mat_pcd = self.mat_pcd(self.transform(self.mat_graph()))
        init = self.pos_sommet(self.sommetsIniList[0])*self.size + self.pos_sommet(self.sommetsIniList[1])
        rdv = []
        for c in self.rdvList:
            rdv.append(self.pos_sommet(c)*self.size + self.pos_sommet(c))
        res = np.inf
        fin = np.inf
        for i in range(len(rdv)):
            if mat_pcd[init,rdv[i]] < res:
                res = mat_pcd[init,rdv[i]]
                fin = i
        if fin != np.inf:
            print("le rdv le plus optimal est : " + self.rdvList[fin])
        else:
            print("pas de rdv possible")



    def mat_pcd(self, mat):
        size_pair = self.size * self.size
        for i in range(size_pair):
            mat[i,i] = 0
        for k in range(size_pair):
            for i in range(size_pair):
                for j in range(size_pair):
                    mat[i,j] = min(mat[i,j],mat[i,k]+mat[k,j])
        return mat
