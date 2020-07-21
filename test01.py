from sklearn import model_selection
import statsmodels.api as sm
import statsmodels.regression.linear_model as Re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import preprocessing
from statsmodels.iolib.table import (SimpleTable, default_txt_fmt)

Profit = pd.read_excel(r'D:\亚龙展旗\spss\本地版回归分析\中华烘丝0706七批数据对应.xlsx')
Profit.head()
Profit=Profit.drop(["批次号","日期","时间","批内序号","管路"],axis=1)
Profit.head()
train,test = model_selection.train_test_split(Profit,test_size = 0.2,random_state=22)

x=train.drop("叶丝干燥（薄板式）含水率 ",axis=1)
X=sm.add_constant(x)

y=train["叶丝干燥（薄板式）含水率 "]
est=sm.OLS(y,X)
est=est.fit()


# 异常值检测
outliers = est.get_influence()

# 帽子矩阵
leverage = outliers.hat_matrix_diag

# dffits值
dffits = outliers.dffits[0]

# 学生化残差
resid_stu = outliers.resid_studentized_external
# cook距离
cook = outliers.cooks_distance[0]

# 合并各种异常值检验的统计量值
contatl = pd.concat([pd.Series(leverage, name='leverage'),
                     pd.Series(dffits, name='dffits'),
                     pd.Series(resid_stu, name='resid_stu'),
                     pd.Series(cook, name='cook')
                     ], axis=1)

train.index = range(train.shape[0])
profit_outliers = pd.concat([train, contatl], axis=1)
print(profit_outliers)

outliers_ratio = np.sum(np.where((np.abs(profit_outliers.resid_stu) > 2), 1, 0)) / profit_outliers.shape[0]
print(outliers_ratio)

none_outliers = profit_outliers.loc[np.abs(profit_outliers.resid_stu) <= 2,]
print(none_outliers)

none_outliers = none_outliers.drop(["leverage", "dffits", "resid_stu", "cook"], axis=1)
x2 = none_outliers.drop("叶丝干燥（薄板式）含水率 ", axis=1)
y2 = none_outliers["叶丝干燥（薄板式）含水率 "]

X2 = sm.add_constant(x2.loc[:, :])
est2 = sm.OLS(y2, X2).fit()
est2.summary()
#print(est2.summary())
#print(x)

# pred4 = model4.predict(exog = test.ix[:,['RD_Spend','Marketing_Spend']])
# plt.scatter(x = test.Profit ,y = pred4)
# plt.plot([ test.Profit.min(),test.Profit.max()],
#          [test.Profit.min(),test.Profit.max()],
#         color = 'red',
#          linestyle = '--'
# )
# plt.xlabel('实际值')
# plt.ylabel('预测值')
# plt.show()
import seaborn as sns
import scipy.stats as stats
from pylab import *

