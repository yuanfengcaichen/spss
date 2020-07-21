from django.conf.urls import url

from analysis import views

urlpatterns = [
    url('uploadfile',views.uploadfile),
    url('sendselect',views.sendselect),
    url('getprediction',views.getprediction),
    url('getnormality',views.getnormality),
    url('getppqq',views.getppqq),
    url('getks',views.getks),
    url('getmulticol',views.getmulticol),
    url('getlinearcorrelate',views.getlinearcorrelate),
    url('getoutliertest',views.getoutliertest),
    url('getresidual',views.getresidual),
    url('getbp',views.getbp),
    url('getvariance',views.getvariance),
    url('',views.index)
]