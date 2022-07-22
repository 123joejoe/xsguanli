from django.db import models


# Create your models here.

class studentmessage(models.Model):
    objects = models.Manager()
    GENDER_CHOICES = (
        (1, '男'),
        (2, '女'),
    )
    # 学号
    student_id = models.CharField(max_length=10)
    # 姓名
    name = models.CharField(max_length=10)
    # 性别
    gender = models.BooleanField(choices=GENDER_CHOICES)
    # 年龄
    age = models.IntegerField()
    # 专业
    major = models.CharField(max_length=20)
    # 地址
    city = models.CharField(max_length=10)
    def __str__(self):
        return self.student_id

    class Meta:
        db_table = 'studentmessage'

