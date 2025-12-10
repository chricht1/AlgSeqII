from collections import defaultdict
import numpy as np
import os

class DeBrujinGraph:
    def __init__(self, sequences, k):
        self.construct(sequences, k)


    def construct(self, sequences, k):
        deBrujinGraph = defaultdict(lambda: defaultdict(bool))
        sequences = [t.upper() for t in sequences] # ignore soft-masked sequences
        kp1 = k+1
        for s in sequences:
            for i in range(0, len(s)-kp1+1):
                kp1mer = s[i:i+kp1]
                deBrujinGraph[kp1mer[:-1]][kp1mer[-1]] = 1 
                # important criteria: 
                # - don't store same edge multiple times
            deBrujinGraph[s[-k:]] # last k-mer in sequence
        self.graph = deBrujinGraph


    def getDegreesNodes(self): # returns dict: node -> [inDegree, outDegree]
        degrees = defaultdict(lambda: [0,0])

        for node in self.graph:
            degrees[node][1] = len(self.graph[node])
            for succBase in self.graph[node]:
                degrees[node[1:]+succBase][0] += self.graph[node][succBase]

        return degrees
    

        
class Assembly:
    def __init__(self, deBrujinGraph:DeBrujinGraph, nodeDegrees, outFile:str, outFileLineLen = None):
        self.graph = dict(deBrujinGraph.graph)
        self.nodeDegrees = nodeDegrees
        self.outFile = outFile
        self.outFileLineLen = outFileLineLen


    def findAssemblyEuler(self): # Algorihtm of Hierholzer
        self.numPaths = 0
        startNode = self.findStartNode()
        assembly, _ = self.findEulerPath(startNode)
        print(assembly)
        print(self.graph)
        if len(self.graph) != 0:
            print('There are multiple euler paths!\n' \
                  'Found multiple starting nodes.\n' \
                'Current program just outputs greedy solution.')
        
        self.writeAssemblyToFile(assembly)
        

    def findEulerPath(self, startNode, cycleStartNode = None):
        g = self.graph # just renaming
        path = startNode
        node = startNode
        
        endingPaths = []
        
        while 1:
            #print('curr node: ', node)
            if node not in g:
                print('Trying to access an already deleted node,\n'\
                      'reason could be two or more paths including'\
                      'the same edge in the De-Brujin-Graph.\n' \
                    'Taking only the aleady taken path.')
                return None, None

            if len(g[node]) > 1:
                # possible outcomes: 
                # - obtain complete path in one traversal including cycles
                # - obtain multiple possible endings of euler path, one could include cycle
                #   - we want to include cycle(s) in assembly not coupled to ending path -> check for cylces 
                #       - we want to add best ending path separately from cycles 
                
                while node in g and len(g[node]) >= 1:
                    #print('\nstarting recursion call at node ', node)
                    nextNode = self.getNextNode(node)
                    subPath, cycleStartNode = self.findEulerPath(nextNode, cycleStartNode = node)
                    
                    if subPath is None:
                        continue
                    
                    if cycleStartNode == subPath[-len(node):]:
                        print('Cycle found in euler path!\n' \
                                'Greedily appending to assembly.')
                        #print('cycle: ', cycleStartNode+subPath[len(node)-1:], '\n')
                        path += subPath[len(node)-1:]
                    else:
                        endingPaths.append(subPath)
                if len(endingPaths) > 1:
                    print(f'There are multiple ({len(endingPaths)}) ending paths!\n' \
                            'Appending longest one.\n')
                lenEndingPaths = [len(endingPath) for endingPath in endingPaths]
                path += endingPaths[np.argmax(np.array(lenEndingPaths))][len(node)-1:]
                return path, None
                    
            elif len(g[node]) == 0:
                #print('reached path end, returning\n')
                del g[node]
                return path, None
            
            nextNode = self.getNextNode(node)
            path += nextNode[-1]

            if nextNode == cycleStartNode: # cycle found
                #print(f'cycle found at next node: {nextNode}, returning\n')
                return path, cycleStartNode
            
            node = nextNode 

        
    def findStartNode(self):
        startNodes = []
        numStartNodes = 0
        for node in self.nodeDegrees:
            if self.nodeDegrees[node][0]+1 == self.nodeDegrees[node][1] and len(self.graph[node]) > 0: # indegree+1==outdegree
                numStartNodes += 1
                startNodes.append(node)
        print(f'{numStartNodes} possible start nodes found!\n' \
              'Taking the first one.\n' \
              'Taking the one with smallest degree would be an option (not implemented).')
        return startNodes[0]
    

    def getNextNode(self, node):
        succBase = next(iter(self.graph[node]))
        nextNode = node[1:]+succBase
        self.removeEdge(node, succBase)
        return nextNode


    def removeEdge(self, node, succBase):
        #print('del edge ', node, succBase)
        del self.graph[node][succBase]
        #print('len(self.graph[node]) ', len(self.graph[node]))
        if len(self.graph[node]) == 0:
            #print('del node ', node)
            del self.graph[node]


    def writeAssemblyToFile(self, assembly):

        if os.path.exists(self.outFile):
            os.remove(self.outFile)

        with open(self.outFile, 'a') as f:
            #f.write(f'>{pathName}\n')
            if self.outFileLineLen is not None:
                for i in range(len(assembly)//self.outFileLineLen):
                    f.write(assembly[i*self.outFileLineLen:(i+1)*self.outFileLineLen] + '\n')
                f.write(assembly[(len(assembly)//self.outFileLineLen)*self.outFileLineLen:] + '\n')
            else:
                f.write(assembly)