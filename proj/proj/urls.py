"""proj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from app import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^planning-request/write-feedback/(?P<request_id>[0-9]+)', views.write_planning_request_feedback, name='planning_request_write_feedback'),
    url(r'^planning-request/edit/(?P<request_id>[0-9]+)', views.edit_planning_request, name='planning_request_edit'),
    url(r'^planning-request/approve', views.approve, name='approve'),
    url(r'^planning-request/', views.planning_request, name='planning_request'),
    url(r'^task/create/(?P<request_id>[0-9]+)', views.create_task, name='create_task'),
    url(r'^recruitment-request/create/(?P<request_id>[0-9]+)', views.create_recruitment_request, name='create_recruitment_request'),
    url(r'^financial-request/create/(?P<request_id>[0-9]+)', views.create_financial_request, name='create_financial_request'),
    url(r'^login/', views.login, name='login'),
    url(r'^logout/', views.logout, name='logout'),
    url(r'^$', views.index, name='index'),
]
