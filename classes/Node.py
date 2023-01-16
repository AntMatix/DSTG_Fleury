import json

class Node:
    def __init__(self, id, metadata, children):
        self.id = id
        self.metadata = metadata
        self.children = children
        self.visited = False
        self.fork = 0

    def printNode(self):
        print("ID: ", self.id)
        self.metadata.printMetadata()
        print("Children: ", self.children)
        print("Visited: ", self.visited)
        print("Fork: ", self.fork)
