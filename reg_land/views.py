import base64
from django.shortcuts import render
from . models import *
from django.views.decorators.http import require_POST
from django.http import HttpResponse
# Create your views here.


#  返回注册登陆页面
def index(request):
    return render(request, 'index.html')


# 注册验证
@require_POST
def register(request):
    empty = ' '
    # 获取 前台数据
    name = request.POST.get('firstname')
    pwd = request.POST.get('password')
    em = request.POST.get('email')
    if name is None or name.isspace() or pwd is None or pwd.isspace() or em is None or em.isspace():
        return render(request, 'index.html', {'register_point_out': '账号, 密码, 邮箱,不能为空'})
    elif len(name) < 6 or len(name) > 16 or len(pwd) < 6 or len(pwd) > 16 or len(em) < 6 or len(em) > 20:
        return render(request, 'index.html', {'register_point_out': '账号, 密码,长度为 6 到 16 位! 邮箱, 长度为 6 到 20 位'})
    elif empty in name or empty in pwd or empty in em: # 验证空格
        return render(request, 'index.html', {'register_point_out': '账号, 密码,邮箱, 不能包含空格'})
    else:
        base_pwd = (str(base64.b64encode(pwd.encode('utf-8')), 'utf-8'))
        Regland.objects.create(uName=name, passWord=base_pwd, emAil=em)
        return render(request, 'index.html', {'register_point_out': '注册成功'})


# 登陆验证
@require_POST
def land(request):
    empty = ' '
    # 获取前台数据
    uname = request.POST.get('land_name')
    upwd = request.POST.get('land_pwd')
    base_pwd = (str(base64.b64encode(upwd.encode('utf-8')), 'utf-8'))
    if uname is None or uname.isspace() or upwd is None or upwd.isspace():
        return render(request, 'index.html', {'land_point_out': '账号, 密码, 不能为空'})
    elif len(uname) < 6 or len(uname) > 16 or len(upwd) < 6 or len(upwd) > 16:
        return render(request, 'index.html', {'land_point_out': '账号, 密码,长度为 6 到 16 位!'})
    elif empty in uname or empty in upwd: # 验证空格是否存在
        return render(request, 'index.html', {'land_point_out': '账号, 密码, 不能包含空格'})

    if Regland.objects.filter(uName = uname, passWord = base_pwd): #  跟 数据库中的数据 匹配
        return render(request, 'land.html', {'land_point_out': '尊敬的  ['+uname+']  欢迎你!'})
    else:
        return render(request, 'index.html', {'land_point_out': '登陆失败!账号密码错误'})


# 查看老师  展示老师的学生
def teacher_student(request):
    tea = Teacher.objects.values().all()    # 查询所有老师
    lis = []
    tea_num = request.GET.get('tea_num')    # 获取 前端 的值
    if tea_num:     # 当有值
        try:
            s = Teacher.objects.get(id=tea_num).student_set.values('name')  # 根据 值 查询学生
            if s:   # 当有学生
                for i in s:
                    lis.append(i.get('name'))
                return render(request, 'teacher_student.html', {'tea':tea, 's':lis})
            return render(request, 'teacher_student.html', {'tea': tea, 'ss': '该老师没有学生'})   # 没有学生
        except Exception:
            return render(request, 'teacher_student.html', {'tea': tea, 'ss': '没有该老师'})
    return render(request, 'teacher_student.html', {'tea': tea})    # 当tea_num 没值


# 添加老师页面
def add_teacher_page(request):
    return render(request, 'add_teacher_page.html')


# 添加老师到数据库
def add_teacher(request):
    uname = request.GET.get('uname')
    ubirth = request.GET.get('ubirth')
    ugender = request.GET.get('ugender')
    uis_married = request.GET.get('uis_married')
    Teacher.objects.create(name = uname, birth = ubirth, gender = ugender, is_married = uis_married)
    return render(request, 'add_teacher_page.html', {'point_out':'添加成功'})


# 删除老师
def delete_teacher(request):
    tea = Teacher.objects.values().all()
    dellete = request.GET.get('dellete')
    t = Teacher.objects.filter(id=dellete)
    if t.count() == 0:
        return render(request, 'teacher_student.html', {'dele': '没有该老师', 'tea': tea})
    Teacher.objects.filter(id=dellete).delete()
    return render(request, 'teacher_student.html', { 'tea': tea, 'dele':'删除成功'})



# 修改老师页面
def revise_teacher_page(request):
    return render(request, 'revise_teacher_page.html')


# 数据库修改
def revise_teacher(request):
    id = request.GET.get('id')
    uname = request.GET.get('uname')
    ubirth = request.GET.get('ubirth')
    ugender = request.GET.get('ugender')
    uis_married = request.GET.get('uis_married')
    try:
        Teacher.objects.filter(id = id).update(name = uname, birth = ubirth, gender = ugender, is_married = uis_married)
        return render(request, 'revise_teacher_page.html', {'rev':'修改成功'})
    except Exception:
        return render(request, 'revise_teacher_page.html', {'rev': '修改失败!请认真输入 '})


# 学生 展示    学生的老师展示
def student_show(request):
    stu = Student.objects.all()
    liss = []
    students = request.GET.get('students')
    if students:
        try:
            t = Student.objects.get(id = students).teachers.values('name')
            if t:
                for i in t:
                    liss.append(i.get('name'))
                return render(request, 'student_show.html', {'stu': stu, 't': liss})
            return render(request, 'student_show.html', {'stu': stu, 'tt': '该学生没有老师'})
        except Exception:
            return render(request, 'student_show.html', {'stu': stu, 'tt': '没有该学生'})
    return render(request, 'student_show.html', {'stu':stu})


# 删除学生
def delete_student(request):
    stu = Student.objects.values().all()
    del_stu = request.GET.get('del_stu')
    s = Student.objects.filter(id=del_stu)
    if s.count() == 0:
        return render(request, 'student_show.html', {'del_stu': '没有该学生', 'stu': stu})
    Student.objects.filter(id=del_stu).delete()
    return render(request, 'student_show.html', {'del_stu':'删除成功', 'stu': stu})


# 添加学生页面
def add_student_page(request):
    return render(request, 'add_student_page.html')


# 添加学生到数据库
def add_student(request):
    uname = request.GET.get('uname')
    ubirth = request.GET.get('ubirth')
    ugender = request.GET.get('ugender')
    Student.objects.create(name=uname, birth=ubirth, gender=ugender)
    return render(request, 'add_student_page.html', {'point_out': '添加成功'})


# 修改页面
def revise_student_page(request):
    return render(request, 'revise_student_page.html')



# 修改数据库
def revise_student(request):
    id = request.GET.get('id')
    uname = request.GET.get('uname')
    ubirth = request.GET.get('ubirth')
    ugender = request.GET.get('ugender')
    try:
        Student.objects.filter(id=id).update(name=uname, birth=ubirth, gender=ugender)
        return render(request, 'revise_student_page.html', {'rev': '修改成功'})
    except Exception:
        return render(request, 'revise_student_page.html', {'rev': '修改失败!请认真输入 '})

