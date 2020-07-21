"""
获取修正后的模型
"""
from sklearn import model_selection
import statsmodels.api as sm
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import copy

def setcurmodel(Profit,xselected,yselected):
    train, test = model_selection.train_test_split(Profit, test_size=0.2, random_state=22)
    x = train[xselected]
    X = sm.add_constant(x)

    y = train[yselected]
    est = sm.OLS(y, X)
    est = est.fit()
    outliers = est.get_influence()

    resid_stu = outliers.resid_studentized_external
    contatl = pd.Series(resid_stu, name='resid_stu')
    train.index = range(train.shape[0])
    x = x.reset_index(drop=True)
    y = y.reset_index(drop=True)
    # profit_outliers = pd.concat([train, contatl], axis=1)
    profit_outliers = pd.concat([x, y, contatl], axis=1)
    # print(profit_outliers)

    outliers_ratio = np.sum(np.where((np.abs(profit_outliers.resid_stu) > 2), 1, 0)) / profit_outliers.shape[0]
    # print(outliers_ratio)

    none_outliers = profit_outliers.loc[np.abs(profit_outliers.resid_stu) <= 2,]
    # print(none_outliers)

    # 求异常值
    outdata = profit_outliers.loc[np.abs(profit_outliers.resid_stu) > 2,]
    # print(outdata)
    outlist = []
    ls = copy.deepcopy(xselected)
    ls.append(yselected)
    ls.append('resid_stu')
    for l in outdata.values.tolist():
        outlist.append(dict(zip(ls, l)))

    # none_outliers = none_outliers.drop(["leverage", "dffits", "resid_stu", "cook"], axis=1)
    x2 = none_outliers[xselected]
    y2 = none_outliers[yselected]

    X2 = sm.add_constant(x2.loc[:, :])
    est2 = sm.OLS(y2, X2).fit()
    return est2