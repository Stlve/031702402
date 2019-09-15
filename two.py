import string
import re
import json
import os


class Result:
    name = ""
    phone = ""
    province = ""
    city = ""
    area = ""
    town = ""
    road = ""
    number = ""
    last = ""


def getname(s):
    ss = s.split(",")
    return ss


def getphone(s):
    pat = re.compile(r'[1-9]\d{10}')
    phonematch = pat.search(s)
    phone = phonematch.group(0)
    #print(phone)
    return phone


def getdetailaddress(ss, phone):
    addressplit = ss[1].split(phone)
    # print(addressplit)
    sep = ''
    address = sep.join(addressplit)
    return address


def cutSame(address, province):
    if len(address) < len(province):
        leng = len(address)
    else:
        leng = len(province)
    i = 0
    while i < leng:
        if address[i] != province[i]:
            break
        i = i + 1
    return address[i:]


def getroad(new4):
    p = re.compile(r'.+(路|街|巷|学|桥|岛){1}')
    roadmatch = p.search(new4)
    road = roadmatch.group(0)
    #print(road)
    return road


def getnumber(new6):
    pp = re.compile(r'.+(号|\d){1}')
    numbermatch = pp.search(new6)
    number = numbermatch.group(0)
   # print(number)
    return number


def main():
    result = Result()
    # s = open("data.txt","r")
    s = input()
    #print(s)
    # s.close()
    ss = getname(s)
    names = ss[0]
    result.name = names
    #print(names)
    phone = getphone(s)
    result.phone = phone
    address = getdetailaddress(ss, phone)
    address = address[:-1]
    #print(address)
    # 开始处理json文件
    filepath = os.path.split(os.path.realpath(__file__))[0]
    filepath = filepath + "\\" + "pcas-code.json"
    with open(filepath,"r+",encoding='utf-8_sig')as f:
        provincelist = json.load(f)
    for province in provincelist:
        one = address[0] + address[1]
        if province['name'].find(one) != -1:  # 是他的子集
            # print("yes,i find province")
            result.province = province['name']
            #print(result.province)
            new1 = cutSame(address, result.province)
            #print(new1)
            if result.province == "北京"or result.province == "重庆"or result.province == "天津"or result.province == "上海":
                new1 = result.province + new1
            cities = province['children']
            for city in cities:
                two = new1[0] + new1[1]
                if city['name'].find(two) != -1 :
                    result.city = city['name']
                    #print(result.city)
                    new2 = cutSame(new1,result.city)
                    # print(new2)
                    areas = city['children']
                    for area in areas:
                        three = new2[0] + new2[1]
                        if area['name'].find(three) != -1:
                            result.area = area['name']
                            #print(result.area)
                            new3 = cutSame(new2, result.area)
                            # print(new3)
                            towns = area['children']
                            for town in towns:
                                four = new3[0] + new3[1]
                                if town['name'].find(four) != -1:
                                    result.town = town['name']
                                   # print(result.town)
                                    new4 = cutSame(new3,result.town)
                                    #print(new4)
                                    detail = new4
                                    result.road = getroad(new4)
                                    new6 = cutSame(new4, result.road)
                                    #print(new6)
                                    result.number = getnumber(new6)
                                    result.last = cutSame(new6, result.number)
                                   # print(result.last)
    print(json.dumps(obj=result.__dict__,ensure_ascii=False))
main()
