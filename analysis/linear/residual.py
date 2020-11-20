"""
返回残差独立性相关数据
"""

from sklearn import model_selection
import statsmodels.api as sm
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import preprocessing

from analysis.linear.curmodel import setcurmodel
#redis模块
from analysis.tools.myredis import getconn
import pickle

def residual(fileindex,xselected,yselected):
    conn = getconn()
    if conn.hexists(fileindex, 'est2'):
        est2 = pickle.loads(conn.hget(fileindex, 'est2'))
    else:
        est2 = None
    if (est2 != None):
        from statsmodels.stats.stattools import (durbin_watson)
        DW = ["%#8.3f" % durbin_watson(est2.wresid)]
        return DW
    else:
        setcurmodel(fileindex, xselected, yselected)
        data = residual(fileindex, xselected, yselected)
        return data