from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404

from myapp.apiResponse import APIResponse
from myapp.models import Ticket, RemainingTickets, Flight
from myapp.serializers import TicketSerializer, RemainingTicketsSerializer


@api_view(['POST'])
def refund_ticket(request):
    try:
        ticket_code = request.GET.get('ticket_code')
        ticket = Ticket.objects.get(ticket_code=ticket_code)
    except Ticket.DoesNotExist:
        return APIResponse(myStatus=False, msg='未找到订单', data={"ticket_code":ticket_code})

    if ticket.status == 'refunded':
        return APIResponse(myStatus=False, msg='订单已退票，重复退票操作', data={"ticket_code":ticket_code})
    elif ticket.status == 'used':
        return APIResponse(myStatus=False, msg='订单已使用，退票失败', data={"ticket_code":ticket_code})

    ticket.status = 'refunded'
    ticket.save()
    # update remain_ticket
    remaining_ticket = RemainingTickets.objects.get(flight=ticket.flight, cabin_class=ticket.cabin_class)
    remaining_ticket.mark_seat_as_available(ticket.seat_num) # 退票，可用余票数增加
    remaining_ticket.save()

    serializer = TicketSerializer(ticket)
    return APIResponse(myStatus=True, msg='退票成功', data=serializer.data)

@api_view(['POST'])
def purchase_ticket(request):
    seat_num = request.data.get('seat_num')
    cabin_class = request.data.get('cabin_class')
    ticket_price = request.data.get('ticket_price')
    passenger_id = request.data.get('passenger_id')
    flight_id = request.data.get('flight_id')

    try:
        remaining_tickets_list = RemainingTickets.objects.filter(
            Q(flight=flight_id) & Q(cabin_class=cabin_class)
        )
    except RemainingTickets.DoesNotExist:
        return APIResponse(myStatus=False, msg='未找到相关航班的余票信息', data={"flight_id":flight_id})
    if not remaining_tickets_list.exists():
        return APIResponse(myStatus=False, msg='未找到相关航班的余票信息', data={"flight_id": flight_id})
    remaining_tickets = remaining_tickets_list[0]

    if remaining_tickets.available_num <= 0:
        return APIResponse(myStatus=False, msg='余票不足，购票失败', data={"flight_id":flight_id})
    elif not remaining_tickets.is_seat_available(seat_num):
        return APIResponse(myStatus=False, msg='该座位已售出，购票失败', data={"flight_id": flight_id})

    # 在这里执行你的购票逻辑，例如创建 Ticket 记录
    ticket = Ticket.objects.create(
        seat_num=seat_num,
        cabin_class=cabin_class,
        ticket_price=ticket_price,
        passenger_id=passenger_id,
        flight_id=flight_id,
        status='booked'  # 新购票的初始状态
    )

    # 更新余票信息
    remaining_tickets.mark_seat_as_purchased(seat_num)
    remaining_tickets.save()

    serializer = TicketSerializer(ticket)
    return APIResponse(myStatus=True, msg='购票成功', data=serializer.data)

@api_view(['POST'])
def search_tickets(request):
    try:
        # 获取航班号和舱位等级
        flight_id = request.data.get('flight_id')
        cabin_class = request.data.get('cabin_class')

        # 获取航班对象
        flight = Flight.objects.get(flight_id=flight_id)

        # 获取相关余票信息
        remaining_tickets = RemainingTickets.objects.filter(
            Q(flight=flight) & Q(cabin_class=cabin_class)
        )

        if remaining_tickets.exists():
            # 序列化所有匹配的余票信息
            serializer = RemainingTicketsSerializer(remaining_tickets, many=True)
            return APIResponse(myStatus=True, msg='成功获取余票信息', data=serializer.data[0])
        else:
            return APIResponse(myStatus=False, msg='未找到相关余票信息', data=None)

    except Exception as e:
        return APIResponse(myStatus=False, msg=str(e), data=None)

@api_view(['POST'])
def change_ticket(request):
    try:
        seat_num = request.data.get('tar_seat_num')
        cabin_class = request.data.get('tar_cabin_class')
        # 获取原始票务信息
        ori_ticket_id = request.data.get('ori_ticket_id')
        original_ticket = get_object_or_404(Ticket, ticket_code=ori_ticket_id)
        # 获取目标航班信息
        tar_flight_id = request.data.get('tar_flight_id')
        target_flight = get_object_or_404(Flight, flight_id=tar_flight_id)

        tar_remaining_tickets = RemainingTickets.objects.filter(
                Q(flight=tar_flight_id) & Q(cabin_class=cabin_class)
            )

        if not tar_remaining_tickets.exists():
            return APIResponse(myStatus=False, msg='未找到对应航班')

        if tar_remaining_tickets[0].available_num <= 0:
            return APIResponse(myStatus=False, msg='余票不足，购票失败', data={"flight_id": tar_flight_id})
        elif not tar_remaining_tickets[0].is_seat_available(seat_num):
            return APIResponse(myStatus=False, msg='该座位已售出，购票失败', data={"flight_id": tar_flight_id})

        # 标记原始票务为已改签
        original_ticket.status = 'refunded'
        original_ticket.save()
        ori_remain_ticket = RemainingTickets.objects.filter(
            Q(flight=original_ticket.flight) & Q(cabin_class=original_ticket.cabin_class)
        )
        ori_remain_ticket[0].mark_seat_as_available(original_ticket.seat_num)

        # 创建 Ticket 记录
        ticket = Ticket.objects.create(
            seat_num=seat_num,
            cabin_class=cabin_class,
            ticket_price=tar_remaining_tickets[0].ori_price,
            passenger_id=original_ticket.passenger_id,
            flight_id=tar_flight_id,
            status='booked'  # 新购票的初始状态
        )

        # 更新余票信息
        tar_remaining_tickets[0].mark_seat_as_purchased(seat_num)
        tar_remaining_tickets[0].save()

        serializer = TicketSerializer(ticket)
        return APIResponse(myStatus=True, msg= '改签成功', data=serializer.data)
    except Exception as e:
        return APIResponse(myStatus=False, msg=str(e), data=None)

