from django.shortcuts import render, Http404, redirect, HttpResponse
from mainapp.models import Date_user,Equation, Coefficient, Zuizhi
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.exceptions import ObjectDoesNotExist
from mainapp.form import  LoginForm, userform, Calculateform
from mainapp.calculate import solve_equations
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout

# Create your views here.
#用户注册
def register_view(request):
    context = {}
    if request.method == 'GET':
        form = UserCreationForm
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse(calculate_view))
    context['form'] = form
    return render(request, 'register.html', context)

#用户登录
def login_view(request):
    context = {}
    if request.method == 'GET':
        form = LoginForm
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user =  authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect(reverse(calculate_view))
            else:
                return Http404
    context['form'] = form
    return render(request, 'login.html', context)

#用户注销
def logout_view(request):
    logout(request)
    return redirect('/')  

#成功页
def success_view(request):
    return render(request, 'success_page.html')

#计算提交页
@login_required
def calculate_view(request):
    context = {}
    user = request.user
    existed = Date_user.objects.filter(date_user=user).exists()
    count = Date_user.objects.filter(date_user=user).count()
    if request.method == 'GET':
        form = Calculateform()
    if  request.method == 'POST':
        form = Calculateform(request.POST)
        if form.is_valid():
            row = form.cleaned_data['row']
            line = form.cleaned_data['line']
            if count < 10:
                newda = Date_user(row=row, line=line, date_user=user)
                newda.save()
                return redirect('calculate_page_index/')
            else:
                return render(request, 'defult.html')
        else:
            Http404
    count_left = 10 - count
    context['form'] = Calculateform()
    context['count'] = count_left
    return render(request, 'calculate_page.html', context)
    
#失败页面
def defult(request):
    return render(request, 'defult.html')

#计算详情页面
@login_required
def calculate_page_index(request):
    context = {}
    user = request.user
    belong_user = Date_user.objects.filter(date_user=user).order_by('-id').first()
    equ_id = belong_user.id
    if request.method == 'POST':
        num_hang = belong_user.line
        num_lie = belong_user.row
        for k in range(1,num_lie + 1):
            value_coefficient = request.POST.get(f'value coefficient{k}')#价值系数
            zuizhi = Zuizhi(belong_to_user3=belong_user, value=value_coefficient)
            zuizhi.save()
        for i in range(1, num_hang + 1):
            comparison_operator = request.POST.get(f'comparison_operator{i}')#约束符号
            constraint_value = request.POST.get(f'constraint_value{i}')#约束条件
            # 创建 Equation 对象
            print(comparison_operator)
            equation = Equation(sign=comparison_operator, constraint_value=float(constraint_value), belong_to_user1=belong_user)
            equation.save()
            for j in range(1, num_lie + 1):                
                coef_value = request.POST.get(f'coefficient{i}{j}')#系数
                coefficient = Coefficient(belong_to_equation=equation, value=float(coef_value), belong_to_user2=belong_user)
                coefficient.save()
        return redirect('detail/')
    equ = Equation.objects.filter(belong_to_user1=belong_user)
    coef = Coefficient.objects.filter(belong_to_user2=belong_user,belong_to_equation=equ_id)
    context['date'] = belong_user
    context['equ'] = equ
    context['coef'] = coef
    return render(request, 'calculate_page_index.html', context)

#结果显示页
@login_required
def calculate_detail(request):
    context = {}
    user = request.user
    belong_user = Date_user.objects.filter(date_user=user).order_by('-id').first()
    date_yueshu = Equation.objects.filter(belong_to_user1=belong_user)#equ对象，符号和约束条件
    date_xishu = Coefficient.objects.filter(belong_to_user2=belong_user)#coe对象，系数
    date_zuizhi = Zuizhi.objects.filter(belong_to_user3=belong_user)#价值系数
    date_zuizhi_value = [zuizhi.value for zuizhi in date_zuizhi]
    belong_user_row = belong_user.row
    solve = solve_equations(date_yueshu, date_xishu, date_zuizhi_value, belong_user_row)
    print(solve)
    context['yueshu'] = date_yueshu
    context['xishu'] = date_xishu
    context['zuizhi'] = date_zuizhi 
    context['date'] = belong_user
    context['solve'] = solve
    return render(request, 'calculate_detail.html', context)