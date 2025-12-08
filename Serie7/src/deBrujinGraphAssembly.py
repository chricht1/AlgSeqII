from collections import defaultdict

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
    def __init__(self, deBrujinGraph:DeBrujinGraph):
        self.graph = deBrujinGraph

    def findAssemblyEuler(self, nodeDegrees, outFile): # Algorihtm of Hierholzer
        g = self.graph
        edgeMarks = defaultdict(lambda: defaultdict(int))
        

        for node in nodeDegrees:
            if node[0] == 0 and node[1] == 1:
                startNode = node
        node = startNode
        assembly = startNode.key()

        while(node is not None):
            for succBase, edgeCount in g[node]: 
                if edgeMarks[node][succBase] < edgeCount:
                    nextNode = g[node[1:]+succBase]
                    edgeMarks[node][succBase] += 1
                    assembly += succBase
                    node = nextNode 
                    break
                