from django.db import models


class EarthquakeCase(models.Model): # 定义模型
    ID = models.AutoField(primary_key=True) # ID字段，自增，主键
    Level = models.FloatField() # 地震等级字段
    Time = models.DateTimeField(auto_now=False, auto_now_add=False) # 发生时间字段
    Longitude = models.FloatField() # 经度字段
    Latitede = models.FloatField() # 维度字段
    Deep = models.IntegerField() # 深度字段
    Address = models.CharField(max_length=64) #地址字段

    class Meta:
        unique_together = ("Longitude", "Latitede", "Time") # 建立组合唯一索引