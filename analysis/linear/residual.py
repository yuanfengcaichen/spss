"""
返回残差独立性相关数据
"""

from sklearn import model_selection
import statsmodels.api as sm
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import preprocessing
def residual(Profit,xselected,yselected):
    train, test = model_selection.train_test_split(Profit, test_size=0.2, random_state=22)

    x = train[xselected]
    X = sm.add_constant(x)

    y = train[yselected]
    est = sm.OLS(y, X)
    est = est.fit()
    outliers = est.get_influence()
    est.summary()

    # 帽子矩阵
    leverage = outliers.hat_matrix_diag

    # dffits值,这个很慢
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
    # print(profit_outliers)

    outliers_ratio = np.sum(np.where((np.abs(profit_outliers.resid_stu) > 2), 1, 0)) / profit_outliers.shape[0]
    # print(outliers_ratio)

    none_outliers = profit_outliers.loc[np.abs(profit_outliers.resid_stu) <= 2,]
    # print(none_outliers)

    none_outliers = none_outliers.drop(["leverage", "dffits", "resid_stu", "cook"], axis=1)
    x2 = none_outliers[xselected]
    y2 = none_outliers[yselected]

    X2 = sm.add_constant(x2.loc[:, :])
    est2 = sm.OLS(y2, X2).fit()
    from statsmodels.stats.stattools import (durbin_watson)
    DW = ["%#8.3f" % durbin_watson(est2.wresid)]
    return DW