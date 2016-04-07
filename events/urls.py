from django.conf.urls import url
from events import views

urlpatterns = [
    url(r'^create$', views.Create.as_view(), name='create'),
    url(r'^all$', views.All.as_view(), name='all'),
    url(r'^(?P<pk>[\d]+)/edit$', views.Edit.as_view(), name='edit'),
    url(r'^(?P<pk>[\d]+)/delete$', views.Delete.as_view(), name='delete'),
    url(r'^(?P<pk>[\d]+)/attend$', views.Attend.as_view(), name='attend'),
    url(r'^getall$', views.GetAll.as_view(), name='getall'),
    url(r'^attending$', views.Attending.as_view(), name='attending'),

]
