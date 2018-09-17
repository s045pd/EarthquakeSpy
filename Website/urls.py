from django.urls import path
from Website.views import MakeChart

urlpatterns = [
    path("",MakeChart.as_view()) # 定义可视化数据接口路由
]
