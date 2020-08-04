import requests
import json

ls2=[1,2,3,4,5,6,7]
ls1=['4','5','89','1']
print(dict(zip(ls1,ls2)))
l3 = ls1
l3.append("123")
print(l3)
L = ['Adam', 'Lisa', 'Bart']
L.append('Paul')
print (L)

ip = '223.75.252.198'

url = 'https://api.map.baidu.com/location/ip?ak=rGa0BEvgESYRDkgTLSIwkwHN5zkLfGcA&ip='+ip+'&coor=bd09ll'  # 请求接口
req = requests.get(url)#发送请求
data = req.json()
print(data)
print(data.get("content").get("address"))