'''
#正态性检验
mpl.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
sns.distplot(a = y,
            bins =10,
            fit = stats.norm,
            norm_hist = True,
            hist_kws = {'color':'green','edgecolor':'black','label':'直方图'},
            kde_kws = {'color':'black','linestyle':'--','label':'核密度曲线'},
            fit_kws = {'color':'red','linestyle':':','label':'正态密度曲线'}
           )
#plt.legend(['核密度曲线','正态密度曲线','直方图'])
plt.show()
'''
'''
#pp图和qq图ppplot qqplot
pq_plot = sm.ProbPlot(y)
pq_plot.ppplot(line='45')
plt.title('PP图')
pq_plot.qqplot(line='q')
plt.title('QQ图')
plt.show()
'''
'''
#多重共线性检验
from statsmodels.stats.outliers_influence import variance_inflation_factor
X = sm.add_constant(Profit1.loc[:,:])
vif = pd.DataFrame()
vif['features'] = X.columns
vif["VIF Factor"] = [variance_inflation_factor(X.values,i) for i in range(X.shape[1])]
print(vif)
print(vif.values[0])
'''
'''
#线性相关性检验
sns.pairplot(Profit.loc[:,:])
plt.show()
#数据框的corrwith方法(该方式优点是可以计算任意指定变量之间的相关系数)¶
print(Profit1.corrwith(y))

'''
'''
# 异常值检测
outliers = est.get_influence()

# 帽子矩阵
leverage = outliers.hat_matrix_diag

# dffits值
dffits = outliers.dffits[0]

# 学生化残差
resid_stu = outliers.resid_studentized_external
# cook距离
cook = outliers.cooks_distance[0]

# 合并各种异常值检验的统计量值
contatl = pd.concat([pd.Series(leverage, name='leverage'),
                     pd.Series(dffits, name='dffits'),
                     pd.Series(resid_stu, name='resid_stu'),
                     pd.Series(cook, name='cook')
                     ], axis=1)

train.index = range(train.shape[0])
profit_outliers = pd.concat([train, contatl], axis=1)
print(profit_outliers)

outliers_ratio = np.sum(np.where((np.abs(profit_outliers.resid_stu) > 2), 1, 0)) / profit_outliers.shape[0]
print(outliers_ratio)

none_outliers = profit_outliers.loc[np.abs(profit_outliers.resid_stu) <= 2,]
print(none_outliers)

none_outliers = none_outliers.drop(["leverage", "dffits", "resid_stu", "cook"], axis=1)
x2 = none_outliers.drop("叶丝干燥（薄板式）含水率 ", axis=1)
y2 = none_outliers["叶丝干燥（薄板式）含水率 "]

X2 = sm.add_constant(x2.loc[:, :])
est2 = sm.OLS(y2, X2).fit()
est2.summary()
#print(est2.summary())

'''


ax1 = plt.subplot2grid(shape=(2, 1), loc=(0, 0))  # 设置第一张子图位置
# 散点图绘制
# 学生化残差与自变量散点图
# ax1.scatter(none_outliers["蒸汽流量 "], none_outliers.resid_stu )
# 标准化残差和自变量散点图
ax1.scatter(none_outliers["蒸汽流量 "], (est2.resid - est2.resid.mean()) / est2.resid.std())
# 添加水平参考线
ax1.hlines(y=0,
           xmin=none_outliers["蒸汽流量 "].min(),
           xmax=none_outliers["蒸汽流量 "].max(),
           color='red',
           linestyle='--'
           )
ax1.set_xlabel('蒸汽流量')
ax1.set_ylabel('Std_Residual')

ax2 = plt.subplot2grid(shape=(2, 1), loc=(1, 0))
# 学生化残差与自变量散点图
# ax2.scatter(none_outliers["拔风压力PID阀门开度 "], none_outliers.resid_stu )
# 标准化残差和自变量散点图
ax2.scatter(none_outliers["拔风压力PID阀门开度 "], (est2.resid - est2.resid.mean()) / est2.resid.std())
ax2.hlines(y=0,
           xmin=none_outliers["拔风压力PID阀门开度 "].min(),
           xmax=none_outliers["拔风压力PID阀门开度 "].max(),
           color='magenta',
           linestyle='--'
           )
ax2.set_xlabel('拔风压力PID阀门开度')
ax2.set_ylabel('Std_Residual')

# 调整2子图之间距离
plt.subplots_adjust(hspace=0.6, wspace=0.3)
plt.show()


"""
x_test=test.drop("叶丝干燥（薄板式）含水率 ",axis=1)
y_test=test["叶丝干燥（薄板式）含水率 "]
X_test=sm.add_constant(x_test)
y_pred = est.predict(X_test)

plt.scatter(y_test,y_pred)
plt.plot([y_test.min(),y_test.max()],
         [y_test.min(),y_test.max()],
         color = 'red',
         linestyle = '--')
plt.xlabel('实际值')
plt.ylabel('预测值')
plt.show()
"""