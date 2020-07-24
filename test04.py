import uuid

from sklearn import model_selection
import statsmodels.api as sm
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import preprocessing
from time import *

from analysis.linear.prediction import prediction

Profit = pd.read_excel(r'D:\亚龙展旗\项目\spss(多元回归分析)\本地版回归分析\中华烘丝0706七批数据对应.xlsx')
start = time()
print(start)
columns = Profit.columns.values.tolist()
end = time()
print(end)
print(end-start)
# Profit = Profit.drop(["批次号", "日期", "时间", "批内序号", "管路"], axis=1)
# Profit.head()
#
# train, test = model_selection.train_test_split(Profit, test_size=0.2, random_state=22)
#
# x = train.drop("叶丝干燥（薄板式）含水率 ", axis=1)
# X = sm.add_constant(x)
#
# y = train["叶丝干燥（薄板式）含水率 "]
# est = sm.OLS(y, X)
# est = est.fit()
# #print(est.summary())

sheets = pd.ExcelFile(r'D:\亚龙展旗\项目\spss(多元回归分析)\本地版回归分析\中华烘丝0706七批数据对应.xlsx').sheet_names
for sheet in sheets:
    uid = str(uuid.uuid4())
    fid = ''.join(uid.split('-'))
    filedata = {}
    p = pd.read_excel(r'D:\亚龙展旗\项目\spss(多元回归分析)\本地版回归分析\中华烘丝0706七批数据对应.xlsx',sheet)
    columns = p.columns.values.tolist()
    filedata["Profit"] = p
    endtime = time()
    print("endtime: " + str(endtime))