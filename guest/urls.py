"""guest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls import url
from django.views import static
from django.contrib import admin
from django.urls import path, include
from sign import views

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^static/(?P<path>.*)$', static.serve,
        {'document_root': settings.STATIC_ROOT}, name='static'),

    # sign应用
    # url(r'^index/$', views.index),
    path('index/', views.index),
    path('login_action/', views.login_action),
    path('event_manage/', views.event_manage),
    path('accounts/login/', views.index),
    path('search_name/', views.search_name),
    path('guest_manage/', views.guest_manage),
    path('search_phone/', views.search_phone),
    path('logout/', views.logout),
    path('sign_index/<int:eid>/', views.sign_index),
    path('sign_index_action/<int:event_id>/', views.sign_index_action),

    # api应用
    path('api/', include('api.urls')),
]
