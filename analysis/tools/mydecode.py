#将二进制数据转为正常的数据
def mapdecode(map):
    newmap = {}  # 转换后的数据
    for key, values in map.items():
        newkey = key.decode()
        newvalue = values.decode()
        newmap[newkey] = newvalue
    return  newmap

def mapkeydecode(map):
    newmap = {}  # 转换后的数据
    for key, values in map.items():
        newkey = key.decode()
        newmap[newkey] = values
    return  newmap

def mapvaluedecode(map):
    newmap = {}  # 转换后的数据
    for key, values in map.items():
        newvalue = values.decode()
        newmap[key] = newvalue
    return  newmap

def listdecode(list):
    newlist = []
    for item in list:
        newlist.append(item.decode())
    return newlist