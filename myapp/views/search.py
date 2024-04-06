from datetime import datetime, timedelta

from rest_framework.decorators import api_view

from myapp.apiResponse import APIResponse
from myapp.models import Aircraft, Airport, Flight, Passenger, Ticket
from myapp.serializers import AircraftSerializer, AirportSerializer, FlightSerializer, PassengerSerializer, \
    TicketSerializer, TicketFlightSerializer, TmpTicketFlightSerializer


@api_view(['POST'])
def get_related_data(request):
    selected_object = request.data.get('queryObject')
    filter_object = request.data.get('filterObject')
    try:
        data = None

        # 根据 selected_object 查询相应的表
        if selected_object == "plane":
            data = Aircraft.objects.all()
            serializer = AircraftSerializer(aircraft_filter(data, filter_object), many=True)
        elif selected_object == "airport":
            data = Airport.objects.all()
            serializer = AirportSerializer(airport_filter(data, filter_object), many=True)
        elif selected_object == "flight":
            data = Flight.objects.all()
            serializer = FlightSerializer(flight_filter(data, filter_object), many=True)
        elif selected_object == "passenger":
            data = Passenger.objects.all()
            serializer = PassengerSerializer(passenger_filter(data, filter_object), many=True)
        elif selected_object == "ticket":
            data = Ticket.objects.all()
            serializer = TmpTicketFlightSerializer(ticket_filter(data, filter_object), many=True)
        else:
            return APIResponse(myStatus=False, msg='无效的 selectedObject', data=None)

        # 返回查询结果
        return APIResponse(myStatus=True, msg=f'成功获取 {selected_object} 相关数据', data=serializer.data)

    except Exception as e:
        return APIResponse(myStatus=False, msg=f'获取 {selected_object} 相关数据时出错', data={'error': str(e)})

def flight_filter(data, filter_object):
    for filter_condition in filter_object:
        filter_label = filter_condition.get('filterLabel', '')
        filter_val = filter_condition.get('filterVal', '')

        # 添加过滤条件
        if filter_label == '航班编号':
            data = data.filter(flight_code=filter_val)
        elif filter_label == '起飞机场':
            data = data.filter(departure_airport__name__icontains=filter_val)
        elif filter_label == '起飞时间':
            datetime_val = datetime.strptime(filter_val, '%Y-%m-%dT%H:%M')
            start_time = datetime_val - timedelta(hours=1)
            end_time = datetime_val + timedelta(hours=1)
            data = data.filter(departure_time__range=(start_time, end_time))
        elif filter_label == '降落机场':
            data = data.filter(arrival_airport__name__icontains=filter_val)
        elif filter_label == '降落时间':
            datetime_val = datetime.strptime(filter_val, '%Y-%m-%dT%H:%M')
            start_time = datetime_val - timedelta(hours=1)
            end_time = datetime_val + timedelta(hours=1)
            data = data.filter(arrival_time__range=(start_time, end_time))
        elif filter_label == '执飞飞机':
            data = data.filter(operating_aircraft__aircraft_id=filter_val)
        elif filter_label == '状态':
            data = data.filter(status=filter_val)
        else:
            print("unexpected filter_label")
    return data

def aircraft_filter(data, filter_object):
    for filter_condition in filter_object:
        filter_label = filter_condition.get('filterLabel', '')
        filter_val = filter_condition.get('filterVal', '')

        # 添加过滤条件
        if filter_label == '编号':
            data = data.filter(aircraft_id=filter_val)
        elif filter_label == '所属航空公司':
            data = data.filter(airline=filter_val)
        elif filter_label == '座位数':
            data = data.filter(seats_num=filter_val)
        elif filter_label == '机龄':
            data = data.filter(age=filter_val)
        elif filter_label == '机型':
            data = data.filter(aircraft_model__contains=filter_val)
        elif filter_label == '飞机里程':
            data = data.filter(aircraft_mileage=filter_val)
        elif filter_label == '有无wifi':
            data = data.filter(WIFI_availability=filter_val)
        elif filter_label == '飞机状态':
            data = data.filter(status=filter_val)
        else:
            print("unexpected filter_label")
    return data

def airport_filter(data, filter_object):
    for filter_condition in filter_object:
        filter_label = filter_condition.get('filterLabel', '')
        filter_val = filter_condition.get('filterVal', '')

        # 添加过滤条件
        if filter_label == '机场名':
            data = data.filter(name__icontains=filter_val)
        elif filter_label == '机场编号':
            data = data.filter(code=filter_val)
        elif filter_label == '机场地址':
            data = data.filter(address__icontains=filter_val)
        elif filter_label == '机场电话':
            data = data.filter(phone=filter_val)
        elif filter_label == '休息室数量':
            data = data.filter(lounge_count=filter_val)
        elif filter_label == '停车位数量':
            data = data.filter(parking_spaces=filter_val)
        elif filter_label == '航站楼数量':
            data = data.filter(terminal_num=filter_val)
        else:
            print("unexpected filter_label")
    return data

def passenger_filter(data, filter_object):
    for filter_condition in filter_object:
        filter_label = filter_condition.get('filterLabel', '')
        filter_val = filter_condition.get('filterVal', '')

        # 添加过滤条件
        if filter_label == '姓名':
            data = data.filter(name__icontains=filter_val)
        elif filter_label == '证件号':
            data = data.filter(id_number=filter_val)
        elif filter_label == '性别':
            data = data.filter(gender=filter_val)
        elif filter_label == '年龄':
            numList = filter_val.split(',')
            min = numList[0]
            max = numList[1]
            data = data.filter(age__range=(min, max))
        elif filter_label == '手机号':
            data = data.filter(phone_number=filter_val)
        elif filter_label == '邮箱':
            data = data.filter(email=filter_val)
        elif filter_label == '证件类型':
            data = data.filter(id_type=filter_val)
        else:
            print("unexpected filter_label")
    return data

def ticket_filter(data, filter_object):
    for filter_condition in filter_object:
        filter_label = filter_condition.get('filterLabel', '')
        filter_val = filter_condition.get('filterVal', '')

        # 添加过滤条件
        if filter_label == '订单编号':
            data = data.filter(ticket_code=filter_val)
        elif filter_label == '座位号':
            data = data.filter(seat_num=filter_val)
        elif filter_label == '舱位':
            data = data.filter(cabin_class=filter_val)
        elif filter_label == '购票价格':
            numList = filter_val.split(',')
            min = numList[0]
            max = numList[1]
            data = data.filter(ticket_price__range=(min, max))
        elif filter_label == '乘客名':
            data = data.filter(passenger__name__icontains=filter_val)
        elif filter_label == '航班号':
            data = data.filter(flight__flight_code=filter_val)
        else:
            print("unexpected filter_label")
    return data