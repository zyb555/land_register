from django.db import models

# Create your models here.


class Regland(models.Model):
    uName = models.CharField(primary_key=True, max_length=16, db_column='name')
    passWord = models.CharField(max_length=255, db_column='password')
    emAil = models.CharField(max_length=20, db_column='email')

    class Meta:
        db_table  = 'reg_land'



class Teacher(models.Model):
    name = models.CharField(max_length=255,default='')
    birth = models.DateField()
    gender_choices = [
        (0, '女'),
        (1, '男'),
    ]
    gender = models.IntegerField(choices=gender_choices)
    is_married_choices = [
        (0, '未婚'),
        (1, '已婚'),
    ]
    is_married = models.IntegerField(choices=is_married_choices)

    class Meta:
        db_table = 'tea_stu_teacher'



class Student(models.Model):
    name = models.CharField(max_length=255,default='')
    birth = models.DateField()
    gender_choices = [
         (0, '女'),
         (1, '男'),
     ]
    gender =models.IntegerField(choices=gender_choices)
    teachers = models.ManyToManyField(Teacher)
    class Meta:
        db_table = 'tea_stu_student'
