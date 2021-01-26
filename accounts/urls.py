from django.conf.urls import url
from .views import *



app_name = "accounts"

urlpatterns = [

    url(r'^$', HomeView.as_view(), name='home'),        
    url(r'^register/$', RegistrationView.as_view(), name='registration'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^forgotpassword/$', PasswordForgotView.as_view(), name='passwordforgot'),   
    url(r'^resetpassword/<email>/<token>/', PasswordResetView.as_view(), name="passwordreset"),
    url(r'^profile/$', ProfileView.as_view(), name='profile'),

    url(r'^contact/$', ContactView.as_view(), name='contact'),

]
