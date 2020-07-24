from sklearn import model_selection
import statsmodels.api as sm
import statsmodels.regression.linear_model as Re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import preprocessing
from statsmodels.iolib.table import (SimpleTable, default_txt_fmt)



Profit = pd.read_excel(r'D:\亚龙展旗\模型诊断\上烟三车间0711.xlsx')
values = dict([(col_name, col_mean) for col_name, col_mean in zip(Profit.columns.tolist(), Profit.mean().tolist())]) # 参看1，生成字典，key为列名，value为列对应的均值
Profit.fillna(value=values, inplace=True) # 参看2，填充空值，value这里选择为字典形式，字典的key指明列，字典的value指明填充该列所用的值

# Profit[np.isnan(Profit)] = 0
# Profit[np.isinf(Profit)] = 0
Profit.head()
#Profit1=Profit.drop("叶丝干燥（薄板式）含水率 ",axis=1)
#Profit1
x=Profit["切叶丝宽度"]
y=Profit["82烟片松散回潮温度（出口处）"]
x_train,y_train,x_test,y_test = model_selection.train_test_split(x,y,test_size = 0.2,random_state=22)
X=sm.add_constant(x)
est=sm.OLS(y,X)
est=est.fit()
est.summary()
print(type(est))