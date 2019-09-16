import string
import re
import json
import os
import demjson
class result:
    province = ""
    city = ""
    area = ""
    town = ""
    new5 = ""
    new7 = ""
    last = ""
    detail = ""
    
    
def getname(s):
    ss = s.split(",")
    return ss
def getphone(s):
    pat = re.compile(r'[1-9]\d{10}')
    phonematch = pat.search(s)
    phone = phonematch.group(0)
    #print(phone)
    return phone
def getdetailaddress(ss,phone):
    addressplit = ss[1].split(phone)
    #print(addressplit)
    sep = ''
    address = sep.join(addressplit)
    return address
def cutSame(address,province):
    if len(address)<len(province):
        leng = len(address)
    else:
        leng = len(province)
    i = 0
    while i<leng:
        if address[i] != province[i]:
            break
        i = i+1
    return address[i:]
def getnew5(new4):
    p = re.compile(r'.+(路|街|巷){1}')
    new5match = p.search(new4)
    new5 = new5match.group(0)
    #print(new5)
    return new5
    
def getnew7(new6):
    pp = re.compile(r'.+(号){1}')
    new7match = pp.search(new6)
    new7 = new7match.group(0)
    #print(new7)
    return new7
def main():
    #s = open("data.txt","r")
    s = input()
    #print(s)
    #s.close()
    ss = getname(s)
    names = ss[0]
    print(names)
    phone = getphone(s)
    address = getdetailaddress(ss,phone)
    address = address[:-1]
    print(address)
    #开始处理json文件
    f = open('pcas-code.json',encoding='utf-8')
    provincelist = json.load(f)
   
    for province in provincelist:
        one = address[0]+address[1]
        if province['name'].find(one) != -1: #是他的子集
            #print("yes,i find province")
            result.province = province['name']
            #print(result.province)
            new1 = cutSame(address,result.province)
            #print(new1)
            cities = province['children']
            for city in cities:
                two = new1[0]+new1[1]
                if city['name'].find(two)!=-1:
                    result.city = city['name']
                    #print(result.city)
                    new2 = cutSame(new1,result.city)
                    #print(new2)
                    areas = city['children']
                    for area in areas:
                        three = new2[0]+new2[1]
                        if area['name'].find(three)!=-1:
                            result.area = area['name']
                            #print(result.area)
                            new3 = cutSame(new2,result.area)
                           # print(new3)
                            towns = area['children']
                            for town in towns:
                                four = new3[0]+new3[1]
                                if town['name'].find(four)!=-1:
                                    result.town = town['name']
                                  #  print(result.town)
                                    new4 = cutSame(new3,result.town)
                                    print(new4)
                                    result.detail = new4
    
    result.new5 = getnew5(new4)
    new6 = cutSame(new4,result.new5)
    #print(new6)
    result.new7 = getnew7(new6)
    result.last = cutSame(new6,result.new7)
    print(result.last)
    print()
    
main()


