"""
异常值检测模型
"""

from sklearn import model_selection
import statsmodels.api as sm
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
from sklearn import preprocessing
from io import BytesIO
import base64
import copy
def outliertest(Profit,xselected,yselected):
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
    x=x.reset_index(drop=True)
    y=y.reset_index(drop=True)
    #profit_outliers = pd.concat([train, contatl], axis=1)
    profit_outliers = pd.concat([x,y, contatl], axis = 1)
    # print(profit_outliers)

    outliers_ratio = np.sum(np.where((np.abs(profit_outliers.resid_stu) > 2), 1, 0)) / profit_outliers.shape[0]
    # print(outliers_ratio)

    none_outliers = profit_outliers.loc[np.abs(profit_outliers.resid_stu) <= 2,]
    # print(none_outliers)

    #求异常值
    outdata=profit_outliers.loc[np.abs(profit_outliers.resid_stu) > 2,]
    #print(outdata)
    outlist=[]
    ls = copy.deepcopy(xselected)
    ls.append(yselected)
    ls.append('resid_stu')
    for l in outdata.values.tolist():
        outlist.append(dict(zip(ls, l)))

    #none_outliers = none_outliers.drop(["leverage", "dffits", "resid_stu", "cook"], axis=1)
    x2 = none_outliers[xselected]
    y2 = none_outliers[yselected]

    X2 = sm.add_constant(x2.loc[:, :])
    est2 = sm.OLS(y2, X2).fit()

    x_test = test[xselected]
    y_test = test[yselected]
    X_test = sm.add_constant(x_test)
    y_pred = est.predict(X_test)
    #画图
    plt.scatter(y_test, y_pred)
    plt.plot([y_test.min(), y_test.max()],
             [y_test.min(), y_test.max()],
             color='red',
             linestyle='--')
    plt.xlabel('实际值')
    plt.ylabel('预测值')
    sio = BytesIO()
    plt.savefig(sio, format='png', bbox_inches='tight', pad_inches=0.0)
    data = base64.encodebytes(sio.getvalue()).decode()
    src = 'data:image/png;base64,' + str(data)
    # 记得关闭，不然画出来的图是重复的
    plt.axis('off')
    plt.close()

    return {'model':est2.summary().as_html(),'outdata':outlist,'src':src}