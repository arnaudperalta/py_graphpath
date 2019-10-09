class Graph:
    def __init__(self, data):
        print("nbNoeuds : " + str(data["nbNoeuds"]))
        print("liste arcs : ")
        for arc in data["arcs"]:
            print(arc["sommetInitial"]
                  + " -- "
                  + str(arc["duree"])
                  + " --> "
                  + arc["sommetTerminal"])
