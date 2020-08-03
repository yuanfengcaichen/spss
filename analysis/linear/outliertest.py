"""
异常值检测模型
"""

from sklearn import model_selection
import statsmodels.api as sm
import pandas as pd
import numpy as np
import matplotlib

from analysis.linear.curmodel import setcurmodel

matplotlib.use('Agg')
from matplotlib import pyplot as plt
from sklearn import preprocessing
from io import BytesIO
import base64
import copy
def outliertest(Files,fileindex,xselected,yselected):
    data = Files.get(fileindex)
    train = data.get("train")
    test = data.get("test")
    est = data.get("est")
    est2 = data.get("est2")
    outlist = data.get("outlist")
    xselected_change = data.get("xselected_change")
    if(est2!=None):
        if (xselected_change == None):  # 没有xselected_change证明是线性回归
            x_test = test[xselected]
            y_test = test[yselected]
            X_test = sm.add_constant(x_test)
            y_pred = est.predict(X_test)
            # 画图
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

            return {'model': est2.summary().as_html(), 'outdata': outlist, 'src': src}
        else:
            x_test = test[xselected_change]
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
    else:
        setcurmodel(Files, fileindex, xselected, yselected)
        data=outliertest(Files, fileindex, xselected, yselected)
        return data