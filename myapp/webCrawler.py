import json
import os
import random
import string
from datetime import timedelta

import django
import requests
import pandas as pd
from django.utils import timezone
from lxml import html
from pymysql import IntegrityError

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backEnd.settings')
django.setup()
from myapp.models import Airline, Airport, Flight, Aircraft, RemainingTickets, FlightDepartureInfo

etree = html.etree

def get_xml(url, start_city, last_city, date):
    resp = requests.get(url, params={"startCity":start_city, "lastCity":last_city, "theDate":date, "userID":""})
    resp.encoding = "utf-8"
    return resp.content
def parse_xml(xml_text):
    xml = etree.XML(xml_text)
    airlines = xml.xpath("//AirlinesTime")
    result = []
    for airline in airlines:
        item = {}
        company = airline.xpath("./Company/text()")[0]
        if company == '没有航班':
            return result
        item['company'] = company
        airline_code = airline.xpath("./AirlineCode/text()")[0]
        item['airline_code'] = airline_code
        start_drome = airline.xpath("./StartDrome/text()")[0]
        item['start_drome'] = start_drome
        arrive_drome = airline.xpath("./ArriveDrome/text()")[0]
        item['arrive_drome'] = arrive_drome
        start_time = airline.xpath("./StartTime/text()")[0]
        item['start_time'] = start_time
        arrive_time = airline.xpath("./ArriveTime/text()")[0]
        item['arrive_time'] = arrive_time
        mode = airline.xpath("./Mode/text()")[0]
        item['mode'] = mode
        airline_stop = airline.xpath("./AirlineStop/text()")[0]
        item['airline_stop'] = airline_stop
        week = airline.xpath("./Week/text()")[0]
        item['week'] = week
        result.append(item)
    return result


def generate_random_string():
    # 生成一个大写字母
    letter = random.choice(string.ascii_uppercase)

    # 生成一个1到20之间的数字
    number = random.randint(1, 20)

    # 返回合并的字符串
    return f"{letter}{number}"

