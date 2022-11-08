# -*- coding: UTF-8 -*-
from graphviz import Digraph    


class Grafo:
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

    def insertNode(self, value):
        if (self.searchNode(value) < 0):
            self.__nodos.append(value)
            self.__matriz.append({})
            return True
        return False

    def insertArc(self, startValue, endValue, peso=1):
        nextStart = self.searchNode(startValue)
        nextEnd = self.searchNode(endValue)
        if (nextStart >= 0 and nextEnd >= 0):
            self.__matriz[nextStart][endValue] = peso
            return True
        return False

    # Show the values ​​(or information) of the nodes in the graph
    def showNodes(self):
        i = 0
        for nodo in self.__nodos:
            print (i, nodo)
            i = i + 1

    # Show weight and destination node of the arcs (or edges) of a node, given its value
    def showArc(self, value):
        nextStart = self.searchNode(value)
        if (nextStart < 0):
            return False

        for endValue in self.__matriz[nextStart]:
            print(value, " -> ", endValue)
        return True

    # Indicates if there is an arc (or edge) from a source node to a destination node
    def existArc(self, startValue, endValue):
        nextStart = self.searchNode(startValue)
        nextEnd = self.searchNode(endValue)
        if (nextStart >= 0 and nextEnd >= 0):
            if (endValue in self.__matriz[nextStart]):
                return True
        return False

    # Remove a node from the graph
    def removeNode(self, startValue):
        nextStart = self.searchNode(startValue)
        del self.__nodos[nextStart]
        del self.__matriz[nextStart]

        for arcos in self.__matriz:
            if (startValue in arcos):
                del arcos[startValue]

    # Indicates if there are island nodes in a graph
    # Validate island node with link to itself
    def existIsland(self):
        pos = 0
        for arcos in self.__matriz:
            if (len(arcos) == 0):
                endValue = self.__nodos[pos]

                esIsla = True
                posNodo = 0
                for valNodo in self.__nodos:
                    if (endValue in self.__matriz[posNodo]):
                        esIsla = False
                    posNodo = posNodo + 1

                if (esIsla == True) or (self.existArc(valNodo, valNodo)):
                    return True

            pos = pos + 1
        return False

    # verifica quantas variacoes de caminhos de no maximo 3 passos existem e retorna o numero de caminhos
    def caminhosAte3Iteracoes(self, nodo):
        global counter3path
        nextStart = self.searchNode(nodo)
        if (nextStart < 0):
            return False

        for endValue in self.__matriz[nextStart]:
            nextStart2 = self.searchNode(endValue)
            for endValue2 in self.__matriz[nextStart2]:
                counter3path = counter3path + 1
        return True
    
    def caminhosAte2Iteracoes(self, nodo):
        global counter2path
        nextStart = self.searchNode(nodo)
        
        if (nextStart < 0):
            return False
        
        for endValue in self.__matriz[nextStart]:
            counter2path = counter2path + 1
        return True
        
    # Remove all the loops/links to the same graph
    def removeLoops(self):
        nextStart = 0
        for startValue in self.__nodos:
            for endValue in self.__matriz[nextStart]:
                if (startValue == endValue):
                    del self.__matriz[nextStart][endValue]
                    break

            nextStart = nextStart + 1

    # Shows the stored adjacency matrix of the graph

    def showStructure(self):
        print (self.__nodos)
        print (self.__matriz)
        
        
    # Dot
    def showDot(self):
        dot = Digraph( format="png")
        styleNoeuds = {'fontname':'Arial', 'shape':'ellipse', 'color': '#000000', 'style': 'filled', 'fillcolor':'#ffffff'}
        dot.node_attr.update(styleNoeuds)
        dot.attr(rankdir="LR", size="8,5")
        
        for nodo in self.__nodos:
            nextStart = self.searchNode(nodo)
            if (nextStart < 0):
                break

            for endValue in self.__matriz[nextStart]:
                dot.edge(nodo, endValue)

        dot.view("assets/grafo.dot", cleanup=True)     


    def path3(self):
        global counter3path
        counter3path = 0
        for nodo in self.__nodos:
            self.caminhosAte3Iteracoes(nodo)            
        
        return(counter3path)
    
    def path2(self):
        global counter2path
        counter2path = 0
        for nodo in self.__nodos:
            self.caminhosAte2Iteracoes(nodo)
        
        return(counter2path)



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
        grafo.insertArc(line[0], line[1])
    return grafo

# MAIN

g = readTxt()
print ("Nodos:\n")
g.showNodes()

print ("Number of variations up to 3 flavors: ", g.path3())

print("Number of variations up to 2 flavors: ", g.path2())
try:
    g.showDot()
except:
    print(" ")
