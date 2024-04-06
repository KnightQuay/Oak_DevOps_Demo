import numpy as np
import pandas as pd
from rest_framework.decorators import api_view, authentication_classes

from myapp.apiResponse import APIResponse
from myapp.auth.authtication import MyTokenAuthtication
from myapp.models import Airport, Aircraft, Airline, Passenger, User, Flight, Ticket


@api_view(['POST'])
@authentication_classes([MyTokenAuthtication])
def upload_airport_data(request):
    file = request.FILES['file']
    if not file.name.endswith('.xls') and not file.name.endswith('.xlsx'):
        return APIResponse(myStatus=False, msg='只支持上传Excel文件', data=None)

    try:
        df = pd.read_excel(file)

        # 数据清洗逻辑
        df_cleaned = clean_airport_data(df)

        # 遍历清洗后的 DataFrame 中的每一行，保存到数据库
        for index, row in df_cleaned.iterrows():
            Airport.objects.create(
                code=row['code'],
                name=row['name'],
                address=row['address'],
                phone=row['phone'],
                lounge_count=row['lounge_count'],
                parking_spaces=row['parking_spaces'],
                terminal_num=row['terminal_num']
            )

        return APIResponse(myStatus=True, msg='机场数据导入成功')
    except Exception as e:
        return APIResponse(myStatus=False, msg=str(e), data=None)

def clean_airport_data(df):
    # 删除包含不可缺失项处为缺失值的数据
    non_missing_columns = ['code', 'name', 'address']  # 添加其他必须项
    df_cleaned = df.dropna(subset=non_missing_columns)

    # 将数值字段转换为整数
    numerical_columns = ['lounge_count', 'parking_spaces', 'terminal_num']
    df_cleaned[numerical_columns] = df_cleaned[numerical_columns].astype(pd.Int64Dtype(), errors='ignore')
    df_cleaned.replace([pd.NA, np.nan, 'NA'], None, inplace=True)

    print(df_cleaned)

    return df_cleaned

@api_view(['POST'])
@authentication_classes([MyTokenAuthtication])
def upload_aircraft_data(request):
    file = request.FILES['file']
    if not file.name.endswith('.xls') and not file.name.endswith('.xlsx'):
        return APIResponse(myStatus=False, msg='只支持上传Excel文件', data=None)

    try:
        df = pd.read_excel(file)

        # 数据清理逻辑
        df_cleaned = clean_aircraft_data(df)

        # 遍历清理后的DataFrame行并保存到数据库
        for index, row in df_cleaned.iterrows():
            airline = Airline.objects.get(company_id=row['airline'])
            Aircraft.objects.create(
                airline=airline,
                seats_num=row['seats_num'],
                age=row['age'],
                aircraft_model=row['aircraft_model'],
                aircraft_mileage=row['aircraft_mileage'],
                WIFI_availability=row['WIFI_availability'],
                status=row['status']
            )

        return APIResponse(myStatus=True, msg='飞机数据导入成功')
    except Exception as e:
        return APIResponse(myStatus=False, msg=str(e), data=None)

def clean_aircraft_data(df):
    # 删除在指定列中包含缺失值的行
    non_missing_columns = ['airline', 'seats_num', 'age', 'aircraft_model']
    df_cleaned = df.dropna(subset=non_missing_columns)

    # 将数值列转换为整数
    numerical_columns = ['seats_num', 'age', 'aircraft_mileage']
    df_cleaned[numerical_columns] = df_cleaned[numerical_columns].astype(pd.Int64Dtype(), errors='ignore')
    df_cleaned.replace([pd.NA, np.nan, 'NA'], None, inplace=True)

    return df_cleaned