def importData(output_excel_file):
    # 读取Excel文件
    df_flights = pd.read_excel(output_excel_file)

    airport_code = 20
    # 将Excel中的航空公司和机场信息添加到数据库
    for _, row in df_flights.iterrows():
        company_name = row['company']
        airline_code = row['airline_code']
        start_drome_name = row['start_drome']
        arrive_drome_name = row['arrive_drome']

        # 添加航空公司到数据库
        airline, created = Airline.objects.get_or_create(
            company_name_chinese=company_name,
            defaults={
                'company_code': airline_code[:2],
                'company_loc' :company_name[:2],
                'aircraft_num' : random.randint(30, 500),
                'website_url' : 'http://www.airchina.com.cn/',
                'prefix' : airline_code[:2]
            }
        )

        # 添加起飞机场到数据库
        start_drome, created = Airport.objects.get_or_create(
            name=start_drome_name,
            defaults={
                'code': airport_code,
                'address' : start_drome_name,
                'phone' : random.randint(1000000,9999999),
                'lounge_count' : random.randint(100,500),
                'parking_spaces' : random.randint(1000, 5000),
                'terminal_num' : random.randint(1,5)
                }
        )
        if created:
            airport_code = airport_code + 1

        # 添加降落机场到数据库
        arrive_drome, created = Airport.objects.get_or_create(
            name=arrive_drome_name,
            defaults={
                'code': airport_code,
                'address': start_drome_name,
                'phone': random.randint(1000000, 9999999),
                'lounge_count': random.randint(100, 500),
                'parking_spaces': random.randint(1000, 5000),
                'terminal_num': random.randint(1, 5)
            }
        )
        if created:
            airport_code = airport_code + 1

    createAircraft()

    # 重新读取Excel文件，包括新添加的航空公司和机场信息
    df_flights = pd.read_excel(output_excel_file)

    # 将航班信息导入数据库
    for _, row in df_flights.iterrows():
        # 获取航空公司、起飞机场和降落机场对象
        company = Airline.objects.get(company_name_chinese=row['company'])
        start_drome = Airport.objects.get(name=row['start_drome'])
        arrive_drome = Airport.objects.get(name=row['arrive_drome'])
        operating_aircrafts = Aircraft.objects.filter(airline=company)
        if not operating_aircrafts.exists():
            operating_aircraft = Aircraft.objects.get(aircraft_id=1)
        else:
            index = random.randint(0, len(operating_aircrafts) - 1)
            operating_aircraft = operating_aircrafts[index]

        # 时间
        departure_time = timezone.make_aware(
            timezone.datetime.strptime('2023-12-22 ' + row['start_time'], '%Y-%m-%d %H:%M'),
            timezone=timezone.get_fixed_timezone(8 * 60)  # UTC+8的时区
        )
        arrival_time = timezone.make_aware(
            timezone.datetime.strptime('2023-12-22 ' + row['arrive_time'], '%Y-%m-%d %H:%M'),
            timezone=timezone.get_fixed_timezone(8 * 60)  # UTC+8的时区
        )

        # 创建航班对象
        flight = Flight(
            flight_code=row['airline_code'],
            departure_airport=start_drome,
            departure_time=departure_time,
            arrival_airport=arrive_drome,
            arrival_time=arrival_time,
            operating_aircraft=operating_aircraft,  # 你可能需要提供正确的飞机信息
            status='scheduled'
        )
        flightDepartureInfo = FlightDepartureInfo(
            flight=flight,
            terminal = 'T1' if random.randint(0, 1) == 0 else 'T2',
            check_in_counter = generate_random_string(),
            boarding_gate = random.randint(1, 300),
            boarding_time = departure_time - timedelta(minutes=30)
        )

        seat_num_economy = random.randint(80, 150)
        economy = RemainingTickets(
            flight = flight,
            ori_price = random.randint(500, 2000),
            total_num = seat_num_economy,
            available_num = seat_num_economy,
            discount_percentage = 0,
            cabin_class = 'economy',
            purchased_seats = '0'
        )
        seat_num_business = random.randint(30,50)
        business = RemainingTickets(
            flight=flight,
            ori_price=random.randint(2500, 4000),
            total_num=seat_num_business,
            available_num=seat_num_business,
            discount_percentage=0,
            cabin_class='business',
            purchased_seats='0'
        )
        seat_num_prior = random.randint(5, 15)
        prior = RemainingTickets(
            flight=flight,
            ori_price=random.randint(5000, 10000),
            total_num=seat_num_prior,
            available_num=seat_num_prior,
            discount_percentage=0,
            cabin_class='prior',
            purchased_seats='0'
        )

        try:
            flight.save()
            flightDepartureInfo.save()
            economy.save()
            business.save()
            prior.save()
            print(f"Flight {row['airline_code']} added successfully.")
        except IntegrityError:
            print(f"Flight {row['airline_code']} already exists.")

def createAircraft():
    for airline in Airline.objects.all():
        Aircraft.objects.create(
            airline=airline,
            seats_num = random.randint(100, 300),
            age = random.randint(1, 15),
            aircraft_model = 'Boeing 737',
            aircraft_mileage = random.randint(100, 10000),
            WIFI_availability = False if random.randint(0, 1) == 0 else True,
            status = '1'
        )
        Aircraft.objects.create(
            airline=airline,
            seats_num=random.randint(100, 300),
            age=random.randint(1, 15),
            aircraft_model='Airbus A320',
            aircraft_mileage=random.randint(100, 10000),
            WIFI_availability=False if random.randint(0, 1) == 0 else True,
            status='1'
        )
        Aircraft.objects.create(
            airline=airline,
            seats_num=random.randint(100, 300),
            age=random.randint(1, 15),
            aircraft_model='Airbus A380',
            aircraft_mileage=random.randint(100, 10000),
            WIFI_availability=False if random.randint(0, 1) == 0 else True,
            status='1'
        )
        Aircraft.objects.create(
            airline=airline,
            seats_num=random.randint(100, 300),
            age=random.randint(1, 15),
            aircraft_model='Boeing 767',
            aircraft_mileage=random.randint(100, 10000),
            WIFI_availability=False if random.randint(0, 1) == 0 else True,
            status='1'
        )
        Aircraft.objects.create(
            airline=airline,
            seats_num=random.randint(100, 300),
            age=random.randint(1, 15),
            aircraft_model='C919',
            aircraft_mileage=random.randint(100, 10000),
            WIFI_availability=False if random.randint(0, 1) == 0 else True,
            status='1'
        )


