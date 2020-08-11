import copy
import threading
import uuid
from time import *
import requests
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
import json
import pandas as pd
# Create your views here.
from analysis.linear.curmodel import setcurmodel
from analysis.linear.linearcorrelationgraph import linear_correlation
from analysis.linear.model import setmodel
from analysis.linear.outliertest import outliertest
from analysis.linear.ppqqgraph import pp, qq
from analysis.linear.prediction import prediction
from analysis.linear.regression import analysis, returncloumns, normality, multicol, norks

from openpyxl import load_workbook
import xlrd
from django.core.files.base import ContentFile
import base64
from io import BytesIO
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

#fileList=[]
from analysis.linear.residual import residual
from analysis.linear.variance import variance, varbp
from analysis.models import Red


def getaddress(id,ip):
    url = 'https://api.map.baidu.com/location/ip?ak=rGa0BEvgESYRDkgTLSIwkwHN5zkLfGcA&ip='+ip+'&coor=bd09ll'  # 请求接口
    req = requests.get(url)#发送请求
    data = req.json()
    #print(ip + "----" + data.get("content").get("address"))#获取请求，得到的是字典格式

def savefile(file,sheet,fid):
    global Files
    filedata = {}
    p = returncloumns(file, sheet)
    filedata["Profit"] = p
    Files[fid]=filedata

Files={}
def index(request):#返回多元线性回归网页
    # x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')  # 判断是否使用代理
    # if x_forwarded_for:
    #     ip = x_forwarded_for.split(',')[0]  # 使用代理获取真实的ip
    # else:
    #     ip = request.META.get('REMOTE_ADDR')  # 未使用代理获取IP
    # t1 = threading.Thread(target=getaddress, args=(1,ip))  # 新开一个线程获取访问地址
    # t1.start()
    # l = pd.DataFrame(list(Red.objects.all())) # 使用数据库读取数据
    # print(type(l))
    # for a in l:
    #     pass
    return render(request, 'index.html')

def linear(request):
    return render(request, 'regression_index.html')
def gradually(request):
    return render(request, 'regression_index.html')

def uploadfile(request):#用户上传文件，返回文件中的列名
    global Files
    file = request.FILES.get("file")
    filename = file.name
    tables = load_workbook(file)
    sheets = tables.sheetnames
    resultdatas=[]
    for sheet in sheets:
        uid = str(uuid.uuid4())
        fid = ''.join(uid.split('-'))
        copyfile = copy.deepcopy(file)
        t1 = threading.Thread(target=savefile, args=(copyfile,sheet,fid))  # 新开一个线程保存读取的文件
        t1.start()
        table = tables.get_sheet_by_name(sheet)
        a = table.max_column
        columns = []
        for i in range(1, a + 1):
            columns.append(table.cell(row=1,column=i).value)
        resultdata=[filename+'-'+sheet,columns,fid]
        resultdatas.append(resultdata)
    ret1 = json.loads(json.dumps(resultdatas, ensure_ascii=False))
    return JsonResponse({"result": 1,"resultdata":ret1}, json_dumps_params={'ensure_ascii': False})


def sendselect(request):#用户选择x轴和y轴，进行回归分析，返回模型数据
    if request.method == "POST":
        #print(request.body)
        data=json.loads(request.body)
        fileindex = data["fileindex"]
        xselected = data["xselected"]
        yselected = data["yselected"]
        analytype = data["analytype"]
        criterion = data["criterion"]
        direction = data["direction"]
        global Files
        i=0
        for i in range(5):
            if(fileindex in Files):
                return sendselecthelp(Files, fileindex, xselected, yselected, analytype, criterion, direction)
            else:
                sleep(1)
                #print("休息1s")
        return None

def sendselecthelp(Files, fileindex, xselected, yselected, analytype, criterion, direction):
    t1 = threading.Thread(target=setmodel, args=(
        Files, fileindex, xselected, yselected, analytype, criterion, direction))  # 新开一个线程获取模型
    t1.start()
    t1.join()
    t2 = threading.Thread(target=setcurmodel, args=(Files, fileindex, xselected, yselected))  # 新开一个线程获取修正后的模型
    t2.start()
    f = analysis(Files, fileindex, xselected, yselected, analytype, criterion, direction)
    model = json.loads(json.dumps(f.get('model').summary().as_html(), ensure_ascii=False))
    responsedata = {"result": 1, "model": model, "f1": f.get('f1'), "f2": f.get('f2')}
    return JsonResponse(responsedata, json_dumps_params={'ensure_ascii': False})


