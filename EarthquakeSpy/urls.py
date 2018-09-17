"""EarthquakeSpy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from rest_framework.documentation import include_docs_urls
from django.conf.urls import handler404


handler404 = 'Common.CommonErrorPage.handler404'

from Website.tasks import getBaseData
from Website.views import EarthquakeCaseViewSet

router = routers.DefaultRouter()
list(map(lambda item: router.register(*item), [
    [r'datas', EarthquakeCaseViewSet],
]))

urlpatterns = [
    path('admin/', admin.site.urls), # 定义管理员页
    path('auth/', include('rest_framework.urls')), # 导入认证所有页
    path('api/', include(router.urls)), # 导入router所有页
    path('',include('Website.urls')), # 导入可视化数据所有页
    path('docs/', include_docs_urls(title='My API title')), # 导入文档接口页
]

# getBaseData()
