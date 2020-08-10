"""
获取修正后的模型
"""
from sklearn import model_selection
import statsmodels.api as sm
import pandas as pd
import numpy as np
import matplotlib

from analysis.linear.model import setmodel

matplotlib.use('Agg')
import copy


def setcurmodel(Files,fileindex,xselected,yselected):
    data = Files.get(fileindex)
    train = data.get("train")
    test = data.get("test")
    est = data.get("est")
    xselected_change = data.get("xselected_change")
    if (xselected_change == None):  # 没有xselected_change证明是线性回归
        usedx = xselected
    else:
        usedx = xselected_change
    if(est!=None):
        # train, test = model_selection.train_test_split(Files.get(fileindex).get("Profit"), test_size=0.2,random_state=22)
        x = train[usedx]
        X = sm.add_constant(x)

        y = train[yselected]
        # est = sm.OLS(y, X)
        # est = est.fit()
        outliers = est.get_influence()

        resid_stu = outliers.resid_studentized_external
        contatl = pd.Series(resid_stu, name='resid_stu')
        x = x.reset_index(drop=True)
        y = y.reset_index(drop=True)
        profit_outliers = pd.concat([x,y, contatl], axis = 1)

        # 求异常值
        outdata = profit_outliers.loc[np.abs(profit_outliers.resid_stu) > 2,]
        round(outdata, 3)
        outlist = []
        ls = copy.deepcopy(usedx)
        ls.append(yselected)
        ls.append('resid_stu')
        for l in outdata.values.tolist():
            outlist.append(dict(zip(ls, l)))

        none_outliers = profit_outliers.loc[np.abs(profit_outliers.resid_stu) <= 2,]
        x2 = none_outliers[usedx]
        y2 = none_outliers[yselected]

        X2 = sm.add_constant(x2.loc[:, :])
        est2 = sm.OLS(y2, X2).fit()



        data=Files.get(fileindex)
        data["est2"]=est2
        data["outlist"]=outlist
        data["none_outliers"]=none_outliers
    else:
        pass
        #setmodel(Files,fileindex,xselected,yselected,analytype,criterion,direction)
        #setcurmodel(Files, fileindex, xselected, yselected,analytype,criterion,direction)