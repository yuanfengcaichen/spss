"""
获取模型
"""
from sklearn import model_selection
import statsmodels.api as sm
import matplotlib

from analysis.linear.gradually import FeatureSelection

matplotlib.use('Agg')
from matplotlib import pyplot as plt
import base64
from io import BytesIO
import pandas as pd
import numpy as np

def setmodel(Files,fileindex,xselected,yselected,analytype,criterion,direction):
    if(analytype=="linear"):
        train, test = model_selection.train_test_split(Files.get(fileindex).get("Profit"), test_size=0.2, random_state=22)

        x = train[xselected]
        X = sm.add_constant(x)

        y = train[yselected]
        est = sm.OLS(y, X)
        est = est.fit()

        data = Files.get(fileindex)
        data["train"] = train
        data["test"] = test
        data["est"] = est
    elif(analytype=="gradually"):
        data_train, data_test = model_selection.train_test_split(Files.get(fileindex).get("Profit"), test_size=0.2, random_state=22)
        s=[]
        for x in xselected:
            s.append(x)
        s.append(yselected)
        F = FeatureSelection().stepwise(df=data_train[s], response=yselected, max_iter=200,
                                    criterion=criterion,direction=direction)
        est = F.stepwise_model
        xselected_change = F.stepwise_feat_selected_
        data = Files.get(fileindex)
        data["train"] = data_train
        data["test"] = data_test
        data["est"] = est
        data["xselected_change"] = xselected_change
        #print(est.summary())