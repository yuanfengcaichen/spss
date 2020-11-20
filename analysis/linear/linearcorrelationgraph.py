"""
返回线性相关性检测图片
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
#redis模块
from analysis.tools.myredis import getconn
import pickle

def linear_correlation(fileindex,lineselected):
    import matplotlib
    matplotlib.use('Agg')
    from matplotlib import pyplot as plt
    conn = getconn()
    newProfit = pickle.loads(conn.hget(fileindex, 'Profit'))
    linedata = newProfit[lineselected].corr()
    #print(linedata)
    sns.pairplot(newProfit.loc[:, lineselected])
    sio = BytesIO()
    plt.savefig(sio, format='png', bbox_inches='tight', pad_inches=0.0)
    data = base64.encodebytes(sio.getvalue()).decode()
    src = 'data:image/png;base64,' + str(data)
    # 记得关闭，不然画出来的图是重复的
    plt.axis('off')
    plt.close()
    return {'src':src,'lindata':round(linedata,3).values.tolist()}