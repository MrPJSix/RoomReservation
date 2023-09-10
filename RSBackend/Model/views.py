from django.http import JsonResponse
from Model.models import *
from django.contrib.auth.hashers import check_password

# Create your views here.
from django.shortcuts import render, HttpResponse

from django.middleware.csrf import get_token

# Create your views here.

def csrf(request):
    csrf_token = get_token(request)
    return JsonResponse({'csrfToken': csrf_token})

# 用户登陆
def login(request):
    # user_id = 1234
    # password = '123'
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        password = request.POST.get('password')
    elif request.method == 'GET':
        user_id = request.GET.get('user_id')
        password = request.GET.get('password')
    data = {
        "user_id": "",
        "userName": "",
        "credits": '',
        "defaultTimes": '',
        "email": ""
    }
    response_data = {
        "success": True,
        "code": 200,
        "message": '',
        "data": data
    }
    try:
        user = User.objects.get(user_id = user_id)
    # 用户不存在
    except User.DoesNotExist:
        response_data['success'] = False
        response_data['message'] = 'User not found'
        return JsonResponse(response_data)
    # 密码正确
    # if check_password(password, user.password):
    if check_password(password, user.password):
        data['user_id'] = user.user_id
        data['userName'] = user.user_name
        data['credits'] = user.credits
        data['defaultTimes'] = user.default_times
        data['email'] = user.email
        response_data['message'] = 'Password is correct'
        return JsonResponse(response_data)
    # 密码不正确
    response_data['success'] = False
    response_data['message'] = 'Incorrect password'
    return JsonResponse(response_data)

# 用户注册
def register(request):
    # user_id = 123
    # user_name = 'Gaga Wang'
    # password = '123'
    # is_admin = True

    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        user_name = request.POST.get('user_name')
        password = request.POST.get('password')
        # is_admin = request.POST.get('is_admin')
        email = request.POST.get('email')
    elif request.method == 'GET':
        user_id = request.GET.get('user_id')
        user_name = request.GET.get('user_name')
        password = request.GET.get('password')
        # is_admin = request.GET.get('is_admin')
        # if not is_admin:
        email = request.GET.get('email')

    response_data = {
        "success": True,
        "code": 200,
        "message": 'User created successfully',
        # "data": data
    }

    try:
        user = User.objects.get(user_id=user_id)
        response_data['success'] = False
        response_data['message'] = 'User is existing'
        return JsonResponse(response_data)
    except:
        pass
    
    # email = '123'
    try:
        new_user = User.objects.create_user(user_id=user_id, user_name=user_name, password=password, email=email)
    except ValueError as e:
            response_data['success'] = False
            response_data['message'] = str(e)
            return JsonResponse(response_data)
    return JsonResponse(response_data)

# 用户注销
def delete_user(request):
    # user_id = 1231
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
    elif request.method == 'GET':
        user_id = request.GET.get('user_id')

    response_data = {
        "success": True,
        "code": 200,
        "message": 'User wrote off successfully',
    }

    try:
        user = User.objects.get(user_id=user_id)
    except User.DoesNotExist:
        response_data['success'] = False
        response_data['message'] = 'User not found'
        return JsonResponse(response_data)
    
    user.delete()
    return JsonResponse(response_data)


# 查看用户所有信息
def user_info(request):
    # user_id = 123

    if request.method == 'POST':
        user_id = request.POST.get('user_id')
    elif request.method == 'GET':
        user_id = request.GET.get('user_id')

    data = {
        'user_id': '',
        'user_name': '',
        'email': '',
        'credits': '',
        'default_times': '',
        'is_staff': False
    }
    response_data = {
        "success": True,
        "code": 200,
        "message": '',
        "data": data
    }
    try:
        user = User.objects.get(user_id=user_id)
    except User.DoesNotExist:
        response_data['success'] = False
        response_data['message'] = 'User not found'
        return JsonResponse(response_data)
    
    data['user_id'] = user.user_id
    data['user_name'] = user.user_name
    data['email'] = user.email
    data['credits'] = user.credits
    data['default_times'] = user.default_times
    data['is_staff'] = user.is_staff
    return JsonResponse(response_data)

# 更新用户信息
def user_info_update(request):
    user_id = None
    user_name = None
    email = None

    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        user_name = request.POST.get('user_name')
        email = request.POST.get('email')
    elif request.method == 'GET':
        user_id = request.GET.get('user_id')
        user_name = request.GET.get('user_name')
        email = request.GET.get('email')

    data = {
        'user_id': '',
        'user_name': '',
        'email': '',
    }
    response_data = {
        "success": True,
        "code": 200,
        "message": '',
        "data": data
    }

    try:
        user = User.objects.get(user_id=user_id)
    except User.DoesNotExist:
        response_data['success'] = False
        response_data['message'] = 'User not found'
        return JsonResponse(response_data)
    
    user.user_name = user_name if user_name is not None else user.user_name
    user.email = email if email is not None else user.email
    user.save()

    data['user_id'] = user.user_id
    data['user_name'] = user.user_name
    data['email'] = user.email

    return JsonResponse(response_data)

# # 必须带上request参数
# def test(request):
#     return HttpResponse("Hello, world!")
#     user.user_name = user_name if user_name is not None else user.user_name
#     user.email = email if email is not None else user.email
#     user.save()
#
#     data['user_id'] = user.user_id
#     data['user_name'] = user.user_name
#     data['email'] = user.email
#
#     return JsonResponse(response_data)

# 查询信誉分
def info_credits(request):
    # user_id = 111

    if request.method == 'POST':
        user_id = request.POST.get('user_id')
    elif request.method == 'GET':
        user_id = request.GET.get('user_id')

    data = {
        'user_id': '',
        'credits': '',
    }
    response_data = {
        "success": True,
        "code": 200,
        "message": '',
        "data": data
    }

    try:
        user = User.objects.get(user_id=user_id)
    except User.DoesNotExist:
        response_data['success'] = False
        response_data['message'] = 'User not found'
        return JsonResponse(response_data)
    if user.is_superuser:
        response_data['success'] = False
        response_data['message'] = 'User not found'
        return JsonResponse(response_data)

    data['user_id'] = user.user_id
    data['credits'] = user.credits
    return JsonResponse(response_data)
