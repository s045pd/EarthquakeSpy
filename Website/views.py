from rest_framework import filters, pagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.renderers import AdminRenderer, TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from Website import models, serializers


class DefaultPagination(pagination.PageNumberPagination):
    page_size = 10 # 每页默认数量
    max_page_size = 100 # 每页最大数量


class EarthquakeCaseViewSet(ModelViewSet):
    queryset = models.EarthquakeCase.objects.all() # 定义queryset
    serializer_class = serializers.EarthquakeCaseSerializers # 定义序列化类
    pagination_class = DefaultPagination # 定义默认翻页参数
    filter_backends = (filters.SearchFilter, filters.OrderingFilter,) # 定义查询筛选方法
    permission_classes = (IsAuthenticatedOrReadOnly,) # 定义访问认证控制
    ordering_fields = '__all__' # 定义排序字段，__all__ 为通配
    search_fields = ('Level','Time','Longitude','Latitede','Deep','Adress') # 定义查询字段
    renderer_classes = (AdminRenderer,) # 定义render类


class MakeChart(APIView):
    renderer_classes = [TemplateHTMLRenderer] # 定义模板类
    template_name = 'index.html' # 模板文件

    def get(self, request):
        queryset = models.EarthquakeCase.objects.order_by('-Time')  # 根据时间降序
        return Response({'data': queryset}) # 响应数据集
