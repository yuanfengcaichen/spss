"""
返回方差齐性检验图片
"""
import base64
import copy
from io import BytesIO
from sklearn import model_selection
import statsmodels.api as sm
import pandas as pd
import numpy as np
import matplotlib

from analysis.linear.curmodel import setcurmodel
#redis模块
from analysis.tools.myredis import getconn
import pickle
matplotlib.use('Agg')
from matplotlib import pyplot as plt
from sklearn import preprocessing
def varbp(fileindex, xselected, yselected):
    conn = getconn()
    if conn.hexists(fileindex, 'est2'):
        est2 = pickle.loads(conn.hget(fileindex, 'est2'))
    else:
        est2 = None
    if (est2 != None):
        BP = sm.stats.diagnostic.het_breuschpagan(est2.resid, exog_het=est2.model.exog)
        return BP
    else:
        setcurmodel(fileindex, xselected, yselected)
        data = varbp(fileindex, xselected, yselected)
        return data


def variance(fileindex, xselected, yselected,oselected_1,oselected_2):
    conn = getconn()
    if conn.hexists(fileindex, 'est2'):
        est2 = pickle.loads(conn.hget(fileindex, 'est2'))
    else:
        est2 = None
    if conn.hexists(fileindex, 'none_outliers'):
        none_outliers = pickle.loads(conn.hget(fileindex, 'none_outliers'))
    else:
        none_outliers = None

    # 残差方差齐性检验 )
    ax1 = plt.subplot2grid(shape=(2, 1), loc=(0, 0))  # 设置第一张子图位置
    # 散点图绘制
    # 学生化残差与自变量散点图
    # ax1.scatter(none_outliers["蒸汽流量 "], none_outliers.resid_stu
    # 标准化残差和自变量散点图
    ax1.scatter(none_outliers[oselected_1], (est2.resid - est2.resid.mean()) / est2.resid.std())
    # 添加水平参考线
    ax1.hlines(y=0,
               xmin=none_outliers[oselected_1].min(),
               xmax=none_outliers[oselected_1].max(),
               color='red',
               linestyle='--'
               )
    ax1.set_xlabel(oselected_1)
    ax1.set_ylabel('Std_Residual')

    ax2 = plt.subplot2grid(shape=(2, 1), loc=(1, 0))
    # 学生化残差与自变量散点图
    # ax2.scatter(none_outliers["拔风压力PID阀门开度 "], none_outliers.resid_stu )
    # 标准化残差和自变量散点图
    ax2.scatter(none_outliers[oselected_2], (est2.resid - est2.resid.mean()) / est2.resid.std())
    ax2.hlines(y=0,
               xmin=none_outliers[oselected_2].min(),
               xmax=none_outliers[oselected_2].max(),
               color='magenta',
               linestyle='--'
               )
    ax2.set_xlabel(oselected_2)
    ax2.set_ylabel('Std_Residual')

    # 调整2子图之间距离
    plt.subplots_adjust(hspace=0.6, wspace=0.3)
    sio = BytesIO()
    plt.savefig(sio, format='png', bbox_inches='tight', pad_inches=0.0)
    data = base64.encodebytes(sio.getvalue()).decode()
    src = 'data:image/png;base64,' + str(data)
    # 记得关闭，不然画出来的图是重复的
    plt.axis('off')
    plt.close()
    return src

