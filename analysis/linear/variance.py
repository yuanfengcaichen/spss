"""
返回方差齐性检验图片
"""
import base64
from io import BytesIO
from sklearn import model_selection
import statsmodels.api as sm
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
from sklearn import preprocessing
def varbp(Profit, xselected, yselected):
    train, test = model_selection.train_test_split(Profit, test_size=0.2, random_state=22)

    x = train[xselected]
    X = sm.add_constant(x)

    y = train[yselected]
    est = sm.OLS(y, X)
    est = est.fit()
    outliers = est.get_influence()

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

    BP = sm.stats.diagnostic.het_breuschpagan(est2.resid, exog_het=est2.model.exog)
    return BP

def variance(Profit, xselected, yselected,oselected_1,oselected_2):
    train, test = model_selection.train_test_split(Profit, test_size=0.2, random_state=22)

    x = train[xselected]
    X = sm.add_constant(x)

    y = train[yselected]
    est = sm.OLS(y, X)
    est = est.fit()
    outliers = est.get_influence()

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


    #残差方差齐性检验
    ax1 = plt.subplot2grid(shape=(2, 1), loc=(0, 0))  # 设置第一张子图位置
    # 散点图绘制
    # 学生化残差与自变量散点图
    # ax1.scatter(none_outliers["蒸汽流量 "], none_outliers.resid_stu )
    # 标准化残差和自变量散点图
    ax1.scatter(none_outliers[oselected_1], (est2.resid - est2.resid.mean()) / est2.resid.std())
    # 添加水平参考线
    ax1.hlines(y=0,
               xmin=none_outliers[oselected_1].min(),
               xmax=none_outliers[oselected_1].max(),
               color='red',
               linestyle='--'
               )
    ax1.set_xlabel(oselected_1)
    ax1.set_ylabel('Std_Residual')

    ax2 = plt.subplot2grid(shape=(2, 1), loc=(1, 0))
    # 学生化残差与自变量散点图
    # ax2.scatter(none_outliers["拔风压力PID阀门开度 "], none_outliers.resid_stu )
    # 标准化残差和自变量散点图
    ax2.scatter(none_outliers[oselected_2], (est2.resid - est2.resid.mean()) / est2.resid.std())
    ax2.hlines(y=0,
               xmin=none_outliers[oselected_2].min(),
               xmax=none_outliers[oselected_2].max(),
               color='magenta',
               linestyle='--'
               )
    ax2.set_xlabel(oselected_2)
    ax2.set_ylabel('Std_Residual')

    # 调整2子图之间距离
    plt.subplots_adjust(hspace=0.6, wspace=0.3)
    sio = BytesIO()
    plt.savefig(sio, format='png', bbox_inches='tight', pad_inches=0.0)
    data = base64.encodebytes(sio.getvalue()).decode()
    src = 'data:image/png;base64,' + str(data)
    # 记得关闭，不然画出来的图是重复的
    plt.axis('off')
    plt.close()
    return src