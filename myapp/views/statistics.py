from io import BytesIO

import matplotlib
import pandas as pd
from django.http import HttpResponse
from matplotlib import pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from rest_framework.decorators import api_view, authentication_classes

from myapp.auth.authtication import MyTokenAuthtication
from myapp.models import Airline, Ticket, RemainingTickets, Flight, User
from reportlab.pdfgen import canvas


@api_view(['GET'])
@authentication_classes([MyTokenAuthtication])
def generate_statistics(request):
    matplotlib.use('Agg')
    # 调用统计函数获取每个航空公司的飞机数量区间统计结果
    aircraft_count_ranges = calculate_aircraft_count_ranges()

    scatter_airlines = generate_scatter_chart_airlines(Airline.objects.all())

    # 生成饼状图
    chart_buffer_aircraft = generate_pie_chart(aircraft_count_ranges)

    # 调用统计函数获取票价统计结果
    ticket_price_ranges = calculate_ticket_price_ranges()

    # 生成散点图
    scatter_chart_buffer = generate_scatter_chart(RemainingTickets.objects.all())

    # 生成饼状图
    chart_buffer_ticket = generate_pie_chart(ticket_price_ranges)

    departure_time_ranges = calculate_departure_time_ranges(Flight.objects.all())
    line_chart_departure_time = generate_line_chart(departure_time_ranges)
    chart_buffer_departure_time = generate_pie_chart(departure_time_ranges)

    arrival_time_ranges = calculate_arrival_time_ranges(Flight.objects.all())
    line_chart_arrival_time = generate_line_chart_arrival_time(arrival_time_ranges)
    chart_buffer_arrival_time  = generate_pie_chart(arrival_time_ranges)

    token = request.META.get("HTTP_MYTOKEN", "")
    users = User.objects.filter(token=token)
    flag = False
    if token and len(users) > 0 and users[0].user_auth == "airport_member":
        flag = True
        departures_user = users[0].airport_affiliation.departures.all()
        arrivals_user = users[0].airport_affiliation.arrivals.all()
        departure_time_ranges_user = calculate_departure_time_ranges(departures_user)
        line_chart_departure_time_user = generate_line_chart(departure_time_ranges_user)
        chart_buffer_departure_time_user = generate_pie_chart(departure_time_ranges_user)

        arrival_time_ranges_user = calculate_arrival_time_ranges(arrivals_user)
        line_chart_arrival_time_user = generate_line_chart_arrival_time(arrival_time_ranges_user)
        chart_buffer_arrival_time_user = generate_pie_chart(arrival_time_ranges_user)
    else :
        departure_time_ranges_user = None
        line_chart_departure_time_user = None
        chart_buffer_departure_time_user = None
        arrival_time_ranges_user = None
        line_chart_arrival_time_user = None
        chart_buffer_arrival_time_user = None

    # 创建PDF内容
    pdf_content = BytesIO()
    generate_pdf(pdf_content, scatter_airlines, aircraft_count_ranges, chart_buffer_aircraft,
                 ticket_price_ranges, scatter_chart_buffer, chart_buffer_ticket,
                 departure_time_ranges, line_chart_departure_time, chart_buffer_departure_time,
                 arrival_time_ranges, line_chart_arrival_time, chart_buffer_arrival_time,
                 flag, departure_time_ranges_user, line_chart_departure_time_user, chart_buffer_departure_time_user,
                 arrival_time_ranges_user, line_chart_arrival_time_user, chart_buffer_arrival_time_user)


    # 返回生成的PDF文件
    response = HttpResponse(pdf_content.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="aircraft_count_statistics.pdf"'
    return response


def generate_pdf(pdf_buffer, scatter_airlines, aircraft_count_ranges, chart_buffer_aircraft,
                 ticket_price_ranges, scatter_chart_buffer, chart_buffer_ticket,
                 departure_time_ranges, line_chart_departure_time, chart_buffer_departure_time,
                 arrival_time_ranges, line_chart_arrival_time, chart_buffer_arrival_time,
                 flag, departure_time_ranges_user, line_chart_departure_time_user, chart_buffer_departure_time_user,
                 arrival_time_ranges_user, line_chart_arrival_time_user, chart_buffer_arrival_time_user
                 ):
    # 使用reportlab构建PDF内容
    pdf_canvas = canvas.Canvas(pdf_buffer, pagesize=letter)

    # 第一页

    # 设置PDF标题
    pdf_canvas.setFont("Helvetica", 24)  # 大标题字号
    pdf_canvas.drawString(100, 750, "Flight Management System Statistics")

    # 设置PDF副标题
    pdf_canvas.setFont("Helvetica", 18)  # 小标题字号
    pdf_canvas.drawString(100, 720, "The Statistics of Airlines' Present Fleet of Aircraft")

    # 插入饼状图
    chart_image_reader_aircraft = ImageReader(scatter_airlines)
    pdf_canvas.drawImage(chart_image_reader_aircraft, 100, 370, width=400, height=400, preserveAspectRatio=True)

    # 插入饼状图
    chart_image_reader_aircraft = ImageReader(chart_buffer_aircraft)
    pdf_canvas.drawImage(chart_image_reader_aircraft, 100, 80, width=400, height=400, preserveAspectRatio=True)

    # 保存航空公司飞机数量区间统计信息
    pdf_canvas.setFont("Helvetica", 12)
    pdf_canvas.drawString(130, 120, "Aircraft Count Ranges:")

    y_position_aircraft = 100
    for range_name, count in aircraft_count_ranges.items():
        pdf_canvas.drawString(250, y_position_aircraft, f"{range_name}: {count}")
        y_position_aircraft -= 20

    # 另起一页
    pdf_canvas.showPage()

    # 第二页

    # 设置PDF副标题
    pdf_canvas.setFont("Helvetica", 18)  # 小标题字号
    pdf_canvas.drawString(210, 750, "Ticket Price Statistics")

    # 插入散点图
    scatter_chart_image_reader = ImageReader(scatter_chart_buffer)
    pdf_canvas.drawImage(scatter_chart_image_reader, 100, 390, width=400, height=400, preserveAspectRatio=True)

    # 插入饼状图
    chart_image_reader_ticket = ImageReader(chart_buffer_ticket)
    pdf_canvas.drawImage(chart_image_reader_ticket, 100, 100, width=400, height=400, preserveAspectRatio=True)

    # 保存票价统计信息
    pdf_canvas.setFont("Helvetica", 12)
    pdf_canvas.drawString(130, 130, "Ticket Price Ranges:")

    y_position_ticket = 110
    for range_name, count in ticket_price_ranges.items():
        pdf_canvas.drawString(250, y_position_ticket, f"{range_name}: {count}")
        y_position_ticket -= 20

    # 另起一页
    pdf_canvas.showPage()

    # 第三页

    # 设置PDF副标题
    pdf_canvas.setFont("Helvetica", 18)  # 小标题字号
    pdf_canvas.drawString(170, 750, "Flight Departure Time Statistics")

    # 插入散点图
    scatter_chart_image_reader = ImageReader(line_chart_departure_time)
    pdf_canvas.drawImage(scatter_chart_image_reader, 100, 400, width=390, height=400, preserveAspectRatio=True)

    # 插入饼状图
    chart_image_reader_ticket = ImageReader(chart_buffer_departure_time)
    pdf_canvas.drawImage(chart_image_reader_ticket, 100, 100, width=400, height=400, preserveAspectRatio=True)

    # 保存票价统计信息
    pdf_canvas.setFont("Helvetica", 12)
    pdf_canvas.drawString(130, 130, "Flight Departure Time Ranges:")

    y_position_ticket = 110
    for range_name, count in departure_time_ranges.items():
        pdf_canvas.drawString(250, y_position_ticket, f"{range_name}: {count}")
        y_position_ticket -= 20

    # 另起一页
    pdf_canvas.showPage()

    # 第四页

    # 设置PDF副标题
    pdf_canvas.setFont("Helvetica", 18)  # 小标题字号
    pdf_canvas.drawString(170, 750, "Flight Arrival Time Statistics")

    # 插入散点图
    scatter_chart_image_reader = ImageReader(line_chart_arrival_time)
    pdf_canvas.drawImage(scatter_chart_image_reader, 100, 400, width=390, height=400, preserveAspectRatio=True)

    # 插入饼状图
    chart_image_reader_ticket = ImageReader(chart_buffer_arrival_time)
    pdf_canvas.drawImage(chart_image_reader_ticket, 100, 100, width=400, height=400, preserveAspectRatio=True)

    # 保存票价统计信息
    pdf_canvas.setFont("Helvetica", 12)
    pdf_canvas.drawString(130, 130, "Flight Departure Time Ranges:")

    y_position_ticket = 110
    for range_name, count in arrival_time_ranges.items():
        pdf_canvas.drawString(250, y_position_ticket, f"{range_name}: {count}")
        y_position_ticket -= 20

    if flag:
        # 另起一页
        pdf_canvas.showPage()

        # 第五页

        # 设置PDF副标题
        pdf_canvas.setFont("Helvetica", 18)  # 小标题字号
        pdf_canvas.drawString(100, 750, "Affiliation Airports' Flight Departure Time Statistics")

        # 插入散点图
        scatter_chart_image_reader = ImageReader(line_chart_departure_time_user)
        pdf_canvas.drawImage(scatter_chart_image_reader, 100, 400, width=390, height=400, preserveAspectRatio=True)

        # 插入饼状图
        chart_image_reader_ticket = ImageReader(chart_buffer_departure_time_user)
        pdf_canvas.drawImage(chart_image_reader_ticket, 100, 100, width=400, height=400, preserveAspectRatio=True)

        # 保存票价统计信息
        pdf_canvas.setFont("Helvetica", 12)
        pdf_canvas.drawString(130, 130, "Flight Departure Time Ranges:")

        y_position_ticket = 110
        for range_name, count in departure_time_ranges_user.items():
            pdf_canvas.drawString(250, y_position_ticket, f"{range_name}: {count}")
            y_position_ticket -= 20

        # 另起一页
        pdf_canvas.showPage()

        # 第六页

        # 设置PDF副标题
        pdf_canvas.setFont("Helvetica", 18)  # 小标题字号
        pdf_canvas.drawString(110, 750, "Affiliation Airports' Flight Arrival Time Statistics")

        # 插入散点图
        scatter_chart_image_reader = ImageReader(line_chart_arrival_time_user)
        pdf_canvas.drawImage(scatter_chart_image_reader, 100, 400, width=390, height=400, preserveAspectRatio=True)

        # 插入饼状图
        chart_image_reader_ticket = ImageReader(chart_buffer_arrival_time_user)
        pdf_canvas.drawImage(chart_image_reader_ticket, 100, 100, width=400, height=400, preserveAspectRatio=True)

        # 保存票价统计信息
        pdf_canvas.setFont("Helvetica", 12)
        pdf_canvas.drawString(130, 130, "Flight Departure Time Ranges:")

        y_position_ticket = 110
        for range_name, count in arrival_time_ranges_user.items():
            pdf_canvas.drawString(250, y_position_ticket, f"{range_name}: {count}")
            y_position_ticket -= 20

    pdf_canvas.save()

def calculate_aircraft_count_ranges():
    aircraft_count_ranges = {'0-50': 0, '50-100': 0, '100-150': 0, '150-200': 0, '200+': 0}
    airlines = Airline.objects.all()

    for airline in airlines:
        aircraft_count = airline.aircraft_num
        if aircraft_count <= 50:
            aircraft_count_ranges['0-50'] += 1
        elif aircraft_count <= 100:
            aircraft_count_ranges['50-100'] += 1
        elif aircraft_count <= 150:
            aircraft_count_ranges['100-150'] += 1
        elif aircraft_count <= 200:
            aircraft_count_ranges['150-200'] += 1
        else:
            aircraft_count_ranges['200+'] += 1

    return aircraft_count_ranges

def calculate_ticket_price_ranges():
    ticket_price_ranges = {'0-1000': 0, '1000-2000': 0, '2000-5000': 0, '5000+': 0}
    tickets = RemainingTickets.objects.all()

    for ticket in tickets:
        ticket_price = ticket.ori_price
        if ticket_price <= 1000:
            ticket_price_ranges['0-1000'] += 1
        elif ticket_price <= 2000:
            ticket_price_ranges['1000-2000'] += 1
        elif ticket_price <= 5000:
            ticket_price_ranges['2000-5000'] += 1
        else:
            ticket_price_ranges['5000+'] += 1

    return ticket_price_ranges

def calculate_departure_time_ranges(flights):
    departure_time_ranges = {'00:00-06:00': 0, '06:00-12:00': 0, '12:00-18:00': 0, '18:00-24:00': 0}

    for flight in flights:
        departure_time = flight.departure_time.time()

        if pd.to_datetime('00:00:00').time() <= departure_time < pd.to_datetime('06:00:00').time():
            departure_time_ranges['00:00-06:00'] += 1
        elif pd.to_datetime('06:00:00').time() <= departure_time < pd.to_datetime('12:00:00').time():
            departure_time_ranges['06:00-12:00'] += 1
        elif pd.to_datetime('12:00:00').time() <= departure_time < pd.to_datetime('18:00:00').time():
            departure_time_ranges['12:00-18:00'] += 1
        else:
            departure_time_ranges['18:00-24:00'] += 1

    return departure_time_ranges

def calculate_arrival_time_ranges(flights):
    arrival_time_ranges = {'00:00-06:00': 0, '06:00-12:00': 0, '12:00-18:00': 0, '18:00-24:00': 0}

    for flight in flights:
        arrival_time = flight.arrival_time.time()

        if pd.to_datetime('00:00:00').time() <= arrival_time < pd.to_datetime('06:00:00').time():
            arrival_time_ranges['00:00-06:00'] += 1
        elif pd.to_datetime('06:00:00').time() <= arrival_time < pd.to_datetime('12:00:00').time():
            arrival_time_ranges['06:00-12:00'] += 1
        elif pd.to_datetime('12:00:00').time() <= arrival_time < pd.to_datetime('18:00:00').time():
            arrival_time_ranges['12:00-18:00'] += 1
        else:
            arrival_time_ranges['18:00-24:00'] += 1

    return arrival_time_ranges

def generate_line_chart(departure_time_ranges):
    labels = list(departure_time_ranges.keys())
    values = list(departure_time_ranges.values())

    plt.figure(figsize=(8, 6))
    plt.plot(labels, values, marker='o')
    plt.title('Arrival Time Distribution')
    plt.xlabel('Arrival Time Range')
    plt.ylabel('Count')
    plt.grid(True)

    # 保存图表到 BytesIO 缓冲区
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    return buffer
def generate_line_chart_arrival_time(departure_time_ranges):
    labels = list(departure_time_ranges.keys())
    values = list(departure_time_ranges.values())

    plt.figure(figsize=(8, 6))
    plt.plot(labels, values, marker='o')
    plt.title('Departure Time Distribution')
    plt.xlabel('Departure Time Range')
    plt.ylabel('Count')
    plt.grid(True)

    # 保存图表到 BytesIO 缓冲区
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    return buffer
def generate_pie_chart(aircraft_count_ranges):
    labels = list(aircraft_count_ranges.keys())
    sizes = list(aircraft_count_ranges.values())

    plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用中文黑体

    # 检查是否所有值都是零
    if all(size == 0 for size in sizes):
        # 如果所有值都是零，设置默认值
        sizes = [1] * len(sizes)  # 使用默认值1
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    # 保存图表到 BytesIO 缓冲区
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    return buffer

def generate_scatter_chart(tickets):
    # 创建数据框
    data = {'Ticket Price': [ticket.ori_price for ticket in tickets]}
    df = pd.DataFrame(data)

    # 绘制散点图
    plt.figure(figsize=(8, 6))
    plt.scatter(df['Ticket Price'], range(len(df)), alpha=0.5)
    plt.title('Ticket Price Distribution')
    plt.xlabel('Ticket Price')
    plt.ylabel('Count')
    plt.grid(True)

    # 保存图表到 BytesIO 缓冲区
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    return buffer

def generate_scatter_chart_airlines(tickets):
    # 创建数据框
    data = {'Airline Aircraft': [ticket.aircraft_num for ticket in tickets]}
    df = pd.DataFrame(data)

    # 绘制散点图
    plt.figure(figsize=(8, 6))
    plt.scatter(df['Airline Aircraft'], range(len(df)), alpha=0.5)
    plt.title('Airlines\' Present Fleet of Aircraft Distribution')
    plt.xlabel('Airlines\' Present Fleet of Aircraft')
    plt.ylabel('Count')
    plt.grid(True)

    # 保存图表到 BytesIO 缓冲区
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    return buffer

def generate_scatter_chart_range(ticket_price_ranges):
    labels = list(ticket_price_ranges.keys())
    sizes = list(ticket_price_ranges.values())

    # 创建数据框
    data = {'Price Range': labels, 'Count': sizes}
    df = pd.DataFrame(data)

    # 绘制散点图
    plt.figure(figsize=(8, 6))
    plt.scatter(df['Price Range'], df['Count'], s=df['Count'] * 10, alpha=0.5)
    plt.title('Ticket Price Statistics')
    plt.xlabel('Price Range')
    plt.ylabel('Count')
    plt.grid(True)

    # 保存图表到 BytesIO 缓冲区
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    return buffer
