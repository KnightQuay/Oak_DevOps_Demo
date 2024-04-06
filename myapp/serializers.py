from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer, \
    TokenVerifySerializer
from rest_framework_simplejwt.tokens import RefreshToken

from myapp.models import User, LoginLog, Ticket, Passenger, Flight, Aircraft, Airport, RemainingTickets, \
    AddFlightValidation, AddAircraftValidation


class UserRegistrationSerializer(serializers.ModelSerializer):
    user_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        validated_data['user_password'] = make_password(validated_data['user_password'])
        user = User.objects.create(**validated_data, user_icon_url="https://gimg2.baidu.com/image_search/src=http%3A%2F%2Fc-ssl.duitang.com%2Fuploads%2Fitem%2F201911%2F21%2F20191121195046_fktqa.jpeg&refer=http%3A%2F%2Fc-ssl.duitang.com&app=2002&size=f9999,10000&q=a80&n=0&g=0n&fmt=auto?sec=1704274170&t=c7fb5dc3ffce688757ddfb7a3c422a1c")
        # 生成JWT令牌
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)[:499]

        user.token = access_token
        user.save()
        return user

class LoginLogSerializer(serializers.ModelSerializer):
    log_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False)

    class Meta:
        model = LoginLog
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('user_password', 'token')

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'

class PassengerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Passenger
        fields = '__all__'

class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = '__all__'

class AircraftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aircraft
        fields = '__all__'

class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = '__all__'

class RemainingTicketsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RemainingTickets
        fields = '__all__'

class FlightWithPricesSerializer(serializers.Serializer):
    flight_info = FlightSerializer()
    prices = RemainingTicketsSerializer(many=True)

class AddFlightValidationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddFlightValidation
        fields = '__all__'

class AddAircraftValidationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddAircraftValidation
        fields = '__all__'

class POST_AddFlightValidationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddFlightValidation
        fields = '__all__'

    def create(self, validated_data):
        # 设置默认值
        validated_data['progress'] = 'pending'
        validated_data['status'] = 'scheduled'

        # 调用父类的 create 方法来创建对象
        return super().create(validated_data)

class POST_AddAircraftValidationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddAircraftValidation
        fields = '__all__'

    def create(self, validated_data):
        # 设置默认值
        validated_data['progress'] = 'pending'
        validated_data['status'] = '1'

        # 调用父类的 create 方法来创建对象
        return super().create(validated_data)

class PartFlightSerializer(serializers.ModelSerializer):
    departure_airport = AirportSerializer()
    arrival_airport = AirportSerializer()
    class Meta:
        model = Flight
        fields = '__all__'

class TicketFlightSerializer(serializers.ModelSerializer):
    flight = PartFlightSerializer()
    class Meta:
        model = Ticket
        fields = '__all__'

class TmpPassengerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Passenger
        fields = ['name']  # 假设名字是你Passenger模型中的一个字段

    def to_representation(self, instance):
        return instance.name

class TmpTicketFlightSerializer(serializers.ModelSerializer):
    flight = PartFlightSerializer()
    passenger = TmpPassengerSerializer()
    class Meta:
        model = Ticket
        fields = '__all__'
# simple-jwt Token customization: user_email, user_password
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'user_email'
    password_field = 'user_password'

    def validate(self, attrs):
        # 调用父类的 validate 方法完成基本验证
        data = super().validate(attrs)
        return data

class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    username_field = 'user_email'
    password_field = 'user_password'

    def validate(self, attrs):
        data = super().validate(attrs)
        # 添加其他用户信息，如需要的话
        return data

class CustomTokenVerifySerializer(TokenVerifySerializer):
    username_field = 'user_email'
    password_field = 'user_password'

    def validate(self, attrs):
        data = super().validate(attrs)
        # 添加其他用户信息，如需要的话
        return data
