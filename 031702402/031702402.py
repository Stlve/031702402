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
def getlevel(s):
    level = s.split("!")
    return level
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
    p = re.compile(r'.+(路|街|巷|桥|岛){1}')
    roadmatch = p.search(new4)

    if roadmatch != None:    
        road = roadmatch.group(0)
    else :
        road = ""
    #print(road)
    return road


def getnumber(new6):
    pp = re.compile(r'.+(号|\d){1}')
    numbermatch = pp.search(new6)
    if numbermatch != None:
        number = numbermatch.group(0)
    else :
        number = ""
   # print(number)
    return number
def findarea(aareas,new2):
    #areas是现在的所有的县，new2是现在只有乡以后的地址
    atown = new2[0]+new2[1]
    #print(atown)
    for aarea in aareas:#县
        atowns = aarea['children']
        for aatown in atowns:#县下面的镇/乡
            if aatown['name'].find(atown) != -1:
                #print(aatown['name'])
                return aarea['children']
def findcity(cities,new1):
    #cities是现在所有的市，new1是现在的县的地址
    aarea = new1[0]+new1[1]
    #print(aarea)
    for acity in cities:
        #市
        aareas = acity['children']
        for abrea in aareas:
            if abrea['name'].find(aarea) != -1:
                #print(acity['name'])
                return acity['children']


def main():
    data = {"姓名":"",
        "手机":"",
        "地址":[]
    }
    towns = []
    result = Result()
    s = input()
    num = getlevel(s)
    number = num[0]
    #print(number)
    s = num[1]
    #print(s)
    # s.close()
    ss = getname(s)
    names = ss[0]
    result.name = names
    data["姓名"] = result.name
    #print(names)
    phone = getphone(s)
    result.phone = phone
    data["手机"] = result.phone
    address = getdetailaddress(ss, phone)
    address = address[:-1]
    detail = ""
    #print(address)
    # 开始处理json文件
    data_json = {}
    filepath = os.path.split(os.path.realpath(__file__))[0]
    filepath = filepath + "\\" + "pcas-code.json"
    with open(filepath,"r+",encoding='utf-8_sig')as f:
        data_json = json.load(f)
        for province in data_json:  #省份
            one = address[0] + address[1]
            if province['name'].find(one) != -1:  # 是他的子集
                # print("yes,i find province")
                result.province = province['name']
                #print(result.province)
                new1 = cutSame(address, result.province)
                new3 = new1
                new2 = new1
                #print(new1)
                #如果是直辖市的话
                if result.province == "北京"or result.province == "重庆"or result.province == "天津"or result.province == "上海":
                    new1 = result.province + new1
                cities = province['children']
        if result.province == "":
            print("no find province")
            return 
        for city in cities:  #市
            two = new1[0] + new1[1]
            if city['name'].find(two) != -1 :
                result.city = city['name']
                #print(result.city)
                new2 = cutSame(new1,result.city)
                # print(new2)
                areas = city['children']
                #print(areas)
                new3 = new2
        if result.city == "":
            result.city = ""
            areas = findcity(cities,new1)
            new3 = new1
            if areas == {}:
                return 
        for area in areas:  #县
            three = new2[0] + new2[1]
            if area['name'].find(three) != -1:
                result.area = area['name']
                #print(result.area)
                new3 = cutSame(new2, result.area)
                # print(new3)
                towns = area['children']
                #如果县级没有被找到的话
        if result.area == "":
            result.area = ""
            towns = findarea(areas,new2)
            new4 = new3
            if towns == {}:
                return 
        for town in towns: #乡
            four = new3[0] + new3[1]
            if town['name'].find(four) != -1:
                result.town = town['name']
                # print(result.town)
                new4 = cutSame(new3,result.town)
        if result.town == "":
            result.town = ""
            new4 = new3
            #如果乡没有被找到的话
            #print(new4)
        detail = new4
        if number == "1" :
        #五级地址
            data["地址"] = [result.province,result.city,result.area,result.town,detail]
            json_str = json.dumps(dict(data),ensure_ascii=False)
            print(json_str)
        else :
            #七级地址
            result.road = getroad(new4)
            new6 = cutSame(new4, result.road)
            #print(new6)
            result.number = getnumber(new6)
                #如果号找不到的话
            if result.number == "":
                result.number = ""
                result.last = new6
            else:
                result.last = cutSame(new6, result.number)
                # print(result.last)
            data["地址"] = [result.province,result.city,result.area,result.town,result.road,result.number,result.last]
            json_str = json.dumps(dict(data),ensure_ascii=False)
            print(json_str)
main()
