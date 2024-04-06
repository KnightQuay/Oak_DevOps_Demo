from django.db.models import Q
from rest_framework.decorators import api_view

from myapp.apiResponse import APIResponse
from myapp.models import Flight, RemainingTickets, Airport
from myapp.serializers import FlightSerializer, RemainingTicketsSerializer, AirportSerializer

from datetime import datetime, timedelta

def parse_and_format_datetime(datetime_str):
    try:
        # 解析日期时间字符串
        datetime_str = datetime_str.replace(" ", "+")
        # "2023-12-19T16:51:00+08:00"
        parsed_datetime = datetime.fromisoformat(datetime_str)

        # 将日期时间对象格式化为目标格式
        formatted_datetime = parsed_datetime.strftime('%Y-%m-%d %H:%M:%S')

        return parsed_datetime
    except ValueError as e:
        # 处理解析错误
        print(f"解析日期时间出错：{e}")
        return None

@api_view(['GET'])
def get_available_flights_time(request):
    try:
        departure_airport_id = request.GET.get('departure_airport_id')
        arrival_airport_id = request.GET.get('arrival_airport_id')
        departure_time = request.GET.get('departure_time')

        departure_datetime = parse_and_format_datetime(departure_time)
        start_time = departure_datetime - timedelta(hours=1)
        end_time = departure_datetime + timedelta(hours=1)

        # 构建查询条件
        conditions = Q(departure_airport_id=departure_airport_id) & \
                     Q(arrival_airport_id=arrival_airport_id) & \
                     Q(departure_time__range=(start_time, end_time))
        available_flights = Flight.objects.filter(conditions)

        # 构建结果数据
        flight_data = []
        for flight in available_flights:
            # 获取航班信息
            flight_serializer = FlightSerializer(flight)
            flight_info = flight_serializer.data

            # 获取舱位价格信息
            remaining_tickets = RemainingTickets.objects.filter(flight=flight)
            prices_serializer = RemainingTicketsSerializer(remaining_tickets, many=True)
            prices_info = prices_serializer.data

            # 将舱位价格信息添加到航班信息中
            flight_info['prices'] = prices_info

            # 添加到结果列表中
            flight_data.append(flight_info)

        # 返回成功的响应
        return APIResponse(myStatus=True, msg='可选航班获取成功', data=flight_data)
    except Exception as e:
        # 返回错误的响应
        return APIResponse(myStatus=False, msg='获取可选航班失败', data={'error': str(e)})

@api_view(['GET'])
def get_available_flights_date(request):
    try:
        departure_airport_id = request.GET.get('departure_airport_id')
        arrival_airport_id = request.GET.get('arrival_airport_id')
        departure_date = request.GET.get('departure_date')

        # 构建查询条件
        conditions = Q(departure_airport_id=departure_airport_id) & \
                     Q(arrival_airport_id=arrival_airport_id) & \
                     Q(departure_time__date=departure_date)
        available_flights = Flight.objects.filter(conditions)

        # 构建结果数据
        flight_data = []
        for flight in available_flights:
            # 获取航班信息
            flight_serializer = FlightSerializer(flight)
            flight_info = flight_serializer.data

            # 获取舱位价格信息
            remaining_tickets = RemainingTickets.objects.filter(flight=flight)
            prices_serializer = RemainingTicketsSerializer(remaining_tickets, many=True)
            prices_info = prices_serializer.data

            # 将舱位价格信息添加到航班信息中
            flight_info['prices'] = prices_info

            # 添加到结果列表中
            flight_data.append(flight_info)

            # 返回成功的响应
        return APIResponse(myStatus=True, msg='可选航班获取成功', data=flight_data)
    except Exception as e:
        # 返回错误的响应
        return APIResponse(myStatus=False, msg='获取可选航班失败', data={'error': str(e)})

@api_view(['GET'])
def get_airports_with_departures(request):
    try:
        airports_with_departures = Airport.objects.filter(departures__status='scheduled').distinct()

        serializer = AirportSerializer(airports_with_departures, many=True)
        serialized_data = serializer.data

        return APIResponse(myStatus=True, msg='获取可选起飞机场成功', data=serialized_data)
    except Exception as e:
        return APIResponse(myStatus=False, msg='获取可选起飞机场失败', data={'error': str(e)})


@api_view(['GET'])
def get_airports_with_arrivals(request):
    try:
        airports_with_arrivals = Airport.objects.filter(arrivals__status='scheduled').distinct()

        serializer = AirportSerializer(airports_with_arrivals, many=True)
        serialized_data = serializer.data

        return APIResponse(myStatus=True, msg='获取可选到达机场成功', data=serialized_data)
    except Exception as e:
        return APIResponse(myStatus=False, msg='获取可选到达机场失败', data={'error': str(e)})