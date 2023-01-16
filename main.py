from Crypto.Cipher import AES
import base64
import json

from classes.Metadata import Metadata
from classes.Node import Node

#globals
KEY = "6Oo7jxmrndKt9l0c"
KEY = KEY.encode()
nodes = dict()
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

def printAllNodes():
    for key, node in nodes.items():
        print("*"*30)
        print("ID: ", key)
        node.printNode()
        print("*"*30)

if __name__ == '__main__':
    handleDataConversion()

    printAllNodes()

    #example to access node with id
    nodes[3].printNode()