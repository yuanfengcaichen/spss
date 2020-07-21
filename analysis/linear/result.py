import statsmodels.regression.linear_model as x
class result():
    def __init__(self, model: x) -> None:
        self.fa = model.fvalue
    def say(self):
        print(self.fa)
    def turndict(self):
        return self.__dict__