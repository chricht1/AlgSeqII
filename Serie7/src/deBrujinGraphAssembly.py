from collections import defaultdict
import numpy as np
import os

class DeBrujinGraph:
    def __init__(self, sequences, k):
        self.construct(sequences, k)


    def construct(self, sequences, k):
        deBrujinGraph = defaultdict(lambda: defaultdict(bool))
        sequences = [t.upper() for t in sequences] # ignore soft-masked sequences
        for s in sequences:
            #print('seq ', s)
            for i in range(0, len(s)-k+2):
                kp1mer = s[i:i+k+1]
                deBrujinGraph[kp1mer[:-1]][kp1mer[-1]] = 1
        
        self.graph = deBrujinGraph


    def getUniqueEdgeDegreesNodes(self): # returns dict: node -> [inDegree, outDegree]
        degrees = defaultdict(lambda: [0,0])

        for node in self.graph:
            degrees[node][1] = len(self.graph[node])
            for succBase in self.graph[node]:
                if degrees[node[1:]+succBase][0] == 0:
                    degrees[node[1:]+succBase][0] = 1

        return degrees


    def getDegreesNodes(self): # returns dict: node -> [inDegree, outDegree]
        degrees = defaultdict(lambda: [0,0])

        for node in self.graph:
            degrees[node][1] = sum(self.graph[node].values())
            for succBase in self.graph[node]:
                degrees[node[1:]+succBase][0] += self.graph[node][succBase]

        return degrees
    
        
class Assembly:
    def __init__(self, deBrujinGraph:DeBrujinGraph, nodeDegees, outFile:str):
        self.graph = deBrujinGraph
        self.nodeDegees = nodeDegrees
        self.outFile = outFile

    def findAssemblyEuler(self, nodeDegrees): # Algorihtm of Hierholzer
        self.numPaths = 0
        self.edgeMarks = defaultdict(lambda: defaultdict(int))
        paths = []
        while 1:
            path = self.findEulerPath(nodeDegrees)
            if path == '':
                break
            paths.append(path)
            #print(f'found {self.numPaths} Paths')
            #print(f'writing Path of len {len(path)} to file')
        
        assembly = self.unitePaths(paths)
        self.writeAssemblyToFile(assembly)
        

    def findEulerPath(self, startNode):
        g = self.graph
        startNode = self.findStartNode()
        if node is None:
            return ''
        path = node.key()
        node = startNode
        while 1:
            if len(g[node] > 1):
                path = self.findEulerPath(node)

            elif len(g[node] == 0):
                break
            succBase = next(iter(g[node]))
            nextNode = g[node[1:]+succBase]
            self.removeEdge(node, succBase)
            path += succBase
            node = nextNode 
            break

        return path





    def findStartNode(self, nodeDegrees):
        startNode = None
        numStartNodes = 0
        for node in nodeDegrees:
            if node[0]+1 == node[1] and len(self.graph[node]) > 0: # indegree+1==outdegree
                numStartNodes += 1
                if startNode is None:
                    startNode = node
        print(f'{numStartNodes} start nodes found')
        return startNode
    

    def removeEdge(self, node, succBase):
        del self.graph[node][succBase]
        if len(self.graph[node]) == 0:
            del self.graph[node]


    def hasUmarkedEdges(self, node):
        g = self.graph
        for succBase in g[node]:
            if self.edgeMarks[node][succBase] < g[node][succBase]:
                return True
        return False
    

    def unitePaths(self, paths):
        for 
        return assembly


    def writeAssemblyToFile(self, assembly):
        lineLen = 81
        os.remove(self.outFile, exist_ok=True)

        with open(self.outFile, 'a') as f:
            #f.write(f'>{pathName}\n')
            for i in range(len(path)//lineLen):
                f.write(assembly[i*lineLen:(i+1)*lineLen] + '\n')
            f.write(assembly[(len(assembly)//lineLen)*lineLen:] + '\n')