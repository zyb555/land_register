from django.urls import path
from . import views


app_name = 'reg_land'

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('land/', views.land, name='land'),
    path('teacher_student/', views.teacher_student, name='teacher_student'),
    path('add_teacher_page/', views.add_teacher_page, name='add_teacher_page'),
    path('add_teacher/', views.add_teacher, name='add_teacher'),
    path('delete_teacher/', views.delete_teacher, name='delete_teacher'),
    path('revise_teacher_page/', views.revise_teacher_page, name='revise_teacher_page'),
    path('revise_teacher/', views.revise_teacher, name='revise_teacher'),


    path('student_show/', views.student_show, name='student_show'),
    path('delete_student/', views.delete_student, name='delete_student'),
    path('add_student_page/', views.add_student_page, name='add_student_page'),
    path('add_student/', views.add_student, name='add_student'),
    path('revise_student_page/', views.revise_student_page, name='revise_student_page'),
    path('revise_student/', views.revise_student, name='revise_student'),


]