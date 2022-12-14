from tkinter import *
import webbrowser
from graphviz import Digraph


class Graph:

    # Constructor
    def __init__(self, nodes: list, directed: bool = True):
        self.nodes = nodes
        self.directed = directed
        self.listAdj = {node: list() for node in nodes}

    # Add a edge to 2 nodes
    def addedge(self, node1: str, node2: str):
        self.listAdj[node1].append(node2)

        if not self.directed:
            self.listAdj[node2].append(node1)
    
    def printNodesAndEdges(self):
        for i in self.listAdj.keys():
            print(f"Node {i}: {self.listAdj[i]}")

    # Verify if can be connected from node1 to node2
    def canAccess(self, value1: str, value2: str) -> bool:

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

    # Count how many items can have two flavors
    def pathUpto2Interactions(self) -> int:
        counter = 0

        for i in self.listAdj.keys():
            for j in self.listAdj.keys():
                if j != i:
                    if self.canAccess(i, j):
                        counter = counter + 1

        return counter

    # Count how many items can have three flavor
    def pathUpto3Interactions(self) -> int:
        counter = 0
        for i in self.listAdj.keys():
            for j in self.listAdj.keys():
                if j != i:
                    if self.canAccess(i, j):
                        for nextJ in self.listAdj.keys():
                            if nextJ not in [i, j]:
                                if self.canAccess(j, nextJ):
                                    counter = counter + 1

        return counter
    
    def generateDot(self):
        dot = Digraph(comment='Graph', format='png')
        for key in self.listAdj.keys():
            for value in self.listAdj[key]:
                dot.edge(key, value)
        dot.render('assets/graph/graphDot.txt', view=True)

# Read the text file and add the nodes to the list


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

    
        # If want change the file, change the name here
        g = readTxt("assets/test20.txt")

        # Generate the graph to put on graphviz online
        try:
            g.generateDot()
        except:
            print("")
        
        if g != None:

            text = "Number of variations up to 3 flavors: " + \
                (str(g.pathUpto3Interactions()))

            self.path3flavors = Label(self.terceiroContainer,
                                      text=text, font=self.fontePadrao)
            self.path3flavors.pack(side=LEFT)

            text2 = "Number of variations up to 2 flavors: " + \
                (str(g.pathUpto2Interactions()))

            self.path2flavors = Label(self.segundoContainer,
                                      text=text2, font=self.fontePadrao)
            self.path2flavors.pack(side=LEFT)

            self.openSite = Button(self.quintoContainer, text="Site to see the Graph",
                                   font=self.fontePadrao, command=self.openSite)
            self.openSite.pack(side=RIGHT)

            self.text = Label(
                self.quartoContainer, text="Copy the text at 'graphDot.txt' file to paste at site!", font=self.fonteSecundaria)
            self.text.pack(side=LEFT)

    def openSite(self):
        webbrowser.open("https://dreampuf.github.io/GraphvizOnline/#")


root = Tk()
Application(root)
root.mainloop()
