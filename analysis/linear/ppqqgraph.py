"""
返回pp图和qq图
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

def pp(fileindex,yselected):
    import matplotlib
    matplotlib.use('Agg')
    from matplotlib import pyplot as plt
    conn = getconn()
    newProfit = pickle.loads(conn.hget(fileindex, 'Profit'))
    y = newProfit[yselected]
    pq_plot = sm.ProbPlot(y)
    pq_plot.ppplot(line='45')
    plt.title('PP图')
    sio = BytesIO()
    plt.savefig(sio, format='png', bbox_inches='tight', pad_inches=0.0)
    data = base64.encodebytes(sio.getvalue()).decode()
    src = 'data:image/png;base64,' + str(data)
    # 记得关闭，不然画出来的图是重复的
    plt.axis('off')
    plt.close()
    return src

def qq(fileindex,yselected):
    import matplotlib
    matplotlib.use('Agg')
    from matplotlib import pyplot as plt
    conn = getconn()
    newProfit = pickle.loads(conn.hget(fileindex, 'Profit'))
    y = newProfit[yselected]
    pq_plot = sm.ProbPlot(y)
    pq_plot.qqplot(line='q')
    plt.title('QQ图')
    sio = BytesIO()
    plt.savefig(sio, format='png', bbox_inches='tight', pad_inches=0.0)
    data = base64.encodebytes(sio.getvalue()).decode()
    src = 'data:image/png;base64,' + str(data)
    # 记得关闭，不然画出来的图是重复的
    plt.axis('off')
    plt.close()
    return src