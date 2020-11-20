# 载入包
import pandas as pd
#from sklearn.preprocessing import LabelEncoder
from sklearn import model_selection
import statsmodels.api as sm
import numpy as np
from sklearn.preprocessing import StandardScaler



#逐步回归
class FeatureSelection():
    def stepwise(self, df, response, intercept=True, normalize=False, criterion='bic',
                 f_pvalue_enter=.05, p_value_enter=.05, direction='both', show_step=True,
                 criterion_enter=None, criterion_remove=None, max_iter=200, **kw):

        """
        逐步回归。

        参数
        ----
        df : dataframe
            分析用数据框，response为第一列。
        response : str
            回归分析相应变量。
        intercept : bool, 默认是True
            模型是否有截距项。
        criterion : str, 默认是'bic'
            逐步回归优化规则。
        f_pvalue_enter : float, 默认是.05
            当选择criterion=’ssr‘时，模型加入或移除变量的f_pvalue阈值。
        p_value_enter : float, 默认是.05
            当选择derection=’both‘时，移除变量的pvalue阈值。
        direction : str, 默认是'backward'
            逐步回归方向。
        show_step : bool, 默认是True
            是否显示逐步回归过程。
        criterion_enter : float, 默认是None
            当选择derection=’both‘或'forward'时，模型加入变量的相应的criterion阈值。
        criterion_remove : float, 默认是None
            当选择derection='backward'时，模型移除变量的相应的criterion阈值。
        max_iter : int, 默认是200
            模型最大迭代次数。
        """

        criterion_list = ['bic', 'aic', 'ssr', 'rsquared', 'rsquared_adj']
        if criterion not in criterion_list:
            raise IOError('请输入正确的criterion, 必须是以下内容之一：', '\n', criterion_list)
        #print(criterion)

        direction_list = ['backward', 'forward', 'both']
        if direction not in direction_list:
            raise IOError('请输入正确的direction, 必须是以下内容之一：', '\n', direction_list)
        #print(direction)
        # 默认p_enter参数
        p_enter = {'bic': 0.0, 'aic': 0.0, 'ssr': 0.05, 'rsquared': 0.05, 'rsquared_adj': -0.05}
        if criterion_enter:  # 如果函数中对p_remove相应key传参，则变更该参数
            p_enter[criterion] = criterion_enter

        # 默认p_remove参数
        p_remove = {'bic': 0.01, 'aic': 0.01, 'ssr': 0.1, 'rsquared': 0.05, 'rsquared_adj': -0.05}
        if criterion_remove:  # 如果函数中对p_remove相应key传参，则变更该参数
            p_remove[criterion] = criterion_remove

        if normalize:  # 如果需要标准化数据
            intercept = False  # 截距强制设置为0
            df_std = StandardScaler().fit_transform(df)
            df = pd.DataFrame(df_std, columns=df.columns, index=df.index)

        """ forward """
        if direction == 'forward':
            remaining = list(df.columns)  # 自变量集合
            remaining.remove(response)
            selected = []  # 初始化选入模型的变量列表
            # 初始化当前评分,最优新评分
            if intercept:  # 是否有截距
                X = sm.add_constant(df[remaining[0]])
            else:
                X = df[remaining[0]]

            result = sm.OLS(df[response], X).fit()  # 最小二乘法回归模型拟合
            current_score = eval('result.' + criterion)
            best_new_score = eval('result.' + criterion)

            if show_step:
                pass
                #print('\nstepwise starting:\n')
            iter_times = 0
            # 当变量未剔除完，并且当前评分更新时进行循环
            while remaining and (current_score == best_new_score) and (iter_times < max_iter):
                scores_with_candidates = []  # 初始化变量以及其评分列表
                for candidate in remaining:  # 在未剔除的变量中每次选择一个变量进入模型，如此循环
                    if intercept:  # 是否有截距
                        X = sm.add_constant(df[selected + [candidate]])
                    else:
                        X = df[selected + [candidate]]

                    result = sm.OLS(df[response], X).fit()  # 最小二乘法回归模型拟合
                    fvalue = result.fvalue
                    f_pvalue = result.f_pvalue
                    score = eval('result.' + criterion)
                    scores_with_candidates.append((score, candidate, fvalue, f_pvalue))  # 记录此次循环的变量、评分列表

                if criterion == 'ssr':  # 这几个指标取最小值进行优化
                    scores_with_candidates.sort(reverse=True)  # 对评分列表进行降序排序
                    best_new_score, best_candidate, best_new_fvalue, best_new_f_pvalue = scores_with_candidates.pop()  # 提取最小分数及其对应变量
                    if ((current_score - best_new_score) > p_enter[criterion]) and (
                            best_new_f_pvalue < f_pvalue_enter):  # 如果当前评分大于最新评分
                        remaining.remove(best_candidate)  # 从剩余未评分变量中剔除最新最优分对应的变量
                        selected.append(best_candidate)  # 将最新最优分对应的变量放入已选变量列表
                        current_score = best_new_score  # 更新当前评分
                        if show_step:  # 是否显示逐步回归过程
                            pass
                            #print('Adding %s, SSR = %.3f, Fstat = %.3f, FpValue = %.3e' %
                            #      (best_candidate, best_new_score, best_new_fvalue, best_new_f_pvalue))
                    elif (current_score - best_new_score) >= 0 and (
                            best_new_f_pvalue < f_pvalue_enter) and iter_times == 0:  # 当评分差大于等于0，且为第一次迭代
                        remaining.remove(best_candidate)
                        selected.append(best_candidate)
                        current_score = best_new_score
                        if show_step:  # 是否显示逐步回归过程
                            pass
                            #print('Adding %s, %s = %.3f' % (best_candidate, criterion, best_new_score))
                    elif (best_new_f_pvalue < f_pvalue_enter) and iter_times == 0:  # 当评分差小于p_enter，且为第一次迭代
                        selected.append(remaining[0])
                        remaining.remove(remaining[0])
                        if show_step:  # 是否显示逐步回归过程
                            pass
                            #print('Adding %s, %s = %.3f' % (remaining[0], criterion, best_new_score))
                elif criterion in ['bic', 'aic']:  # 这几个指标取最小值进行优化
                    scores_with_candidates.sort(reverse=True)  # 对评分列表进行降序排序
                    best_new_score, best_candidate, best_new_fvalue, best_new_f_pvalue = scores_with_candidates.pop()  # 提取最小分数及其对应变量
                    if (current_score - best_new_score) > p_enter[criterion]:  # 如果当前评分大于最新评分
                        remaining.remove(best_candidate)  # 从剩余未评分变量中剔除最新最优分对应的变量
                        selected.append(best_candidate)  # 将最新最优分对应的变量放入已选变量列表
                        current_score = best_new_score  # 更新当前评分
                        # print(iter_times)
                        if show_step:  # 是否显示逐步回归过程
                            pass
                            #print('Adding %s, %s = %.3f' % (best_candidate, criterion, best_new_score))
                    elif (current_score - best_new_score) >= 0 and iter_times == 0:  # 当评分差大于等于0，且为第一次迭代
                        remaining.remove(best_candidate)
                        selected.append(best_candidate)
                        current_score = best_new_score
                        if show_step:  # 是否显示逐步回归过程
                            pass
                            #print('Adding %s, %s = %.3f' % (best_candidate, criterion, best_new_score))
                    elif iter_times == 0:  # 当评分差小于p_enter，且为第一次迭代
                        selected.append(remaining[0])
                        remaining.remove(remaining[0])
                        if show_step:  # 是否显示逐步回归过程
                            pass
                            #print('Adding %s, %s = %.3f' % (remaining[0], criterion, best_new_score))
                else:
                    scores_with_candidates.sort()
                    best_new_score, best_candidate, best_new_fvalue, best_new_f_pvalue = scores_with_candidates.pop()
                    if (best_new_score - current_score) > p_enter[criterion]:
                        remaining.remove(best_candidate)
                        selected.append(best_candidate)
                        current_score = best_new_score
                        #print(iter_times, flush=True)
                        if show_step:  # 是否显示逐步回归过程
                            pass
                            #print('Adding %s, %s = %.3f' % (best_candidate, criterion, best_new_score))
                    elif (best_new_score - current_score) >= 0 and iter_times == 0:  # 当评分差大于等于0，且为第一次迭代
                        remaining.remove(best_candidate)
                        selected.append(best_candidate)
                        current_score = best_new_score
                        if show_step:  # 是否显示逐步回归过程
                            pass
                            #print('Adding %s, %s = %.3f' % (best_candidate, criterion, best_new_score))
                    elif iter_times == 0:  # 当评分差小于p_enter，且为第一次迭代
                        selected.append(remaining[0])
                        remaining.remove(remaining[0])
                        if show_step:  # 是否显示逐步回归过程
                            pass
                            #print('Adding %s, %s = %.3f' % (remaining[0], criterion, best_new_score))
                iter_times += 1

            if intercept:  # 是否有截距
                X = sm.add_constant(df[selected])
            else:
                X = df[selected]

            self.stepwise_model = sm.OLS(df[response], X).fit()  # 最优模型拟合

            if show_step:  # 是否显示逐步回归过程
                pass
                # print('\n', self.stepwise_model.summary())

        """ backward """
        if direction == 'backward':
            remaining, selected = set(df.columns), set(df.columns)  # 自变量集合
            remaining.remove(response)
            selected.remove(response)  # 初始化选入模型的变量列表
            # 初始化当前评分,最优新评分
            if intercept:  # 是否有截距
                X = sm.add_constant(df[list(selected)])
            else:
                X = df[list(selected)]

            result = sm.OLS(df[response], X).fit()  # 最小二乘法回归模型拟合
            current_score = eval('result.' + criterion)
            worst_new_score = eval('result.' + criterion)
            if show_step:
                pass
                #print('\nstepwise starting:\n')
            iter_times = 0
            # 当变量未剔除完，并且当前评分更新时进行循环
            while remaining and (current_score == worst_new_score) and (iter_times < max_iter):
                scores_with_eliminations = []  # 初始化变量以及其评分列表
                for elimination in remaining:  # 在未剔除的变量中每次选择一个变量进入模型，如此循环
                    if intercept:  # 是否有截距
                        X = sm.add_constant(df[list(selected - set(elimination))])
                    else:
                        X = df[list(selected - set(elimination))]
                    result = sm.OLS(df[response], X).fit()  # 最小二乘法回归模型拟合
                    fvalue = result.fvalue
                    f_pvalue = result.f_pvalue
                    score = eval('result.' + criterion)
                    scores_with_eliminations.append((score, elimination, fvalue, f_pvalue))  # 记录此次循环的变量、评分列表

                if criterion == 'ssr':  # 这几个指标取最小值进行优化
                    scores_with_eliminations.sort(reverse=False)  # 对评分列表进行降序排序
                    worst_new_score, worst_elimination, worst_new_fvalue, worst_new_f_pvalue = scores_with_eliminations.pop()  # 提取最小分数及其对应变量
                    if ((worst_new_score - current_score) < p_remove[criterion]) and (
                            worst_new_f_pvalue < f_pvalue_enter):  # 如果当前评分大于最新评分
                        remaining.remove(worst_elimination)  # 从剩余未评分变量中剔除最新最优分对应的变量
                        selected.remove(worst_elimination)  # 从已选变量列表中剔除最新最优分对应的变量
                        current_score = worst_new_score  # 更新当前评分
                        if show_step:  # 是否显示逐步回归过程
                            pass
                            #print('Removing %s, SSR = %.3f, Fstat = %.3f, FpValue = %.3e' %
                            #      (worst_elimination, worst_new_score, worst_new_fvalue, worst_new_f_pvalue))
                elif criterion in ['bic', 'aic']:  # 这几个指标取最小值进行优化
                    scores_with_eliminations.sort(reverse=False)  # 对评分列表进行降序排序
                    worst_new_score, worst_elimination, worst_new_fvalue, worst_new_f_pvalue = scores_with_eliminations.pop()  # 提取最小分数及其对应变量
                    if (worst_new_score - current_score) < p_remove[criterion]:  # 如果评分变动不显著
                        remaining.remove(worst_elimination)  # 从剩余未评分变量中剔除最新最优分对应的变量
                        selected.remove(worst_elimination)  # 从已选变量列表中剔除最新最优分对应的变量
                        current_score = worst_new_score  # 更新当前评分
                        if show_step:  # 是否显示逐步回归过程
                            pass
                            #print('Removing %s, %s = %.3f' % (worst_elimination, criterion, worst_new_score))
                else:
                    scores_with_eliminations.sort(reverse=True)
                    worst_new_score, worst_elimination, worst_new_fvalue, worst_new_f_pvalue = scores_with_eliminations.pop()
                    if (current_score - worst_new_score) < p_remove[criterion]:
                        remaining.remove(worst_elimination)
                        selected.remove(worst_elimination)
                        current_score = worst_new_score
                        if show_step:  # 是否显示逐步回归过程
                            pass
                            #print('Removing %s, %s = %.3f' % (worst_elimination, criterion, worst_new_score))
                iter_times += 1

            if intercept:  # 是否有截距
                X = sm.add_constant(df[list(selected)])
            else:
                X = df[list(selected)]
            self.stepwise_model = sm.OLS(df[response], X).fit()  # 最优模型拟合

            if show_step:  # 是否显示逐步回归过程
                pass
                # print('\n', self.stepwise_model.summary())

        """ both """
        if direction == 'both':
            remaining = list(df.columns)  # 自变量集合
            remaining.remove(response)
            #print(remaining)
            selected = []  # 初始化选入模型的变量列表
            #print(selected)
            # 初始化当前评分,最优新评分
            if intercept:  # 是否有截距
                X = sm.add_constant(df[remaining[0]])
                #print(X)
            else:
                X = df[remaining[0]]
                #print(X)
            #print(df[response])
            result = sm.OLS(df[response], X).fit()  # 最小二乘法回归模型拟合
            #print(result.summary())
            current_score = eval('result.' + criterion)
            best_new_score = eval('result.' + criterion)
            #print(current_score, best_new_score)
            if show_step:
                pass
                #print('\nstepwise starting:\n')
            # 当变量未剔除完，并且当前评分更新时进行循环
            iter_times = 0
            while remaining and (current_score == best_new_score) and (iter_times < max_iter):
                scores_with_candidates = []  # 初始化变量以及其评分列表
                for candidate in remaining:  # 在未剔除的变量中每次选择一个变量进入模型，如此循环
                    #print(candidate)
                    if intercept:  # 是否有截距
                        X = sm.add_constant(df[selected + [candidate]])
                    else:
                        X = selected + [candidate]
                    result = sm.OLS(df[response], X).fit()  # 最小二乘法回归模型拟合
                    #print(result.summary())
                    fvalue = result.fvalue
                    f_pvalue = result.f_pvalue
                    score = eval('result.' + criterion)
                    scores_with_candidates.append((score, candidate, fvalue, f_pvalue))  # 记录此次循环的变量、评分列表

                if criterion == 'ssr':  # 这几个指标取最小值进行优化
                    scores_with_candidates.sort(reverse=True)  # 对评分列表进行降序排序
                    best_new_score, best_candidate, best_new_fvalue, best_new_f_pvalue = scores_with_candidates.pop()  # 提取最小分数及其对应变量
                    if ((current_score - best_new_score) > p_enter[criterion]) and (
                            best_new_f_pvalue < f_pvalue_enter):  # 如果当前评分大于最新评分
                        remaining.remove(best_candidate)  # 从剩余未评分变量中剔除最新最优分对应的变量
                        selected.append(best_candidate)  # 将最新最优分对应的变量放入已选变量列表
                        current_score = best_new_score  # 更新当前评分
                        if show_step:  # 是否显示逐步回归过程
                            pass
                            #print('Adding %s, SSR = %.3f, Fstat = %.3f, FpValue = %.3e' %
                            #      (best_candidate, best_new_score, best_new_fvalue, best_new_f_pvalue))
                    elif (current_score - best_new_score) >= 0 and (
                            best_new_f_pvalue < f_pvalue_enter) and iter_times == 0:  # 当评分差大于等于0，且为第一次迭代
                        remaining.remove(best_candidate)
                        selected.append(best_candidate)
                        current_score = best_new_score
                        if show_step:  # 是否显示逐步回归过程
                            pass
                            #print('Adding %s, %s = %.3f' % (best_candidate, criterion, best_new_score))
                    elif (best_new_f_pvalue < f_pvalue_enter) and iter_times == 0:  # 当评分差小于p_enter，且为第一次迭代
                        selected.append(remaining[0])
                        remaining.remove(remaining[0])
                        if show_step:  # 是否显示逐步回归过程
                            pass
                            #print('Adding %s, %s = %.3f' % (remaining[0], criterion, best_new_score))
                elif criterion in ['bic', 'aic']:  # 这几个指标取最小值进行优化
                    scores_with_candidates.sort(reverse=True)  # 对评分列表进行降序排序
                    best_new_score, best_candidate, best_new_fvalue, best_new_f_pvalue = scores_with_candidates.pop()  # 提取最小分数及其对应变量
                    if (current_score - best_new_score) > p_enter[criterion]:  # 如果当前评分大于最新评分
                        remaining.remove(best_candidate)  # 从剩余未评分变量中剔除最新最优分对应的变量
                        selected.append(best_candidate)  # 将最新最优分对应的变量放入已选变量列表
                        current_score = best_new_score  # 更新当前评分
                        if show_step:  # 是否显示逐步回归过程
                            pass
                            #print('Adding %s, %s = %.3f' % (best_candidate, criterion, best_new_score))
                    elif (current_score - best_new_score) >= 0 and iter_times == 0:  # 当评分差大于等于0，且为第一次迭代
                        remaining.remove(best_candidate)
                        selected.append(best_candidate)
                        current_score = best_new_score
                        if show_step:  # 是否显示逐步回归过程
                            pass
                            #print('Adding %s, %s = %.3f' % (best_candidate, criterion, best_new_score))
                    elif iter_times == 0:  # 当评分差小于p_enter，且为第一次迭代
                        selected.append(remaining[0])
                        remaining.remove(remaining[0])
                        if show_step:  # 是否显示逐步回归过程
                            pass
                            #print('Adding %s, %s = %.3f' % (remaining[0], criterion, best_new_score))
                else:
                    scores_with_candidates.sort()
                    best_new_score, best_candidate, best_new_fvalue, best_new_f_pvalue = scores_with_candidates.pop()
                    if (best_new_score - current_score) > p_enter[criterion]:  # 当评分差大于p_enter
                        remaining.remove(best_candidate)
                        selected.append(best_candidate)
                        current_score = best_new_score
                        if show_step:  # 是否显示逐步回归过程
                            pass
                            #print('Adding %s, %s = %.3f' % (best_candidate, criterion, best_new_score))
                    elif (best_new_score - current_score) >= 0 and iter_times == 0:  # 当评分差大于等于0，且为第一次迭代
                        remaining.remove(best_candidate)
                        selected.append(best_candidate)
                        current_score = best_new_score
                        if show_step:  # 是否显示逐步回归过程
                            pass
                            #print('Adding %s, %s = %.3f' % (best_candidate, criterion, best_new_score))
                    elif iter_times == 0:  # 当评分差小于p_enter，且为第一次迭代
                        selected.append(remaining[0])
                        remaining.remove(remaining[0])
                        if show_step:  # 是否显示逐步回归过程
                            pass
                            #print('Adding %s, %s = %.3f' % (remaining[0], criterion, best_new_score))
                if intercept:  # 是否有截距
                    X = sm.add_constant(df[selected])
                else:
                    X = df[selected]
                pass
                #print(X)
                result = sm.OLS(df[response], X).fit()  # 最优模型拟合
                if iter_times >= 1:  # 当第二次循环时判断变量的pvalue是否达标
                    if result.pvalues.max() > p_value_enter:
                        var_removed = result.pvalues[result.pvalues == result.pvalues.max()].index[0]
                        p_value_removed = result.pvalues[result.pvalues == result.pvalues.max()].values[0]
                        x=result.pvalues[result.pvalues == result.pvalues.max()].index[0]
                        if(x in selected):
                            selected.remove(result.pvalues[result.pvalues == result.pvalues.max()].index[0])
                        if show_step:  # 是否显示逐步回归过程
                            pass
                            #print('Removing %s, Pvalue = %.3f' % (var_removed, p_value_removed))
                iter_times += 1

            if intercept:  # 是否有截距
                X = sm.add_constant(df[selected])
            else:
                X = df[selected]
            self.stepwise_model = sm.OLS(df[response], X).fit()  # 最优模型拟合
            if show_step:  # 是否显示逐步回归过程
                pass
                #print('\n', self.stepwise_model.summary())
                # 最终模型选择的变量

        #return self.stepwise_model
        if intercept:
            self.stepwise_feat_selected_ = list(self.stepwise_model.params.index[1:])
        else:
            self.stepwise_feat_selected_ = list(self.stepwise_model.params.index)
        return self


def main():
    # 读取数据
    data_path = r'D:\亚龙展旗\项目\spss(多元回归分析)\本地版回归分析\中华烘丝0706七批数据对应.xlsx'
    data = pd.read_excel(data_path)

    data = data.drop(["批次号", "日期", "时间", "批内序号", "管路"], axis=1)

    # 分训练集测试集
    #data_train, data_test = model_selection.train_test_split(data, test_size=0.2, random_state=22)
    #data = data_train
    #est = FeatureSelection().stepwise(df=data, response='叶丝干燥（薄板式）温度（出口处） ', max_iter=200,
    #                            criterion='bic')
    #print(est.summary())

if __name__ == "__main__":
    main()