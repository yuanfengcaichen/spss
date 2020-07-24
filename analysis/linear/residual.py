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


def residual(Files,fileindex,xselected,yselected):
    data = Files.get(fileindex)
    est2 = data.get("est2")
    if (est2 != None):
        from statsmodels.stats.stattools import (durbin_watson)
        DW = ["%#8.3f" % durbin_watson(est2.wresid)]
        return DW
    else:
        setcurmodel(Files, fileindex, xselected, yselected)
        data = residual(Files, fileindex, xselected, yselected)
        return data