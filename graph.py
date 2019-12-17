# coding: utf-8
import numpy as np


# Définition de la classe Graph contenant la structure d'un graphe ainsi que des différentes fonctions
#       permettant les réalistions des deux algorithmes de rendez-vous.
class Graph:
    # Structure du graphe
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

        # Ces attributs sont utilisé lors du parcours récursif du graphe dans l'algorithme 2
        # path conserve le chemin actuel
        self.path = np.zeros(self.size ** 2)
        # bool conserve les sommets par lesquels on est déja passé
        self.bool = np.zeros(self.size ** 2)
        # target correspont au point de rendez-vous actuellement testé
        self.target = 0
        # min conserve la taille du chemin le plus petit actuellement trouvé
        self.min = np.inf
        # res contient les chemins de taille min
        self.res = []

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
                    mat[i, j] = min(mat[i, j], mat[i, k] + mat[k, j])
        return mat

    # fonction récursive qui permet de parcourir le graphe en profondeur pour rassembler tout les chemins possible
    #       entre un point de départ et une cible. La pronfondeur est borné par la longueur d'un chemin minimal déja
    #       trouvé afin de limiter les appels récursif
    def explore(self, mat, position, depth):
        if depth > self.min:
            return
        self.path[depth] = position
        if position == self.target:
            if self.min == depth:
                # Si l'on a déja trouvé un chemin de même taille on sauvegarde aussi le nouveau chemin car il peut avoir
                #   une durée plus courte
                self.res.append(np.copy(self.path[0:depth + 1]).astype(int).tolist())
            if self.min > depth:
                # Si l'on trouve un nouveau chemin minimal on écrase notre résultat par ce nouveau chemin
                #       et on met à jour le nombre d'étape minimale
                self.min = depth
                self.res = [np.copy(self.path[0:depth + 1]).astype(int).tolist()]
            return
        # On marque ce sommet car on y est passé une fois
        self.bool[position] = 1
        for i in range(self.size ** 2):
            # Si il n'y a pas d'arc vers le sommet ou qu'on est déja passé par celui-ci on l'ignore
            if mat[position][i] == np.inf or self.bool[i] == 1:
                continue
            # Sinon on explore par ce sommet
            self.explore(mat, i, depth + 1)
        # on retire la marque
        self.bool[position] = 0
        return

    # Fonction qui implémente l'algorithme 2
    def rdv_optimal2(self):
        size_pair = self.size * self.size
        mat = self.transform(self.mat_graph())
        # Sommet inital
        init = self.pos_sommet(self.sommetsIniList[0]) * self.size + self.pos_sommet(self.sommetsIniList[1])
        # Construction d'un tableau contenant les points de rendez-vous possibles
        rdv = []
        for c in self.rdvList:
            rdv.append(self.pos_sommet(c) * self.size + self.pos_sommet(c))
        roadres = []
        sizemin = np.inf
        # Pour chaque point de rendez-vous on dresse une liste de chemin point de départ -> point de rendez-vous de
        #       taille minimale. En même temps on conserve la taille du plus petit chemin trouvé dans sizemin
        for i in range(len(rdv)):
            # Avant chaque exploration on réinitialise les variables et on choisit la bonne cible
            self.bool = np.zeros(self.size ** 2)
            self.path = np.zeros(self.size ** 2)
            self.min = np.inf
            self.target = rdv[i]
            self.explore(mat, init, 0)
            if len(self.res[0]) < sizemin:
                sizemin = len(self.res[0])
            roadres.append(self.res)
        candidat = []
        # On ne conserve que les points de rendez vous ayant des chemin de tailles minimales
        for i in range(len(roadres)):
            if (len(roadres[i][0])) == sizemin:
                candidat.append(roadres[i])
        distmin = np.inf
        resfinal = np.inf
        # On regarde combien de candidat on obtient
        if len(candidat) > 1:
            # Lorsqu'il y a plusieurs candidats on recherche celui qui a le plus court chemin en terme de durée parmi
            #       ceux de taille minimale
            for i in range(len(candidat)):
                dist = 0
                for u in range(len(candidat[i])):
                    for j in range(sizemin - 1):
                        # on calcule la durée du chemin
                        dist = dist + mat[candidat[i][u][j]][candidat[i][u][j + 1]]
                    if dist < distmin:
                        # Si on trouve une nouvelle durée minimale on sauvegarde celle-ci ainsi que le point de
                        #       rendez-vous qui se trouve à la fin du chemin
                        resfinal = candidat[i][0][sizemin - 1]
                        distmin = dist
        else:
            # Si il y a un seul candidat on le récupère en allant cherchez le point de rendez vous qui est le dernier
            #       des chemins qu'on a sauvegardé
            resfinal = candidat[0][0][sizemin - 1]
        return str(self.sommetsList[(resfinal // (self.size+1))])
