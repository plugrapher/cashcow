"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views., name='')
Class-based views
    1. Add an import:  from other_app.views import 
    2. Add a URL to urlpatterns:  path('', .as_view(), name='')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from user import views as user_view
from django.contrib.auth import views as auth
from django.contrib.auth.views import LoginView
from django.contrib.auth import views as auth_views
from rest_framework.authtoken import views
from django.conf import settings
from django.conf.urls.static import static

from .router import router

urlpatterns = [

    path('admin/', admin.site.urls),

    ######### api path ##########################
   # path('ckeditor/', include('ckeditor_uploader.urls')),

    path('api/', include(router.urls)),
    path('api-token-auth/', views.obtain_auth_token, name='api-tokn-auth'),
    path('passreset/', auth_views.PasswordResetView.as_view(template_name="passreset.html"), name="passreset"),
    path('passreset_done/', auth_views.PasswordResetDoneView.as_view(template_name="email_sent.html"),name="passreset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="reset.html"), name="passreset_confirm"),
    path('reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="reset_complete.html"), name="passreset_complete"),

    #path('ckeditor/', include('ckeditor_uploader.urls')),

    #####user related path##########################
    path('', include('user.urls')),
    path('login/', user_view.Login, name='login'),
    path('logout/', auth.LogoutView.as_view(template_name='users/login.html'), name='logout'),
    path('registration/', user_view.registration, name='register'),

]
