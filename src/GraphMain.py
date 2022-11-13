# -*- coding: UTF-8 -*-
from graphviz import Digraph
from tkinter import *
import webbrowser


class Grafo:
    list = []
    counter3path = 0
    counter2path = 0

    def __init__(self):
        self.__nodos = []
        self.__matriz = []

    # Find the position of a node in the array of nodes
    def searchNode(self, value):
        if (value in self.__nodos):
            return self.__nodos.index(value)
        return -1

    # Insert a node in the graph
    def insertNode(self, value):
        if (self.searchNode(value) < 0):
            self.__nodos.append(value)
            self.__matriz.append({})
            return True
        return False

    # Insert an arc in the graph
    def insertEdge(self, startValue, endValue, peso=1):
        nextStart = self.searchNode(startValue)
        nextEnd = self.searchNode(endValue)
        if (nextStart >= 0 and nextEnd >= 0):
            self.__matriz[nextStart][endValue] = peso
            return True
        return False

    # Show the values ​​(or information) of the nodes in the graph
    def showNodes(self):
        aux = ""
        i = 0
        for nodo in self.__nodos:
            print(i, nodo)
            i = i + 1
            aux = aux + nodo + "\n"
        return aux

    # checks how many variations of paths of at most 3 steps there are and returns the number of paths
    def pathUpto3Interactions(self, nodo):
        global counter3path
        nextStart = self.searchNode(nodo)
        if (nextStart < 0):
            return False

        for endValue in self.__matriz[nextStart]:
            nextStart2 = self.searchNode(endValue)
            for endValue2 in self.__matriz[nextStart2]:
                counter3path = counter3path + 1
        return True

    # checks how many variations of paths of at most 2 steps there are and returns the number of paths
    def pathUpto2Interactions(self, nodo):
        global counter2path        
        list = []

        nextStart = self.searchNode(nodo)

        if (nextStart < 0):
            return False

        for endValue in self.__matriz[nextStart]:
            counter2path = counter2path + 1
            next = self.searchNode(endValue)
            for endValue2 in self.__matriz[next]:
                boolean = False

                if len(list) > 0:
                    for i in list:
                        if (i == endValue2):
                            boolean = True
                            return
                    if (boolean == False):
                        counter2path = counter2path + 1
                        list.append(endValue2)
                        break

                else:
                    counter2path = counter2path + 1
                    list.append(endValue2)

        return True

    # Dot

    def showDot(self):
        dot = Digraph(format="png")
        styleNoeuds = {'fontname': 'Arial', 'shape': 'ellipse',
                       'color': '#000000', 'style': 'filled', 'fillcolor': '#ffffff'}
        dot.node_attr.update(styleNoeuds)
        dot.attr(rankdir="LR", size="8,5")

        for nodo in self.__nodos:
            nextStart = self.searchNode(nodo)
            if (nextStart < 0):
                break

            for endValue in self.__matriz[nextStart]:
                dot.edge(nodo, endValue)

        dot.view("assets/grafo.dot", cleanup=True)

    def path3flavors(self):
        global counter3path
        counter3path = 0
        for nodo in self.__nodos:
            self.pathUpto3Interactions(nodo)

        return (counter3path)

    def path2flavors(self):
        global counter2path, list
       
        counter2path = 0
        for nodo in self.__nodos:
            self.pathUpto2Interactions(nodo)

        return (counter2path)

    # Print all edges of the graph
    def showEdges(self):
        aux = ""
        for nodo in self.__nodos:
            nextStart = self.searchNode(nodo)
            if (nextStart < 0):
                break

            for endValue in self.__matriz[nextStart]:
                aux = aux + nodo + " -> " + endValue + "\n"
        return aux

# Read the text file and create the graph
def readTxt():
    file = open("assets/test.txt", "r")
    lines = file.readlines()
    file.close()

    grafo = Grafo()

    for line in lines:
        if line == " " or line == "\n":
            break
        line = line.strip()
        line = line.split(" -> ")
        grafo.insertNode(line[0])
        grafo.insertNode(line[1])
        grafo.insertEdge(line[0], line[1])
    return grafo


# MAIN
g = readTxt()


path3flavors = g.path3flavors()
path2flavors = g.path2flavors()
print("\n\n\n\nNumber of variations up to 2 flavors: ", path2flavors)

print("Number of variations up to 3 flavors: ", path3flavors)

try:
    g.showDot()
except:
    print(" ")

# Graphical interface
class Application(Frame):

    global path3flavors, path2flavors

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

        texto = "Number of variations up to 3 flavors: " + str(path3flavors)

        self.path3flavors = Label(self.terceiroContainer,
                                  text=texto, font=self.fontePadrao)
        self.path3flavors.pack(side=LEFT)

        texto2 = "Number of variations up to 2 flavors: " + str(path2flavors)

        self.path2flavors = Label(self.segundoContainer,
                                  text=texto2, font=self.fontePadrao)
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
