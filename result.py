import statsmodels.regression.linear_model as x
class result():#返回的模型数据
    def __init__(self, model: x) -> None:
        self.title = model.model.__class__.__name__ + ' ' + "Regression Results"

        #top-left
        self.Dep_Variable = None
        self.Model = None
        self.Method = ['Least Squares']
        self.Date = None
        self.Time = None
        self.No_Observations= None
        self.DfResiduals= None
        self.DfModel = None

        #top-right
        self.R_squared = ["%#8.3f" % model.rsquared]
        self.Adj_R_squared = ["%#8.3f" % model.rsquared_adj]
        self.F_statistic = ["%#8.4g" % model.fvalue]
        self.Prob_F_statistic = ["%#6.3g" % model.f_pvalue]
        self.Log_Likelihood = None
        self.AIC = ["%#8.4g" % model.aic]
        self.BIC = ["%#8.4g" % model.bic]

        from statsmodels.stats.stattools import (jarque_bera, omni_normtest, durbin_watson)
        jb, jbpv, skew, kurtosis = jarque_bera(model.wresid)
        omni, omnipv = omni_normtest(model.wresid)
        eigvals = model.eigenvals
        condno = model.condition_number
        #diagn_left
        self.Omnibus = ["%#6.3f" % omni]
        self.Prob_Omnibus = ["%#6.3f" % omnipv]
        self.Skew = ["%#6.3f" % skew]
        self.Kurtosis = ["%#6.3f" % kurtosis]

        #diagn_right
        self.Durbin_Watson = ["%#8.3f" % durbin_watson(model.wresid)]
        self.JarqueBera_JB = ["%#8.3f" % jb]
        self.Prob_JB = ["%#8.3g" % jbpv]
        self.Cond_No = ["%#8.3g" % condno]

    def say(self):
        print(self.fa)
    def turndict(self):
        return self.__dict__

