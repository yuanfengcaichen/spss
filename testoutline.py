from sklearn import model_selection
import statsmodels.api as sm
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import preprocessing
from time import *

from analysis.linear.outliertest import outliertest
from analysis.linear.prediction import prediction
starttime = time()
Profit = pd.read_excel(r'D:\亚龙展旗\spss\本地版回归分析\中华烘丝0706七批数据对应.xlsx')
outliertest(Profit,["叶丝干燥（薄板式）含水率 ","物料流量 ","筒壁温度PID阀门开度 ","筒壁温度 "],"叶丝烘前含水率 ")