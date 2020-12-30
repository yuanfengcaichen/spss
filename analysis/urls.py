from django.conf.urls import url
from . import views
#from analysis import views

urlpatterns = [
    #url('uploadfile',views.uploadfile),
    url(r"^test", views.test, name='test'),
    url(r"^uploadfile", views.uploadfile, name='uploadfile'),
    url(r"^linear_result", views.linear_result),
    url(r"^sendselect",views.sendselect),
    url(r"^getsin_pre_value",views.getsin_pre_value),
    url(r"^uploadpre_file",views.uploadpre_file),
    url(r"^getprediction",views.getprediction),
    url(r"^getnormality",views.getnormality),
    url(r"^getppqq",views.getppqq),
    url(r"^getks",views.getks),
    url(r"^getmulticol",views.getmulticol),
    url(r"^getlinearcorrelate",views.getlinearcorrelate),
    url(r"^getoutliertest",views.getoutliertest),
    url(r"^getresidual",views.getresidual),
    url(r"^getbp",views.getbp),
    url(r"^getvariance",views.getvariance),
    #url('',views.index),
    url(r"", views.index.as_view(), name='index'),
    url(r"^index/$", views.index.as_view(), name='index'),
]