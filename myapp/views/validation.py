from rest_framework.decorators import api_view, authentication_classes

from myapp.apiResponse import APIResponse
from myapp.auth.authtication import MyTokenAuthtication, AirportTokenAuthtication, AirlineTokenAuthtication, \
    AdminTokenAuthtication
from myapp.models import User, Airport, Aircraft, Flight, AddFlightValidation, AddAircraftValidation, Airline
from myapp.serializers import AirportSerializer, AircraftSerializer, FlightSerializer, AddFlightValidationSerializer, \
    AddAircraftValidationSerializer, POST_AddFlightValidationSerializer, POST_AddAircraftValidationSerializer


@api_view(['GET'])
@authentication_classes([MyTokenAuthtication])
def get_validation_list(request):
    try:
        token = request.META.get("HTTP_MYTOKEN", "")
        users = User.objects.filter(token=token)
        if users[0].user_auth == 'admin':
            # admin --- airports
            all_airports = Airport.objects.all()
            serializer = AirportSerializer(all_airports, many=True)
            return APIResponse(myStatus=True, msg="管理员获取机场表成功", data=serializer.data)
        elif users[0].user_auth == 'airline_member':
            # airline_member --- related aircraft
            user_airline = users[0].airline_affiliation
            user_aircrafts = Aircraft.objects.filter(airline=user_airline)
            serializer = AircraftSerializer(user_aircrafts, many=True)
            return APIResponse(myStatus=True, msg="航空公司人员获取飞机表成功", data=serializer.data)
        elif users[0].user_auth == 'airport_member':
            # airport_member --- related flights
            user_airport = users[0].airport_affiliation

            departing_flights = Flight.objects.filter(departure_airport=user_airport)
            arriving_flights = Flight.objects.filter(arrival_airport=user_airport)
            all_flights = departing_flights.union(arriving_flights)
            serializer = FlightSerializer(all_flights, many=True)
            return APIResponse(myStatus=True, msg="机场人员获取航班表成功", data=serializer.data)
        else :
            return APIResponse(myStatus=False, msg="无管理权限", data=None)
    except Exception as e:
        return APIResponse(myStatus=False, msg='获取管理表失败', data={'error': str(e)})

@api_view(['GET'])
@authentication_classes([MyTokenAuthtication])
def get_items(request):
    try:
        token = request.META.get("HTTP_MYTOKEN", "")
        users = User.objects.filter(token=token)
        if users[0].user_auth == 'admin':
            # admin --- airports
            all_airports = Airport.objects.all()
            serializer = AirportSerializer(all_airports, many=True)
            return APIResponse(myStatus=True, msg="管理员获取机场表成功", data=serializer.data)
        elif users[0].user_auth == 'airline_member':
            # airline_member --- related aircraft
            user_airline = users[0].airline_affiliation
            user_aircrafts = Aircraft.objects.filter(airline=user_airline)
            serializer = AircraftSerializer(user_aircrafts, many=True)
            return APIResponse(myStatus=True, msg="航空公司人员获取飞机表成功", data=serializer.data)
        elif users[0].user_auth == 'airport_member':
            # airport_member --- related flights
            user_airport = users[0].airport_affiliation

            departing_flights = Flight.objects.filter(departure_airport=user_airport)
            arriving_flights = Flight.objects.filter(arrival_airport=user_airport)
            all_flights = departing_flights.union(arriving_flights)
            serializer = FlightSerializer(all_flights, many=True)
            return APIResponse(myStatus=True, msg="机场人员获取航班表成功", data=serializer.data)
        else :
            return APIResponse(myStatus=False, msg="无管理权限", data=None)
    except Exception as e:
        return APIResponse(myStatus=False, msg='获取管理表失败', data={'error': str(e)})

@api_view(['GET'])
@authentication_classes([MyTokenAuthtication])
def get_validation_list(request):
    try:
        token = request.META.get("HTTP_MYTOKEN", "")
        users = User.objects.filter(token=token)
        if users[0].user_auth == 'admin':
            # 查询所有 AddFlightValidation 表的数据
            flight_validation_data = AddFlightValidation.objects.filter(progress='pending')
            flight_serializer = AddFlightValidationSerializer(flight_validation_data, many=True)

            # 查询所有 AddAircraftValidation 表的数据
            aircraft_validation_data = AddAircraftValidation.objects.filter(progress='pending')
            aircraft_serializer = AddAircraftValidationSerializer(aircraft_validation_data, many=True)

            response_data = {
                'flight_validation_data': flight_serializer.data,
                'aircraft_validation_data': aircraft_serializer.data
            }
            return APIResponse(myStatus=True, msg="管理员获取待审核表成功", data=response_data)
        elif users[0].user_auth == 'airline_member':
            aircraft_validation_data = AddAircraftValidation.objects.filter(initiator_user=users[0])
            serializer = AddAircraftValidationSerializer(aircraft_validation_data, many=True)

            return APIResponse(myStatus=True, msg="航空公司人员获取飞机历史审核申请成功", data=serializer.data)
        elif users[0].user_auth == 'airport_member':
            flight_validation_data = AddFlightValidation.objects.filter(initiator_user=users[0])
            serializer = AddFlightValidationSerializer(flight_validation_data, many=True)

            return APIResponse(myStatus=True, msg="机场人员获取航班历史审核申请成功", data=serializer.data)
        else :
            return APIResponse(myStatus=False, msg="无管理权限", data=None)
    except Exception as e:
        return APIResponse(myStatus=False, msg='获取管理表失败', data={'error': str(e)})

