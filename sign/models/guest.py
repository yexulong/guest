#!C:\Users\wb.yexulong\AppData\Local\Programs\Python\Python37\python.exe
# -*- coding: utf-8 -*-
from django.db import models
from sign.models.event import Event


class Guest(models.Model):
    """
    嘉宾表
    """
    event = models.ForeignKey(Event, on_delete=models.CASCADE)  # 关联发布会id
    realname = models.CharField(max_length=64)  # 姓名
    phone = models.CharField(max_length=16)  # 手机号
    email = models.EmailField()  # 邮箱
    sign = models.BooleanField()  # 签到状态
    create_time = models.DateTimeField(auto_now=True)  # 创建时间（自动获取当前时间）

    class Meta:
        unique_together = ('phone', 'event')
        # ordering = ['-id']
        verbose_name = '嘉宾'
        verbose_name_plural = '嘉宾'

    def __str__(self):
        return self.realname
