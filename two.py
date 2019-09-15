import string
import re
import json
import os
import demjson
import json
import queue
#from PersonInfo import PersonInfo
#from FamilyNode import FamilyNode

class FamilyNode:
    def __init__(self, identify = None, parentId = None, 
    children = None, nodeInfo = None):
        self.identify = identify
        self.parentId = parentId
        self.children = children
        self.nodeInfo = nodeInfo
class PersonInfo:
    def __init__(self, name = None, code = None):
        self.name = name
        self.code = code
def getname(s):
    ss = s.split(",")
    return ss
def getphone(s):
    pat = re.compile(r'[1-9]\d{10}')
    phonematch = pat.search(s);
    phone = phonematch.group(0);
    print(phone)
    return phone
def getdetailaddress(ss,phone):
    addressplit = ss[1].split(phone)
    #print(addressplit)
    sep = ''
    address = sep.join(addressplit)
    return address
def main():
    with open('pcas-code.json',encoding='utf-8')as f:
        content =json.load(f)
        jsonData = content[0]
        indentify = 1
        root = FamilyNode()
        root.nodeInfo = PersonInfo()
        root.nodeInfo.name = jsonData["name"]
        root.nodeInfo.code = jsonData["code"]
        root.children = jsonData["children"]
        root.indentify = indentify
        root.parentId = 0
        itemList = []
        itemQueue = queue.Queue()
        itemQueue.put(root)
        while itemQueue.empty() == False:
            node = itemQueue.get()
            itemList.append(node)
            nodeList = node.children
            for item in nodeList:
                child = FamilyNode()
                child.nodeInfo = PersonInfo()
                indentify = indentify + 1
                child.nodeInfo.name = item["name"]
                child.nodeInfo.code = item["code"]
                child.children = item["children"]
                child.indentify = indentify
                child.parentId = node.indentify
                itemQueue.put(child)
    #s = open("data.txt","r")
    s = input()
    print(s)
    #s.close()
    ss = getname(s)
    name = ss[0]
    print(name)
    phone = getphone(s)
    address = getdetailaddress(ss,phone)
    print(address)
main()

