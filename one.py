import string
import re
import json
import os
import demjson

class Province:
    string name
    list<city> children
class City:
    string name
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
    f=open('pcas-code.json',encoding='utf-8')
    user_dic=json.load(f)
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