@api_view(['POST'])
@authentication_classes([AirportTokenAuthtication])
def add_flight(request):
    try:
        token = request.META.get("HTTP_MYTOKEN", "")
        users = User.objects.filter(token=token)
        data = request.data.copy()
        data['initiator_user'] = users[0].user_email

        # 检查 flight_id 是否已经被使用
        flight_id = data.get('flight_id')
        if Flight.objects.filter(flight_id=flight_id).exists():
            return APIResponse(myStatus=False, msg= 'flight_id 已被使用')
        departure_airport = data.get('departure_airport')
        if not Airport.objects.filter(code=departure_airport).exists():
            return APIResponse(myStatus=False, msg= 'departure_airport 不存在')
        arrival_airport = data.get('departure_airport')
        if not Airport.objects.filter(code=arrival_airport).exists():
            return APIResponse(myStatus=False, msg='arrival_airport 不存在')
        operating_aircraft = data.get('operating_aircraft')
        if not Aircraft.objects.filter(aircraft_id=operating_aircraft).exists():
            return APIResponse(myStatus=False, msg='operating_aircraft 不存在')

        serializer = POST_AddFlightValidationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()

            return APIResponse(myStatus=True, msg='航班申请数据添加成功')
        return APIResponse(myStatus=False, msg='航班申请数据添加失败', data={'error': serializer.errors})
    except Exception as e:
        return APIResponse(myStatus=False, msg='添加失败', data={'error': str(e)})

@api_view(['POST'])
@authentication_classes([AirlineTokenAuthtication])
def add_aircraft(request):
    try:
        token = request.META.get("HTTP_MYTOKEN", "")
        users = User.objects.filter(token=token)
        data = request.data.copy()
        data['initiator_user'] = users[0].user_email

        # 检查信息
        airline = data.get('airline')
        if not Airline.objects.filter(company_id=airline).exists():
            return APIResponse(myStatus=False, msg= 'airline 不存在')

        serializer = POST_AddAircraftValidationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()

            return APIResponse(myStatus=True, msg='飞机申请数据添加成功')
        return APIResponse(myStatus=False, msg='飞机申请数据添加失败', data={'error': serializer.errors})
    except Exception as e:
        return APIResponse(myStatus=False, msg='添加失败', data={'error': str(e)})

@api_view(['POST'])
@authentication_classes([AdminTokenAuthtication])
def accept(request):
    try:
        id = request.data.get('validation_id')
        object = request.data.get('object')
        if (object == 'aircraft'):
            validation = AddAircraftValidation.objects.get(id=id)
            validation.progress = 'completed'
            validation.save()
            Aircraft.objects.create(
                airline=validation.airline,  # 提供正确的航空公司实例
                seats_num=validation.seats_num,  # 座位数量
                age=validation.age,  # 飞机使用年限
                aircraft_model=validation.aircraft_model,  # 飞机型号
                aircraft_mileage=validation.aircraft_mileage,  # 飞机里程
                WIFI_availability=validation.WIFI_availability,  # 是否有 WIFI
                status=validation.status
            )
            return APIResponse(myStatus=True, msg='同意申请成功')
        elif (object == 'flight'):
            validation = AddFlightValidation.objects.get(id=id)
            validation.progress = 'completed'
            validation.save()
            print(validation.departure_airport)
            Flight.objects.create(
                flight_code=validation.flight_code,  # 航班代码
                departure_airport=validation.departure_airport,  # 出发机场
                departure_time=validation.departure_time,  # 出发时间
                arrival_airport=validation.arrival_airport,  # 到达机场
                arrival_time=validation.arrival_time,  # 到达时间
                operating_aircraft=validation.operating_aircraft,  # 运营飞机
                status=validation.status
            )
            return APIResponse(myStatus=True, msg='同意申请成功')
        else:
            raise Exception("Unknown object type")
    except Exception as e:
        return APIResponse(myStatus=False, msg='操作失败', data={'error': str(e)})

@api_view(['POST'])
@authentication_classes([AdminTokenAuthtication])
def reject(request):
    try:
        id = request.data.get('validation_id')
        object = request.data.get('object')
        if object == 'aircraft':
            validation = AddAircraftValidation.objects.get(id=id)
            validation.progress = 'rejected'
            validation.save()
            return APIResponse(myStatus=True, msg='拒绝申请成功')
        elif object == 'flight':
            validation = AddFlightValidation.objects.get(id=id)
            validation.progress = 'rejected'
            validation.save()
            return APIResponse(myStatus=True, msg='拒绝申请成功')
        else:
            raise Exception("Unknown object type")
    except Exception as e:
        return APIResponse(myStatus=False, msg='操作失败', data={'error': str(e)})

@api_view(['POST'])
@authentication_classes([MyTokenAuthtication])
def remove(request):
    try:
        id = request.data.get("num")
        removeObject = request.data.get("removeObject")
        if removeObject == 'plane':
            aircraft_to_delete = Aircraft.objects.get(aircraft_id=id)
            aircraft_to_delete.delete()
            return APIResponse(myStatus=True, msg='删除成功')
        elif removeObject == 'airport':
            airport_to_delete = Airport.objects.get(code=id)
            airport_to_delete.delete()
            return APIResponse(myStatus=True, msg='删除成功')
        elif removeObject == 'flight':
            flight_to_delete = Flight.objects.get(flight_id=id)
            flight_to_delete.delete()
            return APIResponse(myStatus=True, msg='删除成功')
        else:
            raise Exception("Unknown object type")
    except Exception as e:
        return APIResponse(myStatus=False, msg='操作失败', data={'error': str(e)})