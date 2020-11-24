"""
获取模型
"""
from sklearn import model_selection
import statsmodels.api as sm
import matplotlib
from analysis.linear.gradually import FeatureSelection

from analysis.tools.myredis import getconn
import pickle

matplotlib.use('Agg')
from matplotlib import pyplot as plt
import base64
from io import BytesIO
import pandas as pd
import numpy as np

def setmodel(fileindex,xselected,yselected,analytype,criterion,direction):
    conn = getconn()
    newProfit = pickle.loads(conn.hget(fileindex, 'Profit'))
    if(analytype=="linear"):
        train, test = model_selection.train_test_split(newProfit, test_size=0.2, random_state=22)

        x = train[xselected]
        X = sm.add_constant(x)

        y = train[yselected]
        est = sm.OLS(y, X)
        est = est.fit()

        # print(type(est.params))
        # print(type(est.params.index.tolist()))
        # print(est.params.index.tolist())
        # print(type(est.params.values.tolist()))

        #redis
        filedata = {}
        filedata["train"] = pickle.dumps(train)
        filedata["test"] = pickle.dumps(test)
        filedata["est"] = pickle.dumps(est)
        conn.hset(fileindex, mapping=filedata)
        conn.expire(fileindex, 60 * 60 * 2)
    elif(analytype=="gradually"):
        data_train, data_test = model_selection.train_test_split(newProfit, test_size=0.2, random_state=22)
        s=[]
        for x in xselected:
            s.append(x)
        s.append(yselected)
        F = FeatureSelection().stepwise(df=data_train[s], response=yselected, max_iter=200,
                                    criterion=criterion,direction=direction)
        est = F.stepwise_model
        xselected_change = F.stepwise_feat_selected_
        # data = Files.get(fileindex)
        # data["train"] = data_train
        # data["test"] = data_test
        # data["est"] = est
        # data["xselected_change"] = xselected_change

        #redis
        filedata = {}
        filedata["train"] = pickle.dumps(data_train)
        filedata["test"] = pickle.dumps(data_test)
        filedata["est"] = pickle.dumps(est)
        filedata["xselected_change"] = pickle.dumps(xselected_change)
        conn.hset(fileindex, mapping=filedata)
        conn.expire(fileindex, 60 * 60 * 2)
        #print(est.summary())