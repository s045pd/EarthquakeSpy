from rest_framework import serializers
from Website.models import EarthquakeCase


class EarthquakeCaseSerializers(serializers.ModelSerializer):
    class Meta:
        model = EarthquakeCase # 定义需要序列化的类
        fields = '__all__' # 定义序列化字段为全部
