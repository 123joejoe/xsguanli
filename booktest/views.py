import io
from pipes import quote

from django.http import HttpResponse
from django.shortcuts import render
from booktest.models import studentmessage
import xlwt
import requests
import re
import bs4 as Beautifulsoup

# Create your views here.
def index(request):
    '''返回首页'''
    student_id = request.POST.get('student_id')

    stu = studentmessage.objects.all()
    print(stu)
    for s in stu:
        if s.gender == True:
            s.gender = '男'
        if s.gender == False:
            s.gender = '女'
    return render(request,'booktest/index.html',{'stu':stu})

def add(request):
    '''添加学生信息页面显示'''
    return render(request, 'booktest/add.html')


def add_check(request):
    '''添加学生信息'''
    student_id = request.POST.get('student_id')
    name = request.POST.get('name')
    gender = request.POST.get('gender')
    age = request.POST.get('age')
    major = request.POST.get('major')
    city = request.POST.get('city')
    print(student_id, name, age, gender, major, city)
    st = studentmessage.objects.all()
    print(st.count)


    # s = models.studentmessage()
    # s.student_id = student_id
    # s.name = name
    # s.gender = gender
    # s.age = age
    # s.major = major
    # s.city = city
    # s.save()
    try:
        for s in st:
            if student_id == s.student_id:
                return render(request, 'booktest/add.html')
        if all([student_id, name, gender, age, major, city]):
            stu = dict(student_id=student_id, name=name, gender=gender, age=age, major=major, city=city)
            s = studentmessage.objects.create(**stu)
            # print(s.student_id, s.city, s.age)
            re = '学生信息添加成功'
        else:
            re = '有选项未填或填入信息有错误'
            return render(request, 'booktest/add.html', {'ok': re})
    except Exception:
        pass
    return render(request, 'booktest/add.html', {'ok': '有选项未填或填入信息有错误'})


def delete(request):
    '''删除学生信系页面显示'''
    return render(request, 'booktest/delete.html')


def delete_check(request):
    '''删除学生信息'''
    student_id = request.POST.get('student_id')
    if len(student_id) == 0:
        return render(request, 'booktest/delete.html', {'re': '学号不能为空，请重新输入'})
    stu = studentmessage.objects.filter(student_id=student_id)
    if stu.count() == 0:
        return render(request, 'booktest/delete.html', {'re': '没有该学生，请重新输入'})
    else:
        s = studentmessage.objects.filter(student_id=student_id).delete()
        return render(request, 'booktest/delete.html', {'re': '删除成功'})


def change(request):
    '''修改学生信息页面'''
    return render(request, 'booktest/change.html')


def change_check(request):
    '''修改学生信息'''
    student_id = request.POST.get('student_id')
    name = request.POST.get('name')
    gender = request.POST.get('gender')
    age = request.POST.get('age')
    major = request.POST.get('major')
    city = request.POST.get('city')
    print(student_id, name, age, gender, major, city)
    try:
        if gender == 2:
            gender = False
        elif all([student_id, name, gender, age, major, city]):
            stu = dict(student_id=student_id, name=name, gender=gender, age=age, major=major, city=city)
            s = studentmessage.objects.update(**stu)
            # print(s.student_id, s.city, s.age)
            re = '学生信息修改成功'
            return render(request, 'booktest/change.html', {'re': re})
        else:
            re = '有选项未填或填入信息有错误'
            return render(request, 'booktest/change.html',{'re':re})
    except Exception:
        pass
    return render(request, 'booktest/change.html')


def find(request):
    '''查询学生信息页面'''
    return render(request,'booktest/find.html',{'re':'有选项未填或填入信息有错误'})

def find_check(request):
    '''查询学生信息'''
    try:
        sd = request.POST.get('student_id')
        student = studentmessage.objects.get(student_id=sd)
        student_id = student.student_id
        name = student.name
        gender = student.gender
        age = student.age
        major = student.major
        city = student.city
        if gender == True:
            gender = '男'
        if gender == False:
            gender = '女'
        data = {
            'student_id':student_id,
            'name':name,
            'gender':gender,
            'age':age,
            'major': major,
            'city':city,
        }
        return render(request,'booktest/find.html',{'data':data})
    except Exception:
        return render(request,'booktest/find.html',{'re':'查无此人'})




def weather_check(request):
    '''天气查询'''
    li = []
    while True:
        citynames = request.POST.get('city_name')
        if citynames == 'q':
            quit()
        else:
            zx = '(..)'
            cityname = re.split(zx, citynames)
            vip = '市'
            if vip not in cityname:
                cityname.remove('')
                name = citynames
            elif vip in cityname:
                cityname.remove('市')
                cityname.remove('')
            for name in cityname:
                url1 = 'http://api.k780.com:88/?app=weather.future&weaid=%s' % name
                url = url1 + '&appkey=10003&sign=b59bc3ef6191eb9f747dd4e83c99f2a4&format=xml'
                headers = {
                    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0'
                }
                reponse = requests.get(url=url, headers=headers).text

                ex = '<days>(.*?)</days><week>(.*?)</week>(.*?)<citynm>(.*?)</citynm>(.*?)<weather>(.*?)</weather>(.*?)<wind>(.*?)</wind><winp>(.*?)</winp>'
                the_lists = re.findall(ex, reponse, re.S)

                for the_list in the_lists:
                    data1, data2, data3, data4, data5, data6, data7, data8, data9 = the_list
                    final = data1, data2, data4, data6, data8, data9
                    li.append(final)
            return render(request,'booktest/index.html',{'final':li})