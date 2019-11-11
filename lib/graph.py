import numpy as np


# Classe Graph:
# Implémentation d'un modèle de graphe accompagné de méthodes de calculs
#       pour les deux algorithmes de rendez-vous
class Graph:

    # Constructeur de la classe Graph, on associe a l'objet le nombre de noeuds, le nom des sommets
    #       les points de rendez-vous, les sommets initiaux et les arcs du graphe associé à data.
    def __init__(self, data):
        self.size = data["nbNoeuds"]
        self.sommetsList = list(data["nomSommets"])
        self.rdvList = list(data["nomRdv"])
        self.sommetsIniList = list(data["nomSommetsInitiaux"])
        self.arcs = list(data["arcs"])
        self.error = 0
        if self.sommetsList.__len__() != data["nbNoeuds"]:
            self.error = 1
        if self.rdvList.__len__() != data["nbLieuxRdv"]:
            self.error = 2

    # Fonction renvoyant un code d'erreur, aucune erreur n'est apparu si cette fonction renvoie 0
    def error(self):
        return self.error

    # Fonction renvoyant la matrice des distances du graphe
    def mat_graph(self):
        mat = np.full((self.size, self.size), np.inf)
        for arc in self.arcs:
            mat[self.pos_sommet(arc["sommetInitial"])
                , self.pos_sommet(arc["sommetTerminal"])] = arc["duree"]
        return mat

    # Fonction qui renvoie un entier correspondant a un sommet du graphe permettant le parcours des matrices
    def pos_sommet(self, char):
        return self.sommetsList.index(char)

    # fonction qui renvoie une matrice des distances correspondant  à un graphe qui à pour sommet une paire de
    #       sommet du graphe initial et pour arcs des arcs du graphe initial tel que pour a,b,i dans S on a :
    #       (a,b) -> ((a,i),(b,i)) et (a,b) -> ((i,a),(i,b))
    def transform(self, mat):
        size_pair = self.size * self.size
        mat_pair = np.full((size_pair, size_pair), np.inf)
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

    # fonction du premier algorithme qui détermine le points de rendez-optimal en comparant la plus courte distance
    #       entre le sommet initial (a,b) (où a et b sont les deux points de départs) et chaque points de rendez-vous
    #       possible (i,i) (où i figures parmit les points d'arrivés)
    def rdv_optimal(self):
        mat_pcd = self.mat_pcd(self.transform(self.mat_graph()))
        # sommet inital
        init = self.pos_sommet(self.sommetsIniList[0]) * self.size + self.pos_sommet(self.sommetsIniList[1])
        # construction d'un tableau contenant les points de rendez-vous possibles
        rdv = []
        for c in self.rdvList:
            rdv.append(self.pos_sommet(c) * self.size + self.pos_sommet(c))
        res = np.inf
        fin = np.inf
        # recherche de la plus courte distance
        for i in range(len(rdv)):
            if mat_pcd[init, rdv[i]] < res:
                res = mat_pcd[init, rdv[i]]
                fin = i
        if fin != np.inf:
            return str(self.rdvList[fin])
        else:
            return ""

    # fonction  qui prend une matrice des distances en entrée et qui renvoie la matrices des plus courtes distantes
    #       correspondantes selon l'algorithme de Floyd-Warshall
    def mat_pcd(self, mat):
        size_pair = self.size * self.size
        for i in range(size_pair):
            mat[i, i] = 0
        for k in range(size_pair):
            for i in range(size_pair):
                for j in range(size_pair):
                    mat[i, j] = min(mat[i, j], mat[i, k]+mat[k, j])
        return mat

    # fonction qui renvoie, en plus de la amtrice des plus courtes distance, la matrice des prédécesseur associé à la
    #       matrice des distances indiqua en entrée.
    def mat_pcc(self, mat):
        size_pair = self.size * self.size
        for i in range(size_pair):
            mat[i,i] = 0
        matpcc = np.full((size_pair, size_pair), 0)
        for i in range(size_pair):
            for j in range(size_pair):
                if i != j and mat[i, j] != np.inf:
                    matpcc[i, j] = i + 1
        for k in range(size_pair):
            for i in range(size_pair):
                for j in range(size_pair):
                    av = mat[i, j]
                    mat[i, j] = min(mat[i, j], mat[i, k]+mat[k, j])
                    if av != mat[i, j]:
                        matpcc[i, j] = k + 1
        return mat, matpcc

    # fonction du deuxième algorithme qui détermine le points de rendez-optimal en comparant le nombre d'étapes pour
    #       chaque chemin entre le sommet initiale (a,b) (où a et b sont les deux points de départs) et
    #       chaque points de rendez-vous possible (i,i) (où i figures parmit les points d'arrivés). Si plusieurs
    #       chemins ont le même nombre d'étapes, on se réfère à la matrice des plus courtes distances pour déterminer
    #       le point de rendez-vous optimal entre les points de rendez-vous restants.
    def rdv_optimal2(self):
        doublemat = self.mat_pcc(self.transform(self.mat_graph()))
        # sommet inital
        init = self.pos_sommet(self.sommetsIniList[0]) * self.size + self.pos_sommet(self.sommetsIniList[1])
        # construction d'un tableau contenant les points de rendez-vous possibles
        rdv = []
        for c in self.rdvList:
            rdv.append(self.pos_sommet(c) * self.size + self.pos_sommet(c))
        res = []
        res2 = []
        # on détermine le nombre d'étape entre le sommet initial le point de rendez-vous pour chaque
        #       rendez-vous possible
        for i in range(len(rdv)):
            k = 0
            pos = i
            while doublemat[1][init, pos] != 0 and k < (self.size ** 2):
                pos = doublemat[1][init, pos] - 1
                ++k
            if pos == init:
                res.append(k)
            else:
                res.append(np.inf)
            res2.append(doublemat[0][init, rdv[i]])
        minimum = np.inf
        candidat = []
        # on range dans un tableau les points de rendez-vous atteignable en un minimum d'étape
        for i in range(len(res)):
            if res[i] < minimum:
                candidat.clear()
                candidat.append(i)
            elif res[i] == minimum:
                candidat.append(i)
        resfinal = candidat[0]
        if len(candidat) > 1:
            # lorsqu'il y a plusieurs possibilité on se réfère à la matrice des plus courte distances
            minfinal = np.inf
            for k in range(len(candidat)):
                if res2[candidat[k]] < minfinal:
                    resfinal = candidat[k]
                    minfinal = res2[candidat[k]]
        if resfinal != np.inf:
            return str(self.rdvList[resfinal])
        else:
            return ""

