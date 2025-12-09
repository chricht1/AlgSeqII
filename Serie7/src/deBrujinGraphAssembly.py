from collections import defaultdict
import numpy as np

class DeBrujinGraph:
    def __init__(self, sequences, k):
        self.construct(sequences, k)


    def construct(self, sequences, k):
        deBrujinGraph = defaultdict(lambda: defaultdict(int))
        sequences = [t.upper() for t in sequences] # ignore soft-masked sequences
        for t in sequences:
            for i in range(0, len(t)-k+2):
                kp1mer = t[i:i+k+1]
                deBrujinGraph[kp1mer[:-1]][kp1mer[-1]] += 1
        
        self.graph = deBrujinGraph


    def getDegreesNodes(self): # returns dict: node -> [inDegree, outDegree]
        degrees = defaultdict(lambda: [0,0])

        for node in self.graph:
            degrees[node][1] = sum(self.graph[node].values())
            for succBase in self.graph[node]:
                degrees[node[1:]+succBase][0] += self.graph[node][succBase]

        return degrees
    
        
class Assembly:
    def __init__(self, deBrujinGraph:DeBrujinGraph, outFile:str):
        self.graph = deBrujinGraph
        self.outFile = outFile

    def findAssemblyEuler(self, nodeDegrees, outFile): # Algorihtm of Hierholzer
        self.numAssemblies = 0
        self.edgeMarks = defaultdict(lambda: defaultdict(int))
        
        while 1:
            assembly = self.findEulerPath(nodeDegrees)
            if assembly is None:
                break
            
        node = startNode
        assembly = startNode.key()

        

    def findEulerPath(self, nodeDegrees):
        g = self.graph
        node = self.findStartNode(nodeDegrees)
        
        while(node is not None):
            for succBase, edgeCount in g[node].items():
                if self.edgeMarks[node][succBase] < edgeCount:
                    nextNode = g[node[1:]+succBase]
                    self.edgeMarks[node][succBase] += 1
                    assembly += succBase
                    node = nextNode 
                    break

        return assembly


    def findStartNode(self, nodeDegrees):
        startNode = None
        for node in nodeDegrees:
            if node == [0,1]:
                startNode = node
        '''if startNode is None:
            for node in nodeDegrees:
                if node[0] % 2 == 1 and node[1] % 2 == 1 and node[0] < node[1] and self.hasUmarkedEdges():'''
        #I calculated an De-Brujin Graph from read sequences. Now I should find an assembly and thus an Euler Path or multiple Euler Paths. The first criteria to start  
        return startNode
    

    def hasUmarkedEdges(self):
        g = self.graph
        for node in g:
            for succBase in g[node]:
                if self.edgeMarks[node][succBase] < g[node][succBase]:
                    return True
        return False
    

    def writeAssemblyToFile(self, assembly, assemblyName):
        lineLen = 81
        if self.numAssemblies == 0:

        with open(self.outFile, 'a') as f:
            f.write(f'>{assemblyName}\n')
            for i in range(len(assembly)//lineLen):
                f.write(assembly[i*lineLen:(i+1)*lineLen] + '\n')
            f.write(assembly[(len(assembly)//lineLen)*lineLen:] + '\n')