if __name__ == '__main__':
    url = "http://www.webxml.com.cn/webservices/DomesticAirline.asmx/getDomesticAirlinesTime"
    # #拆包
    # with open("DomesticCity.json", 'r', encoding='utf-8') as f:
    #     load_dict = json.load(f)
    # for city in load_dict:
    #     print(city['cnCityName'])
    #     city_list.append(city['cnCityName'])
    #     print(city_list)
    city_list_test = ['北京', '长春', '常德', '昌都', '长沙', '成都', '重庆', '大理', '大连',
                      '恩施', '佛山', '广州', '桂林', '贵阳', '固原', '海口', '杭州', '合肥',
                      '香港', '高雄', '昆明', '兰州', '拉萨', '南昌', '南充', '南京', '青岛',
                      '三亚', '上海', '沈阳', '深圳', '台中', '台北', '台东', '太原', '天津',
                      '武汉', '芜湖', '无锡', '梧州', '厦门', '西安', '郑州', '银川']
    city_list_test1 = ['阿里', '安康', '安庆', '鞍山', '安顺', '安阳', '百色', '保山', '包头',
     '北海', '北京', '蚌埠', '毕节', '博乐', '长春', '常德', '昌都', '长沙', '长治', '常州', '朝阳', '成都',
     '嘉义', '赤峰', '重庆', '大理', '大连', '丹东', '大庆', '大同', '达县', '达州', '德宏', '德阳', '迪庆',
     '东莞', '东营', '敦煌', '恩施', '佛山', '阜阳', '富蕴', '福州', '赣州', '广汉',
     '光化', '广元', '广州', '桂林', '贵阳', '固原', '海口', '哈密', '邯郸', '杭州',
     '汉中', '合肥', '黑河', '衡阳', '和田', '香港', '淮安', '怀化', '花莲', '黄山', '黄石', '黄岩',
     '惠州', '吉安', '揭阳', '吉林', '济南', '金昌',
     '景洪', '济宁', '晋江', '锦州', '九江', '鸡西', '康定', '高雄', '喀什',
     '金门', '库车', '昆明', '兰州', '拉萨', '连城', '梁平', '荔波', '丽江', '临沧',
     '林西', '临沂', '林芝', '黎平', '柳州', '龙岩', '洛阳', '泸州', '澳门', '马公', '芒市', '梅县', '梅州',
     '绵阳', '漠河', '南昌', '南充', '南京', '南宁', '南通', '南阳', '宁波', '普洱',
     '黔江', '且末', '青岛', '庆阳', '泉州', '衢州', '三亚', '上海',
     '汕头', '沙市', '沈阳', '深圳', '石狮', '思茅', '苏州', '塔城', '台中', '台北', '台东', '太原', '台州',
     '唐山', '腾冲', '天津', '天水', '通化', '通辽', '铜仁', '万州', '潍坊', '威海',
     '文山', '温州', '乌海', '武汉', '芜湖', '无锡', '梧州', '厦门', '西安', '襄樊',
     '襄阳', '西昌', '邢台', '兴义', '西宁', '徐州', '延安', '盐城', '扬州', '延吉',
     '烟台', '宜宾', '宜昌', '宜春', '伊春', '伊犁', '银川', '义乌', '永州', '榆林', '运城', '玉树',
     '张掖', '湛江', '昭通', '郑州', '芷江', '中山', '中卫', '舟山', '珠海', '株洲', '遵义']
    city_list = ['阿尔山', '阿克苏', '阿勒泰', '阿里', '安康', '安庆', '鞍山', '安顺', '安阳', '百色', '保山', '包头', '巴彦淖尔',
     '北海', '北京', '蚌埠', '毕节', '博乐', '长白山', '长春', '常德', '昌都', '长沙', '长治', '常州', '朝阳', '成都',
     '嘉义', '赤峰', '重庆', '大理', '大理市', '大连', '丹东', '大庆', '大同', '达县', '达州', '德宏', '德阳', '迪庆',
     '东莞', '东营', '敦煌', '鄂尔多斯', '二连浩特', '恩施', '佛山', '阜阳', '富蕴', '福州', '赣州', '格尔木', '广汉',
     '光化', '广元', '广州', '桂林', '贵阳', '固原', '哈尔滨', '海口', '海拉尔', '哈密市', '哈密', '邯郸', '杭州',
     '汉中', '合肥', '黑河', '衡阳', '和田', '和田市', '香港', '淮安', '怀化', '花莲', '黄山', '黄石', '黄岩',
     '呼和浩特', '惠州', '加格达奇', '佳木斯', '吉安', '嘉峪关', '揭阳', '吉林', '济南', '金昌', '景德镇', '井冈山',
     '景洪', '济宁', '晋江', '锦州', '九华山', '九江', '九寨沟', '鸡西', '喀纳斯', '康定', '高雄', '喀什市', '喀什',
     '克拉玛依', '金门', '库车', '库尔勒', '昆明', '兰州', '拉萨', '连城', '梁平', '连云港', '荔波', '丽江', '临沧',
     '林西', '临沂', '林芝', '黎平', '柳州', '龙岩', '洛阳', '泸州', '澳门', '马公', '芒市', '满洲里', '梅县', '梅州',
     '绵阳', '漠河', '牡丹江', '那拉提', '南昌', '南充', '南京', '南宁', '南通', '南阳', '宁波', '攀枝花', '普洱',
     '普陀山', '黔江', '且末', '青岛', '庆阳', '秦皇岛', '齐齐哈尔', '泉州', '衢州', '日喀则', '三亚', '上海', '山海关',
     '汕头', '沙市', '沈阳', '深圳', '石家庄', '石狮', '思茅', '苏州', '塔城', '台中', '台北', '台东', '太原', '台州',
     '唐山', '腾冲', '天津', '天水', '通化', '通辽', '铜仁市', '铜仁', '吐鲁番', '万州', '潍坊', '威海', '文山县',
     '文山', '温州', '乌海', '武汉', '芜湖', '乌兰浩特', '乌鲁木齐', '无锡', '武夷山', '梧州', '厦门', '西安', '襄樊',
     '香格里拉', '襄阳', '西昌', '锡林浩特', '邢台', '兴义', '西宁', '西双版纳', '徐州', '延安', '盐城', '扬州', '延吉',
     '烟台', '宜宾', '宜昌', '宜春', '伊春', '伊犁', '银川', '伊宁市', '义乌', '永州', '榆林', '运城', '玉树', '玉树县',
     '张家界', '张家口', '张掖', '湛江', '昭通', '郑州', '芷江', '中山', '中卫', '舟山', '珠海', '株洲', '遵义']
    # 创建一个 Pandas 的 DataFrame 用于存储所有航班信息
    all_results = pd.DataFrame()
    for start_city in city_list_test:
        for last_city in city_list_test:
            if start_city == last_city:
                continue
            # start_city = "北京"
            # last_city = "长春"
            date = ""
            xml_text = get_xml(url, start_city, last_city, date)

            # 解析 XML 数据
            output = parse_xml(xml_text)
            if len(output) == 0:
                continue
            print(parse_xml(xml_text))

            # json
            output_file = './webData/' + start_city + '-' + last_city + "Airline.json"
            with open(output_file, "w", encoding="utf8") as f:
                json.dump(output, f, indent=4, ensure_ascii=False)

            # 将航班信息添加到 DataFrame 中
            df = pd.DataFrame(output)
            # 删除指定列
            df.drop(['mode', 'airline_stop', 'week'], axis=1, inplace=True)
            all_results = pd.concat([all_results, df], ignore_index=True)

    # 将所有结果保存到 Excel 文件中
    output_excel_file = './webData/flights.xlsx'
    all_results.to_excel(output_excel_file, index=False, engine='openpyxl')
    importData(output_excel_file)
