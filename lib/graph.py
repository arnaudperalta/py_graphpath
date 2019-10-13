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
            if mat_pcd[init, rdv[i]] != np.inf:
                print("sommet : " + self.rdvList[i])
                print("distance : " + str(mat_pcd[init, rdv[i]]))
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

    def mat_pcc(self, mat):
        size_pair = self.size * self.size
        for i in range(size_pair):
            mat[i,i] = 0
        matpcc = np.full((size_pair, size_pair), 0)
        for i in range(size_pair):
            for j in range(size_pair):
                if i != j and mat[i,j] != np.inf:
                    matpcc[i,j] = i + 1;
        for k in range(size_pair):
            for i in range(size_pair):
                for j in range(size_pair):
                    av = mat[i,j]
                    mat[i,j] = min(mat[i,j],mat[i,k]+mat[k,j])
                    if av != mat[i,j] :
                        matpcc[i, j] = k + 1
        return (mat, matpcc)

    def rdv_optimal2(self):
        doublemat = self.mat_pcc(self.transform(self.mat_graph()))
        init = self.pos_sommet(self.sommetsIniList[0])*self.size + self.pos_sommet(self.sommetsIniList[1])
        rdv = []
        for c in self.rdvList:
            rdv.append(self.pos_sommet(c)*self.size + self.pos_sommet(c))
        res = []
        res2 = []
        for i in range(len(rdv)):
            k = 0
            pos = i
            while doublemat[1][init,pos] != 0 and k < (self.size**2):
                pos = doublemat[1][init,pos] - 1
                ++k
            if pos == init :
                res.append(k)
            else :
                res.append(np.inf)
            res2.append(doublemat[0][init,rdv[i]])
        min = np.inf
        candidat = []
        for i in range(len(res)):
            if res[i] < min:
                candidat.clear()
                candidat.append(i)
            elif res[i] == min :
                candidat.append(i)

        resfinal = candidat[0]
        if(len(candidat) > 1):
            minfinal = np.inf
            for k in range(len(candidat)):
                if res2[candidat[k]] < minfinal:
                    resfinal = candidat[k]
                    minfinal = res2[candidat[k]]
        if resfinal != np.inf:
            print("le rdv le plus optimal est : " + self.rdvList[resfinal])
        else:
            print("pas de rdv possible")
