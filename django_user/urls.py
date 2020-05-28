from django.conf.urls import url
from django_user.views import (
    UserSignupView, 
    UserSigInView, 
    UserLogoutView,
)

urlpatterns = [
    url(r'^signup/', UserSignupView.as_view(), name='signup'),
    url(r'^login/', UserSigInView.as_view(), name='login'),
    url(r'^logout/', UserLogoutView.as_view(), name='logout'),
]