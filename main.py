from Crypto.Cipher import AES
import base64
import json
import xlsxwriter

from classes.Metadata import Metadata
from classes.Node import Node
from classes.WastedTime import WastedTime

#globals
KEY = "6Oo7jxmrndKt9l0c"
KEY = KEY.encode()
nodes = dict()
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
        nodeObj = Node(metadataObj, obj["children"])
        nodes[obj["id"]] = nodeObj

    #Print out number of elements
    #print(len(label_values))

    #Print out decrypted values for each label
    #for val in label_values:
    #    decryptTheLabel(base64.b64decode(val))

def checkIfAuthorExists(author, dictionary):
    try:
        dictionary[author]
        return True
    except:
        return False

def addTimeToAuthorWastedTime(author, dictionary, time):
    dictionary[author].time_wasted += time

def updateAuthorsWastedTime(author, dictionary, time):
    if author in dictionary:
        dictionary[author].time_wasted += time
    else:
        dictionary[author] = WastedTime(time)

def calculateWastedTime():
    for _, node in nodes.items():
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

    calculateWastedTime()

    #printAllNodes()

    #example to access node with id
    #nodes[3].printNode()

    #printWorkersWastedTime()
    #writeOutWastedTime()
    writeOutWastedTimeExcel()

    #print("Total wasted time: " + str(calculateTotalWastedTime()))