def getprediction(request):#获取模型预测图片
    if request.method == "POST":
        data = json.loads(request.body)
        fileindex = data["fileindex"]
        xselected = data["xselected"]
        yselected = data["yselected"]
        global Files
        prediction_src = prediction(Files,fileindex,xselected,yselected)
        responsedata = {"prediction_src": prediction_src}
        return JsonResponse(responsedata, json_dumps_params={'ensure_ascii': False})

def getnormality(request):#获取正态性检验的图片
    if request.method == "POST":
        data = json.loads(request.body)
        fileindex = data["fileindex"]
        xselected = data["xselected"]
        yselected = data["yselected"]
        global Files
        normality_src = normality(Files.get(fileindex).get("Profit"), yselected)
        responsedata = {"normality_src":normality_src}
        return JsonResponse(responsedata, json_dumps_params={'ensure_ascii': False})

def getppqq(request):#获取qqpp图片地址
    if request.method == "POST":
        data = json.loads(request.body)
        fileindex = data["fileindex"]
        xselected = data["xselected"]
        yselected = data["yselected"]
        global Files
        pp_src = pp(Files.get(fileindex).get("Profit"), yselected)
        qq_src = qq(Files.get(fileindex).get("Profit"), yselected)
        responsedata = {"pp_src":pp_src,"qq_src":qq_src,}
        return JsonResponse(responsedata, json_dumps_params={'ensure_ascii': False})

def getks(request):
    if request.method == "POST":
        data = json.loads(request.body)
        fileindex = data["fileindex"]
        xselected = data["xselected"]
        yselected = data["yselected"]
        global Files
        ks = norks(Files,fileindex,yselected)
        responsedata = {"ks": ks}
        return JsonResponse(responsedata, json_dumps_params={'ensure_ascii': False})

def getmulticol(request):#获取多重共线性表格数据
    if request.method == "POST":
        data = json.loads(request.body)
        fileindex = data["fileindex"]
        xselected = data["xselected"]
        yselected = data["yselected"]
        global Files
        multicollinearity = multicol(Files,fileindex, xselected)
        multicollinearity = json.loads(json.dumps(multicollinearity, ensure_ascii=False))
        responsedata = {"multicollinearity":multicollinearity}
        return JsonResponse(responsedata, json_dumps_params={'ensure_ascii': False})

def getlinearcorrelate(request):#获取线性相关性图片
    if request.method == "POST":
        data = json.loads(request.body)
        fileindex = data["fileindex"]
        lineselected = data["lineselected"]
        global Files
        linear_correlation_src = linear_correlation(Files.get(fileindex).get("Profit"),lineselected)
        responsedata = {"linear_correlation_src": linear_correlation_src}
        return JsonResponse(responsedata, json_dumps_params={'ensure_ascii': False})

def getoutliertest(request):#获取异常值检测模型
    if request.method == "POST":
        data = json.loads(request.body)
        fileindex = data["fileindex"]
        xselected = data["xselected"]
        yselected = data["yselected"]
        global Files
        f = outliertest(Files,fileindex, xselected, yselected)
        testmodel = json.loads(json.dumps(f, ensure_ascii=False))
        responsedata = {"result": 1, "testmodel": testmodel, }
        return JsonResponse(responsedata, json_dumps_params={'ensure_ascii': False})

def getresidual(request):#获取残差独立性相关数据
    if request.method == "POST":
        data = json.loads(request.body)
        fileindex = data["fileindex"]
        xselected = data["xselected"]
        yselected = data["yselected"]
        global Files
        dw = residual(Files,fileindex, xselected, yselected)
        responsedata = {"dw": dw}
        return JsonResponse(responsedata, json_dumps_params={'ensure_ascii': False})

def getbp(request):
    if request.method == "POST":
        data = json.loads(request.body)
        fileindex = data["fileindex"]
        xselected = data["xselected"]
        yselected = data["yselected"]
        global Files
        bp = varbp(Files,fileindex, xselected, yselected)
        responsedata = {"bp": bp}
        return JsonResponse(responsedata, json_dumps_params={'ensure_ascii': False})

def getvariance(request):#获取方差齐性检验图片：
    if request.method == "POST":
        data = json.loads(request.body)
        fileindex = data["fileindex"]
        xselected = data["xselected"]
        yselected = data["yselected"]
        oselected_1 = data["oselected_1"]
        oselected_2 = data["oselected_2"]
        global Files
        variance_src = variance(Files,fileindex, xselected, yselected,oselected_1,oselected_2)
        responsedata = {"variance_src": variance_src}
        return JsonResponse(responsedata, json_dumps_params={'ensure_ascii': False})
