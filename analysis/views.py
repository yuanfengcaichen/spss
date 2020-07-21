import copy

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
import json
import pandas as pd
# Create your views here.
from analysis.linear.linearcorrelationgraph import linear_correlation
from analysis.linear.outliertest import outliertest
from analysis.linear.ppqqgraph import pp, qq
from analysis.linear.prediction import prediction
from analysis.linear.regression import analysis, returncloumns, normality, multicol, norks

import base64
from io import BytesIO
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

#fileList=[]
from analysis.linear.residual import residual
from analysis.linear.variance import variance, varbp

Profit=[]
def index(request):#返回多元线性回归网页
    return render(request, 'index.html')
    title = '探索性数据分析箱型图'
    matplotlib.use('Agg')  # 不出现画图的框
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 这两行用来显示汉字
    plt.rcParams['axes.unicode_minus'] = False
    sns.boxplot([133, 123, 899, 198, 849, 180, 844])  # 箱线图
    plt.title(title, loc='center')
    sio = BytesIO()
    plt.savefig(sio, format='png', bbox_inches='tight', pad_inches=0.0)
    data = base64.encodebytes(sio.getvalue()).decode()
    src = 'data:image/png;base64,' + str(data)
    # 记得关闭，不然画出来的图是重复的
    plt.close()
    return render(request, 'index.html', {"src": src})
def uploadfile(request):#用户上传文件，返回文件中的列名
    global Profit
    file = request.FILES.get("file")
    filename = file.name
    #print(type(file))
    sheets = pd.ExcelFile(file).sheet_names
    resultdatas=[]
    for sheet in sheets:
        p = returncloumns(file,sheet)
        columns = p.columns.values.tolist()
        Profit.append(p)
        d={"Profit":p}
        fileindex = len(Profit)-1
        resultdata=[filename+'-'+sheet,columns,fileindex]
        resultdatas.append(resultdata)
    #print(resultdatas)
    ret1 = json.loads(json.dumps(resultdatas, ensure_ascii=False))
    # p=returncloumns(file)
    # columns=p.columns.values.tolist()
    # Profit.append(p)
    # fileindex = len(Profit)-1
    # resultdata=[filename,columns,fileindex]
    # ret1 = json.loads(json.dumps(resultdata, ensure_ascii=False))
    return JsonResponse({"result": 1,"resultdata":ret1}, json_dumps_params={'ensure_ascii': False})

def sendselect(request):#用户选择x轴和y轴，进行回归分析，返回模型数据
    if request.method == "POST":
        #print(request.body)
        data=json.loads(request.body)
        fileindex = data["fileindex"]
        xselected = data["xselected"]
        yselected = data["yselected"]
        global Profit
        #print(fileindex)
        f=analysis(copy.deepcopy(Profit[fileindex]),xselected,yselected)
        model = json.loads(json.dumps(f.get('model').summary().as_html(), ensure_ascii=False))
        responsedata = {"result": 1, "model": model,"f1":f.get('f1'),"f2":f.get('f2')}
        return JsonResponse(responsedata, json_dumps_params={'ensure_ascii': False})

def getprediction(request):#获取模型预测图片
    if request.method == "POST":
        data = json.loads(request.body)
        fileindex = data["fileindex"]
        xselected = data["xselected"]
        yselected = data["yselected"]
        prediction_src = prediction(Profit[fileindex],xselected,yselected)
        responsedata = {"prediction_src": prediction_src}
        return JsonResponse(responsedata, json_dumps_params={'ensure_ascii': False})

def getnormality(request):#获取正态性检验的图片
    if request.method == "POST":
        data = json.loads(request.body)
        fileindex = data["fileindex"]
        xselected = data["xselected"]
        yselected = data["yselected"]
        global Profit
        normality_src = normality(Profit[fileindex], yselected)
        responsedata = {"normality_src":normality_src}
        return JsonResponse(responsedata, json_dumps_params={'ensure_ascii': False})

def getppqq(request):#获取qqpp图片地址
    if request.method == "POST":
        data = json.loads(request.body)
        fileindex = data["fileindex"]
        xselected = data["xselected"]
        yselected = data["yselected"]
        global Profit
        pp_src = pp(Profit[fileindex], yselected)
        qq_src = qq(Profit[fileindex], yselected)
        responsedata = {"pp_src":pp_src,"qq_src":qq_src,}
        return JsonResponse(responsedata, json_dumps_params={'ensure_ascii': False})

def getks(request):
    if request.method == "POST":
        data = json.loads(request.body)
        fileindex = data["fileindex"]
        xselected = data["xselected"]
        yselected = data["yselected"]
        global Profit
        ks = norks(Profit[fileindex],yselected)
        responsedata = {"ks": ks}
        return JsonResponse(responsedata, json_dumps_params={'ensure_ascii': False})

def getmulticol(request):#获取多重共线性表格数据
    if request.method == "POST":
        data = json.loads(request.body)
        fileindex = data["fileindex"]
        xselected = data["xselected"]
        yselected = data["yselected"]
        global Profit
        multicollinearity = multicol(Profit[fileindex], xselected)
        multicollinearity = json.loads(json.dumps(multicollinearity, ensure_ascii=False))
        responsedata = {"multicollinearity":multicollinearity}
        return JsonResponse(responsedata, json_dumps_params={'ensure_ascii': False})

def getlinearcorrelate(request):#获取线性相关性图片
    if request.method == "POST":
        data = json.loads(request.body)
        fileindex = data["fileindex"]
        lineselected = data["lineselected"]
        global Profit
        linear_correlation_src = linear_correlation(Profit[fileindex],lineselected)
        responsedata = {"linear_correlation_src": linear_correlation_src}
        return JsonResponse(responsedata, json_dumps_params={'ensure_ascii': False})

def getoutliertest(request):#获取异常值检测模型
    if request.method == "POST":
        data = json.loads(request.body)
        fileindex = data["fileindex"]
        xselected = data["xselected"]
        yselected = data["yselected"]
        global Profit
        f = outliertest(copy.deepcopy(Profit[fileindex]), xselected, yselected)
        testmodel = json.loads(json.dumps(f, ensure_ascii=False))
        responsedata = {"result": 1, "testmodel": testmodel, }
        return JsonResponse(responsedata, json_dumps_params={'ensure_ascii': False})

def getresidual(request):#获取残差独立性相关数据
    if request.method == "POST":
        data = json.loads(request.body)
        fileindex = data["fileindex"]
        xselected = data["xselected"]
        yselected = data["yselected"]
        global Profit
        dw = residual(Profit[fileindex], xselected, yselected)
        responsedata = {"dw": dw}
        return JsonResponse(responsedata, json_dumps_params={'ensure_ascii': False})

def getbp(request):
    if request.method == "POST":
        data = json.loads(request.body)
        fileindex = data["fileindex"]
        xselected = data["xselected"]
        yselected = data["yselected"]
        global Profit
        bp = varbp(Profit[fileindex], xselected, yselected)
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
        global Profit
        variance_src = variance(Profit[fileindex],xselected, yselected,oselected_1,oselected_2)
        responsedata = {"variance_src": variance_src}
        return JsonResponse(responsedata, json_dumps_params={'ensure_ascii': False})
