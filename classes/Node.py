import json

class Node:
    def __init__(self, metadata, children):
        self.metadata = metadata
        self.children = children
        self.visited = False
        self.fork = 0

    def printNode(self):
        self.metadata.printMetadata()
        print("Children: ", self.children)
        print("Visited: ", self.visited)
        print("Fork: ", self.fork)
