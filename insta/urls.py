"""instagram URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib.auth import views
from django.contrib import admin
from instagram import views as clones_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'', include('instagram.urls')),
    url('login/', views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    url('^register/', clones_views.register, name='register'),
    url(r'^logout/$', views.logout_then_login, name="logout"),
    # url(r'^logout/$', views.logout, {"next_page": '/'}), 
    url(r'^tinymce/', include('tinymce.urls')),
]