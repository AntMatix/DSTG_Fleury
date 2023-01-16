class Metadata:
    def __init__(self, author, time, branch, _type):
        self.author = author
        self.time = time
        self.branch = branch
        self._type = _type


    def printMetadata(self):
        print("Author: ", self.author)
        print("Time: ", self.time)
        print("Branch: ", self.branch)
        print("Type: ", self._type)
