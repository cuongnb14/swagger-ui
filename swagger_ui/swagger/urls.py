from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^token$', views.SamplView.as_view(), name='sample'),
]
