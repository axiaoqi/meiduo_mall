from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^register/$', views.RegisterView.as_view(), name='register'),
    url(r'^username/(?P<username>[a-zA-Z0-9_]{5,20})/count/$', views.UsernameCountView.as_view(), name='usernamecount'),
    url(r'^login/$', views.LoginView.as_view(), name='login'),
]