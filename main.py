from Crypto.Cipher import AES
import base64
import json
import xlsxwriter

from classes.Metadata import Metadata
from classes.Node import Node
from classes.WastedTime import WastedTime
from classes.Stack import Stack

#globals
KEY = "6Oo7jxmrndKt9l0c"
KEY = KEY.encode()
nodes = dict()
visited_nodes = Stack()
unnecessary_nodes = list()
workers_wasted_time = dict()
##endOf globals


def removePadding(plain_text):
        last_character = plain_text[len(plain_text) - 1:]
        return plain_text[:-ord(last_character)]

def decryptTheLabel(txtToDecrypt):
    decipher = AES.new(KEY, AES.MODE_ECB)
    decrypted = decipher.decrypt(txtToDecrypt).decode("utf8")
    #print(removePadding(decrypted))
    noPaddingDecrypted = removePadding(decrypted)
    decryptedJSON = json.loads(noPaddingDecrypted)
    return decryptedJSON

def createMetadataObject(data):
    try:
        return Metadata(*data.values())
    except:
        raise Exception("Can not create Metadata object")

def handleDataConversion():
    #Open the json file and read its contents into data variable
    with open("ZadatakInput.json", "r") as f:
        loaded_objects = json.load(f)

    #Add values of each -label- element into array label_values
    label_values = [obj["label"] for obj in loaded_objects]

    for obj in loaded_objects:
        decryptedLabel =  decryptTheLabel(base64.b64decode(obj["label"]))
        metadataObj = createMetadataObject(decryptedLabel)
        nodeObj = Node(obj["id"], metadataObj, obj["children"])
        nodes[obj["id"]] = nodeObj

    #Print out number of elements
    #print(len(label_values))

    #Print out decrypted values for each label
    #for val in label_values:
    #    decryptTheLabel(base64.b64decode(val))


def numOfUnvisitedChildren():
    last_node = visited_nodes.items[-1]
    if(len(last_node.children) == 0):
        return -1
    numOfUnvisitedChildren = 0
    for childId in last_node.children:
        if (nodes[childId].visited == False):
            numOfUnvisitedChildren += 1
    return numOfUnvisitedChildren


def returnFirstUnvisitedChildId():
    last_node = visited_nodes.items[-1]
    for childId in last_node.children:
        if (nodes[childId].visited == False):
            return childId
    return False


def findingRedundantNodes():
    # for key, node in nodes.items():
    nodes[1].visited = True
    visited_nodes.push(nodes[1])
    delete_flag = False
    while (visited_nodes.isEmpty() == False):
        last_node = visited_nodes.items[-1]
        _numOfUnvisitedChildren = numOfUnvisitedChildren()
        if (_numOfUnvisitedChildren > 0):
            if(delete_flag == True):
                visited_nodes.items[-1].fork += 1
                delete_flag = False
            if(delete_flag == False):
                newLastNodeId = returnFirstUnvisitedChildId()
                if (newLastNodeId != False):
                    nodes[newLastNodeId].visited = True
                    visited_nodes.push(nodes[newLastNodeId])
##############################
        elif (_numOfUnvisitedChildren == 0):
            if(delete_flag == False):
                visited_nodes.pop()
            if(delete_flag == True):
                visited_nodes.pop()
                if (last_node.fork == (len(last_node.children)-1)):
                    if (last_node.metadata._type != "CP"):
                        unnecessary_nodes.append(last_node)
                else:
                    delete_flag = False
##############################
        elif (_numOfUnvisitedChildren == -1):
            if (last_node.metadata.branch == "develop"):
                visited_nodes.pop()
            if (last_node.metadata.branch == "feature"):
                delete_flag = True
                if (last_node.metadata._type == "CP"):
                    visited_nodes.pop()
                else:
                    visited_nodes.pop()
                    unnecessary_nodes.append(last_node)








def updateAuthorsWastedTime(author, dictionary, time):
    if author in dictionary:
        dictionary[author].time_wasted += time
    else:
        dictionary[author] = WastedTime(time)

def calculateWastedTime():
    for node in unnecessary_nodes:
        author = node.metadata.author
        time = node.metadata.time
        updateAuthorsWastedTime(author, workers_wasted_time, time)

def calculateTotalWastedTime():
    total_time_wasted = 0
    for _, node in workers_wasted_time.items():
        total_time_wasted += node.time_wasted
    return total_time_wasted

def printAllNodes():
    for key, node in nodes.items():
        print("*"*30)
        print("ID: ", key)
        node.printNode()
        print("*"*30)

def printWorkersWastedTime():
    for key, node in workers_wasted_time.items():
        print("*"*30)
        print("ID: ", key)
        print("Wasted Time: " + str(node.time_wasted))
        print("*"*30)

def writeOutWastedTime():
    with open("Wasted Time.txt", "w") as f:
        f.write("Wasted Time per worker \n")
        for key, node in workers_wasted_time.items():
            f.write("ID: " + key + ", Wasted time: " + str(node.time_wasted) + "\n")
        f.write("Wasted Time total: " + str(calculateTotalWastedTime()) + "\n")

def writeOutWastedTimeExcel():
    workbook = xlsxwriter.Workbook("Wasted Time.xlsx")
    worksheet = workbook.add_worksheet()
    worksheet.set_column("A:B", 25)

    bold = workbook.add_format({'bold': True})

    worksheet.write('A1', 'Email', bold)
    worksheet.write('B1', 'Wasted time', bold)

    row = 0

    for key, node in workers_wasted_time.items():
        row += 1
        worksheet.write(row, 0, key)
        worksheet.write(row, 1, str(node.time_wasted))

    row += 2
    worksheet.write(row, 0, "Total Wasted Time:", bold)
    worksheet.write(row, 1, str(calculateTotalWastedTime()))

    workbook.close()


if __name__ == '__main__':
    handleDataConversion()

    findingRedundantNodes()

    for node in unnecessary_nodes:
        node.printNode()


    calculateWastedTime()

    writeOutWastedTime()
    writeOutWastedTimeExcel()

    #printAllNodes()

    #example to access node with id
    #nodes[3].printNode()

    #printWorkersWastedTime()
    

    #print("Total wasted time: " + str(calculateTotalWastedTime()))