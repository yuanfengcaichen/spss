from django.conf.urls import url
from . import views
#from analysis import views

urlpatterns = [
    #url('uploadfile',views.uploadfile),
    url(r"^uploadfile", views.uploadfile, name='uploadfile'),
    url(r"^sendselect",views.sendselect),
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
    url(r"^linear",views.linear.as_view(), name='linear'),
    url(r"^gradually",views.gradually.as_view(), name='gradually'),
    #url('',views.index),
    url(r"", views.index.as_view(), name='index'),
]