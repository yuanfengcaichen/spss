"""
返回模型预测图片
"""

from sklearn import model_selection
import statsmodels.api as sm
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import base64
from io import BytesIO
import pandas as pd
import numpy as np

def prediction(Profit,xselected,yselected):
    train, test = model_selection.train_test_split(Profit, test_size=0.2, random_state=22)

    x = train[xselected]
    #x=train.drop(yselected, axis=1)
    X = sm.add_constant(x)

    y = train[yselected]
    est = sm.OLS(y, X)
    est = est.fit()
    x_test = test[xselected]
    y_test = test[yselected]
    X_test = sm.add_constant(x_test)
    y_pred = est.predict(X_test)

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
    return src