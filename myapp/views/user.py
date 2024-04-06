from django.contrib.auth.hashers import make_password, check_password
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.utils import json
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from myapp import utils
from myapp.apiResponse import APIResponse
from myapp.auth.authtication import MyTokenAuthtication
from myapp.models import User, Ticket
from myapp.serializers import UserRegistrationSerializer, LoginLogSerializer, PassengerSerializer, UserSerializer, \
    TicketSerializer, CustomTokenObtainPairSerializer, TicketFlightSerializer
from myapp.utils import md5value

from rest_framework_simplejwt.tokens import RefreshToken

@api_view(['POST'])
def register(request):
    if request.method == "POST":
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # 使用序列化器获取用户数据
            user_serializer = UserSerializer(user)
            user_data = user_serializer.data

            return APIResponse(myStatus=True, msg="注册成功", data=user_data)
        else:
            print(request.data)
            return APIResponse(myStatus=False, msg="注册失败", data={"error": serializer.errors})
    else:
        return APIResponse(myStatus=False, msg="请求异常")


@api_view(['POST'])
def login(request):
    email = request.data['user_email']
    password = request.data['user_password']
    users = User.objects.filter(user_email=email)
    if len(users) == 0:
        return APIResponse(myStatus=False, msg="用户不存在")
    else:
        if (users[0]).user_password == password:
            (users[0]).user_password = make_password(password)
            refresh = RefreshToken.for_user(users[0])
            access_token = str(refresh.access_token)[:499]
            users[0].token = access_token
            (users[0]).save()

            # LoginLog
            make_login_log(request)
            return APIResponse(myStatus=True, msg="登录成功，已为您的密码加密", data={"user_email":users[0].user_email, "token": access_token})
        elif check_password(password, (users[0]).user_password):
            refresh = RefreshToken.for_user(users[0])
            access_token = str(refresh.access_token)[:499]
            users[0].token = access_token
            (users[0]).save()
            # LoginLog
            make_login_log(request)
            return APIResponse(myStatus=True, msg="登录成功", data={"user_email":users[0].user_email, "token": access_token})
        else:
            return APIResponse(myStatus=False, msg="密码错误", data={"user_email": users[0].user_email})

def make_login_log(request):
    try:
        email = request.data['user_email']
        data = {
            "user_email": email,
            "ip": utils.get_ip(request),
            "ua": utils.get_ua(request)
        }
        serializer = LoginLogSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
        else:
            print(serializer.errors)
    except Exception as e:
        print(e)

@api_view(['POST'])
@authentication_classes([MyTokenAuthtication])
def add_passenger_to_current_user(request):
    token = request.META.get("HTTP_MYTOKEN", "")
    users = User.objects.filter(token=token)
    user = users[0]
    data = request.data

    # 将当前用户与乘客关联
    data['affiliate_user'] = user.user_email

    serializer = PassengerSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return APIResponse(myStatus=True, msg='乘客添加成功', data=serializer.data)
    else:
        return APIResponse(myStatus=False, msg='乘客添加失败', data=serializer.errors)

@api_view(['GET'])
@authentication_classes([MyTokenAuthtication])
def get_user_by_email(request):
    try:
        email = request.GET.get('email')
        user = User.objects.get(user_email=email)
        serializer = UserSerializer(user)
        return APIResponse(myStatus=True, msg='用户信息获取成功', data=serializer.data)
    except User.DoesNotExist:
        return APIResponse(myStatus=False, msg='用户不存在', data=None)
    except Exception as e:
        return APIResponse(myStatus=False, msg='获取用户信息失败', data={'error': str(e)})

@api_view(['GET'])
@authentication_classes([MyTokenAuthtication])
def get_tickets(request):
    email = request.GET.get('email')
    user = User.objects.get(user_email=email)
    print(user)

    # 获取用户的所有机票
    tickets = Ticket.objects.filter(passenger__affiliate_user=user)

    # 序列化机票数据
    serializer = TicketFlightSerializer(tickets, many=True)

    return APIResponse(myStatus=True, msg='用户信息获取成功', data=serializer.data)

@api_view(['GET'])
@authentication_classes([MyTokenAuthtication])
def get_passengers(request):
    try:
        token = request.META.get("HTTP_MYTOKEN", "")
        users = User.objects.filter(token=token)
        user = users[0]

        passengers = user.passengers.all()
        serializer = PassengerSerializer(passengers, many=True)
        return APIResponse(myStatus=True, msg='乘客表获取成功', data=serializer.data)
    except Exception as e:
        return APIResponse(myStatus=False, msg='获取乘客表失败', data={'error': str(e)})