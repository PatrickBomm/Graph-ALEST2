from tkinter import *
import webbrowser


class Graph:

    def __init__(self, nodes: list, directed: bool = True):
        self.nodes = nodes
        self.directed = directed
        self.listAdj = {node: list() for node in nodes}

    def addedge(self, node1: str, node2: str):
        self.listAdj[node1].append(node2)

        if not self.directed:
            self.listAdj[node2].append(node1)

    def printNodesAndEdges(self):
        for key in self.listAdj.keys():
            print(f"Node {key}: {self.listAdj[key]}")

    def canAcess(self, value1: str, value2: str) -> bool:

        alreadyVisited = []
        queue = []

        queue.append(value1)
        alreadyVisited.append(value1)

        while queue:
            a = queue.pop(0)

            if a == value2:
                return True

            for i in self.listAdj[a]:
                if i not in alreadyVisited:
                    queue.append(i)
                    alreadyVisited.append(i)

        return False

    def pathUpto2Interactions(self) -> int:
        counter = 0

        for i in self.listAdj.keys():
            for j in self.listAdj.keys():
                if j != i:
                    if self.canAcess(i, j):
                        counter = counter + 1

        return counter

    def pathUpto3Interactions(self) -> int:
        counter = 0
        for i in self.listAdj.keys():
            for j in self.listAdj.keys():
                if j != i:
                    if self.canAcess(i, j):
                        for nextJ in self.listAdj.keys():
                            if nextJ not in [i, j]:
                                if self.canAcess(j, nextJ):
                                    counter = counter + 1

        return counter


def readTxt(file: str) -> Graph:

    nodes = []
    edges = []

    with open(file) as f:
        lines = f.readlines()

        for line in lines:
            content = line.split(' ')
            if content[0] not in nodes:
                nodes.append(content[0])
            if content[2] not in nodes:
                nodes.append(content[2].split('\n')[0])

            edges.append(tuple([content[0], content[2].split('\n')[0]]))

    graph = Graph(nodes, directed=True)

    for edge in edges:
        graph.addedge(edge[0], edge[1])

    return graph


class Application(Frame):


    def __init__(self, master=None):
        # Read the configuration file
        graph = readTxt('assets/test.txt')

        # Create the interface    
        self.fontePadrao = ("Roboto", "14")
        self.fonteSecundaria = ("Arial", "12")
        self.primeiroContainer = Frame(master)
        self.primeiroContainer["pady"] = 10
        self.primeiroContainer.pack()

        self.segundoContainer = Frame(master)
        self.segundoContainer["padx"] = 20
        self.segundoContainer.pack()

        self.terceiroContainer = Frame(master)
        self.terceiroContainer["padx"] = 20
        self.terceiroContainer.pack()

        self.quartoContainer = Frame(master)
        self.quartoContainer["pady"] = 20
        self.quartoContainer.pack()

        self.quintoContainer = Frame(master)
        self.quintoContainer["pady"] = 20
        self.quintoContainer.pack()

        self.titulo = Label(self.primeiroContainer, text="Graph")
        self.titulo["font"] = ("Roboto", "15", "bold")
        self.titulo.pack()

        text = "Number of variations up to 3 flavors: " + (str(graph.pathUpto3Interactions()))

        self.path3flavors = Label(self.terceiroContainer,
                                  text=text, font=self.fontePadrao)
        self.path3flavors.pack(side=LEFT)

        text2 = "Number of variations up to 2 flavors: " + (str(graph.pathUpto2Interactions()))

        self.path2flavors = Label(self.segundoContainer,
                                  text=text2, font=self.fontePadrao)
        self.path2flavors.pack(side=LEFT)

        self.openSite = Button(self.quintoContainer, text="Site to see the Graph",
                               font=self.fontePadrao, command=self.openSite)
        self.openSite.pack(side=RIGHT)

        self.text = Label(
            self.quartoContainer, text="Copy the text at 'grafo.dot' file to paste at site!", font=self.fonteSecundaria)
        self.text.pack(side=LEFT)

    def openSite(self):
        webbrowser.open("https://dreampuf.github.io/GraphvizOnline/#")


root = Tk()
Application(root)
root.mainloop()
