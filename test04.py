from sklearn import model_selection
import statsmodels.api as sm
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import preprocessing

from analysis.linear.prediction import prediction

Profit = pd.read_excel(r'D:\亚龙展旗\spss\本地版回归分析\中华烘丝0706七批数据对应.xlsx')
Profit.head()

Profit = Profit.drop(["批次号", "日期", "时间", "批内序号", "管路"], axis=1)
Profit.head()

train, test = model_selection.train_test_split(Profit, test_size=0.2, random_state=22)

x = train.drop("叶丝干燥（薄板式）含水率 ", axis=1)
X = sm.add_constant(x)

y = train["叶丝干燥（薄板式）含水率 "]
est = sm.OLS(y, X)
est = est.fit()
#print(est.summary())


#回归模型预测
x_test = test.drop("叶丝干燥（薄板式）含水率 ", axis=1)
y_test = test["叶丝干燥（薄板式）含水率 "]
X_test = sm.add_constant(x_test)
y_pred = est.predict(X_test)

plt.scatter(y_test, y_pred)
plt.plot([y_test.min(), y_test.max()],
         [y_test.min(), y_test.max()],
         color='red',
         linestyle='--')
plt.xlabel('实际值')
plt.ylabel('预测值')
plt.show()