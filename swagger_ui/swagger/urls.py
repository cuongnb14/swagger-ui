from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^(?P<doc_id>\d+)$', views.DocumentView.as_view(), name='doc'),
]
