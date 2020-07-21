"""
获取模型
"""
from sklearn import model_selection
import statsmodels.api as sm
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import base64
from io import BytesIO
import pandas as pd
import numpy as np

def setmodel(Profit,xselected,yselected):
    train, test = model_selection.train_test_split(Profit, test_size=0.2, random_state=22)

    x = train[xselected]
    X = sm.add_constant(x)

    y = train[yselected]
    est = sm.OLS(y, X)
    est = est.fit()
    return est