@api_view(['POST'])
@authentication_classes([MyTokenAuthtication])
def upload_passenger_data(request):
    file = request.FILES['file']
    if not file.name.endswith('.xls') and not file.name.endswith('.xlsx'):
        return APIResponse(myStatus=False, msg='只支持上传Excel文件', data=None)

    try:
        df = pd.read_excel(file)

        # 数据清理逻辑
        df_cleaned = clean_passenger_data(df)

        token = request.META.get("HTTP_MYTOKEN", "")
        user = User.objects.get(token=token)

        # 遍历清理后的DataFrame行并保存到数据库
        for index, row in df_cleaned.iterrows():
            Passenger.objects.create(
                name=row['name'],
                id_number=row['id_number'],
                gender=row['gender'],
                age=row['age'],
                phone_number=row['phone_number'],
                email=row.get('email', None),
                id_type=row.get('id_type', None),
                affiliate_user=user
            )

        return APIResponse(myStatus=True, msg='乘客数据导入成功')
    except Exception as e:
        return APIResponse(myStatus=False, msg=str(e), data=None)

def clean_passenger_data(df):
    # 删除在指定列中包含缺失值的行
    non_missing_columns = ['name', 'id_number', 'gender', 'age', 'phone_number']
    df_cleaned = df.dropna(subset=non_missing_columns)

    return df_cleaned

@api_view(['POST'])
@authentication_classes([MyTokenAuthtication])
def upload_flight_data(request):
    file = request.FILES['file']
    if not file.name.endswith('.xls') and not file.name.endswith('.xlsx'):
        return APIResponse(myStatus=False, msg='只支持上传Excel文件', data=None)

    try:
        df = pd.read_excel(file)

        # 数据清理逻辑
        df_cleaned = clean_flight_data(df)

        # 遍历清理后的DataFrame行并保存到数据库
        for index, row in df_cleaned.iterrows():
            departure_airport = Airport.objects.get(code=row['departure_airport_code'])
            arrival_airport = Airport.objects.get(code=row['arrival_airport_code'])
            operating_aircraft = Aircraft.objects.get(aircraft_id=row['operating_aircraft_id'])

            Flight.objects.create(
                flight_code=row['flight_code'],
                departure_airport=departure_airport,
                departure_time=row['departure_time'],
                arrival_airport=arrival_airport,
                arrival_time=row['arrival_time'],
                operating_aircraft=operating_aircraft,
                status=row['status']
            )

        return APIResponse(myStatus=True, msg='航班数据导入成功')
    except Exception as e:
        return APIResponse(myStatus=False, msg=str(e), data=None)

def clean_flight_data(df):
    # 删除在指定列中包含缺失值的行
    non_missing_columns = ['flight_code', 'departure_airport_code', 'departure_time', 'arrival_airport_code',
                           'arrival_time', 'operating_aircraft_id', 'status']
    df_cleaned = df.dropna(subset=non_missing_columns)

    # 将日期时间列转换为日期时间类型
    df_cleaned['departure_time'] = pd.to_datetime(df_cleaned['departure_time'])
    df_cleaned['arrival_time'] = pd.to_datetime(df_cleaned['arrival_time'])

    print(df_cleaned)

    return df_cleaned

@api_view(['POST'])
def upload_ticket_data(request):
    file = request.FILES['file']
    if not file.name.endswith('.xls') and not file.name.endswith('.xlsx'):
        return APIResponse(myStatus=False, msg='只支持上传Excel文件', data=None)

    try:
        df = pd.read_excel(file)

        # 数据清理逻辑
        df_cleaned = clean_ticket_data(df)

        # 遍历清理后的DataFrame行并保存到数据库
        for index, row in df_cleaned.iterrows():
            # 获取或创建相关的乘客和航班对象
            passenger = Passenger.objects.get(id_number=row['passenger_id_number'])
            flight = Flight.objects.get(flight_code=row['flight_code'])

            Ticket.objects.create(
                seat_num=row['seat_num'],
                cabin_class=row['cabin_class'],
                ticket_price=row['ticket_price'],
                passenger=passenger,
                flight=flight,
                status=row['status']
            )

        return APIResponse(myStatus=True, msg='机票数据导入成功')
    except Exception as e:
        return APIResponse(myStatus=False, msg=str(e), data=None)

def clean_ticket_data(df):
    # 删除在指定列中包含缺失值的行
    non_missing_columns = ['seat_num', 'cabin_class', 'ticket_price', 'passenger_id_number', 'flight_code', 'status']
    df_cleaned = df.dropna(subset=non_missing_columns)

    return df_cleaned