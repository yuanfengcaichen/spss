"""
returncloumns：返回excel表中的列名
analysis：返回model模型数据
normality：返回正态性检验图片
multicol：返回多重共线性检测相关数据
"""

from sklearn import model_selection
import statsmodels.api as sm
import pandas as pd
import numpy as np
from sklearn import preprocessing
import seaborn as sns
import scipy.stats as stats
from pylab import *
import base64
from io import BytesIO
import copy
from analysis.tools.myredis import getconn
import pickle
from analysis.linear.model import setmodel


def returncloumns(file,sheet):#返回读取的文件内容
    #print(pd.ExcelFile(file).sheet_names)
    Profit = pd.read_excel(file,sheet_name=sheet)
    values = dict([(col_name, col_mean) for col_name, col_mean in
                   zip(Profit.columns.tolist(), Profit.mean().tolist())])  # 参看1，生成字典，key为列名，value为列对应的均值
    Profit.fillna(value=values, inplace=True)  # 参看2，填充空值，value这里选择为字典形式，字典的key指明列，字典的value指明填充该列所用的值
    round(Profit,3)
    return Profit

def analysis(fileindex,xselected,yselected,analytype,criterion,direction):#根据文件和选择的x值和y值，生成model
    conn = getconn()

    train = pickle.loads(conn.hget(fileindex, 'train'))
    test = pickle.loads(conn.hget(fileindex, 'test'))
    est = pickle.loads(conn.hget(fileindex, 'est'))
    if conn.hexists(fileindex, 'xselected_change'):
        xselected_change = pickle.loads(conn.hget(fileindex, 'xselected_change'))
    else:
        xselected_change = 'None'
    if(est!=None):
        #理论f值
        from scipy.stats import f
        p = est.df_model  # 自变量个数
        n = train.shape[0]  # 行数，观测个数
        F_Theroy = f.ppf(q=0.95, dfn=p, dfd=n - p - 1)

        return {'model':est,'f1':round(est.fvalue, 3),'f2':round(F_Theroy, 3),'xselected_change':xselected_change}
    else:
        setmodel(fileindex,xselected,yselected,analytype,criterion,direction)
        data = analysis(fileindex,xselected,yselected,analytype,criterion,direction)
        return data

def normality(fileindex,yselected):#正态性检验
    import matplotlib
    matplotlib.use('Agg')
    from matplotlib import pyplot as plt
    import seaborn as sns
    conn = getconn()
    newProfit=pickle.loads(conn.hget(fileindex,'Profit'))
    y = newProfit[yselected]
    mpl.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    sns.distplot(a=y,
                 bins=10,
                 fit=stats.norm,
                 norm_hist=True,
                 hist_kws={'color': 'green', 'edgecolor': 'black',},
                 kde_kws={'color': 'black', 'linestyle': '--', 'label': '核密度曲线'},
                 fit_kws={'color': 'red', 'linestyle': ':', 'label': '正态密度曲线'}
                 )
    plt.legend()
    sio = BytesIO()
    plt.savefig(sio, format='png', bbox_inches='tight', pad_inches=0.0)
    data = base64.encodebytes(sio.getvalue()).decode()
    src = 'data:image/png;base64,' + str(data)
    # 记得关闭，不然画出来的图是重复的
    plt.axis('off')
    plt.close()
    return src

def norks(fileindex,yselected):#正态性检验的K-S检验
    conn = getconn()
    train = pickle.loads(conn.hget(fileindex, 'train'))
    test = pickle.loads(conn.hget(fileindex, 'test'))
    if(len(train)>=5000):
        data = stats.kstest(rvs=train[yselected], args=(train[yselected].mean(), train[yselected].std()),
        cdf="norm")
        type='kstest'
    else:
        data = stats.shapiro(train[yselected])
        type='shapiro'
    #return {'type':type,'data':round(data,3)}
    return {'type': type, 'data': data}

def multicol(fileindex,xselected):# 返回的是二维数组
    conn = getconn()
    newProfit = pickle.loads(conn.hget(fileindex, 'Profit'))
    if conn.hexists(fileindex, 'xselected_change'):
        xselected_change = pickle.loads(conn.hget(fileindex, 'xselected_change'))
    else:
        xselected_change = None
    if (xselected_change == None):  # 没有xselected_change证明是线性回归
        x = newProfit[xselected]
    else:
        x = newProfit[xselected_change]
    from statsmodels.stats.outliers_influence import variance_inflation_factor
    X = sm.add_constant(x.loc[:, :])
    vif = pd.DataFrame()
    vif['features'] = X.columns
    vif["VIF Factor"] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
    return round(vif,3).values.tolist()#将ndarray类型转为list

