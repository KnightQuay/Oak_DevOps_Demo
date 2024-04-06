from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from rest_framework.exceptions import ValidationError


# Create your models here.

class Airline(models.Model):
    company_id = models.BigAutoField(primary_key=True)
    company_name_chinese = models.CharField(max_length=100)
    company_code = models.CharField(max_length=10, null=True, blank=True)
    company_loc = models.CharField(max_length=100, blank=True, null=True)
    aircraft_num = models.IntegerField(default=0, verbose_name="present fleet of aircraft")
    website_url = models.CharField(max_length=100, blank=True, null=True)
    prefix = models.CharField(max_length=100)
    class Meta:
        db_table = 'my_airline'

class Aircraft(models.Model):
    STATUS_CHOICES = (
        ('-1', '报废'),
        ('0', '维修'),
        ('1', '正常'),
    )
    aircraft_id = models.BigAutoField(primary_key=True)
    # 多对一外键，级联删除，反向命名 airline.aircrafts.all()
    airline = models.ForeignKey(Airline, on_delete=models.CASCADE
                                , related_name="aircrafts")
    seats_num = models.IntegerField(default=0)
    age = models.IntegerField(default=0)
    aircraft_model = models.CharField(max_length=30)
    aircraft_mileage = models.IntegerField(default=0, null=True, blank=True)
    WIFI_availability = models.BooleanField(default=False, null=True, blank=True)
    status = models.CharField(max_length=3, choices=STATUS_CHOICES, default='1')

    class Meta:
        db_table = 'my_aircraft'

class Airport(models.Model):
    code = models.CharField(max_length=3, unique=True, primary_key=True)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, null=True, blank=True)
    lounge_count = models.PositiveIntegerField(null=True, blank=True)
    parking_spaces = models.PositiveIntegerField(null=True, blank=True)
    terminal_num = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'my_airport'
        indexes = [
            models.Index(fields=['code'], name='airport_code_index'),
        ]

class Flight(models.Model):
    FLIGHT_STATUS_CHOICES = (
        ('scheduled', '已安排'),
        ('departed', '已起飞'),
        ('arrived', '已降落'),
        ('canceled', '已取消'),
    )
    flight_id = models.BigAutoField(primary_key=True)
    flight_code = models.CharField(max_length=20)
    departure_airport = models.ForeignKey(
        Airport,
        on_delete=models.CASCADE,
        related_name="departures")
    departure_time = models.DateTimeField()
    arrival_airport = models.ForeignKey(
        Airport,
        on_delete=models.CASCADE,
        related_name="arrivals")
    arrival_time = models.DateTimeField()
    operating_aircraft = models.ForeignKey(
        Aircraft,
        on_delete=models.CASCADE,
        related_name="flights")
    status = models.CharField(max_length=20, choices=FLIGHT_STATUS_CHOICES, default='scheduled')

    def __str__(self):
        return f"{self.flight_code} - {self.departure_airport} to {self.arrival_airport}"

    class Meta:
        db_table = "my_flight"

class FlightCode(models.Model):
    flight_code = models.CharField(max_length=20)
    flight_id = models.OneToOneField(Flight, on_delete=models.CASCADE, related_name="my_flight_code")

class FlightDepartureInfo(models.Model):
    flight = models.OneToOneField(
        Flight,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="departureInfo")
    terminal = models.CharField(max_length=10, null=True, blank=True)
    check_in_counter = models.CharField(max_length=10, null=True, blank=True)
    boarding_gate = models.CharField(max_length=10)
    boarding_time = models.DateTimeField()

    def __str__(self):
        return f"{self.flight.flight_code} - Terminal: {self.terminal}, Check-in Counter: {self.check_in_counter}"

    class Meta:
        db_table = "my_flight_departure_info"

class RemainingTickets(models.Model):
    ticket_type_id = models.BigAutoField(primary_key=True)
    flight = models.ForeignKey(
        Flight,
        on_delete=models.CASCADE,
        related_name="remainingTickets")
    ori_price = models.IntegerField()
    total_num = models.IntegerField()
    available_num = models.IntegerField()
    discount_percentage = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)])
    cabin_class = models.CharField(max_length=30)
    purchased_seats = models.CharField(max_length=3000, default='')

    def __str__(self):
        return f"Flight Ticket for {self.flight.flight_code} - Available: {self.available_num}/{self.total_num}, Discount: {self.discount_percentage}%"

    def is_seat_available(self, seat_num):
        return str(seat_num) not in self.purchased_seats.split(',')

    def mark_seat_as_purchased(self, seat_num):
        if not self.is_seat_available(seat_num):
            return False  # 座位已经被购买
        else:
            if self.purchased_seats:
                self.purchased_seats += f',{seat_num}'
            else:
                self.purchased_seats = seat_num
            self.available_num -= 1
            self.save()
            return True  # 座位购买成功

    def mark_seat_as_available(self, seat_num):
        if not self.is_seat_available(seat_num):
            # 座位已购买，从 purchased_seats 中移除
            purchased_seats_list = self.purchased_seats.split(',')
            purchased_seats_list.remove(seat_num)
            self.purchased_seats = ','.join(purchased_seats_list)
            self.available_num += 1
            self.save()
            return True  # 座位标记为可用成功
        else:
            return False  # 座位本来就是可用的

    class Meta:
        db_table = "my_remaining_tickets"

class User(models.Model):
    USER_TYPE_CHOICES = (
        ('airline_member', '航空公司成员'),
        ('airport_member', '机场成员'),
        ('admin', '管理员'),
        ('normal_user', '普通用户'),
    )
    user_nickname = models.CharField(max_length=100, default="null")
    # user_id = models.BigAutoField(primary_key=True)
    user_email = models.CharField(max_length=50, unique=True, primary_key=True)
    user_auth = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='normal_user')
    user_tel = models.CharField(max_length=100, blank=True, null=True)
    user_password = models.CharField(max_length=100)
    user_address = models.CharField(max_length=100, blank=True, null=True)
    user_icon_url = models.CharField(max_length=1000, blank=True, null=True)
    airport_affiliation = models.ForeignKey(
        Airport,
        on_delete=models.CASCADE,
        null=True, blank=True)
    airline_affiliation = models.ForeignKey(
        Airline,
        on_delete=models.CASCADE,
        null=True,
        blank=True)
    token = models.CharField(max_length=500, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.user_auth == 'admin' or self.user_auth == 'normal_user':
            # 如果用户类型是管理员，确保外键为空
            self.airport_affiliation = None
            self.airline_affiliation = None
        elif self.user_auth == 'airport_member':
            # 如果用户类型是机场成员，确保航空公司外键为空
            self.airline_affiliation = None
        elif self.user_auth == 'airline_member':
            # 如果用户类型是航空公司成员，确保机场外键为空
            self.airport_affiliation = None
        else:
            # 如果用户类型无效，抛出 ValidationError
            raise ValidationError("Invalid user type.")

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user_email} - {self.get_user_auth_display()}"

    class Meta:
        managed = True
        db_table = 'my_user'
        indexes = [
            models.Index(fields=['user_email'], name='email_index')
        ]

class Passenger(models.Model):
    GENDER=(
        ('male', '男'),
        ('female', '女'),
    )
    name = models.CharField(max_length=100)
    id_number = models.CharField(max_length=18, unique=True, primary_key=True)
    gender = models.CharField(max_length=10, choices=GENDER)
    age = models.PositiveIntegerField(
        validators=[MaxValueValidator(200)])
    phone_number = models.CharField(max_length=20)
    email = models.CharField(max_length=100, blank=True, null=True)
    id_type = models.CharField(max_length=50, blank=True, null=True)
    affiliate_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="passengers",
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.name} ({self.id_number})"

    class Meta:
        db_table = 'my_passenger'

class Ticket(models.Model):
    TICKET_STATUS_CHOICES = (
        ('booked', '已购票'),
        ('used', '已使用'),
        ('refunded', '已退票'),
    )
    ticket_code = models.AutoField(primary_key=True)
    seat_num = models.CharField(max_length=10)
    cabin_class = models.CharField(max_length=20)
    ticket_price = models.PositiveIntegerField()
    passenger = models.ForeignKey(
        Passenger,
        on_delete=models.CASCADE,
        related_name='tickets')
    flight = models.ForeignKey(
        Flight,
        on_delete=models.CASCADE,
        related_name='tickets')
    status = models.CharField(
        max_length=10,
        choices=TICKET_STATUS_CHOICES,
        default='booked'
    )

    def __str__(self):
        return f"Order: {self.ticket_code} - {self.passenger} - {self.flight}"

    class Meta:
        db_table = 'my_ticket'

class AddFlightValidation(models.Model):
    PROGRESS_CHOICES = [
        ('pending', '审核中'),
        ('completed', '已完成'),
        ('rejected', '已拒绝'),
    ]

    id = models.AutoField(primary_key=True)
    initiator_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='airport_initiated_reviews')
    reviewing_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='airport_reviewed_reviews'
                                       , blank=True, null=True)
    progress = models.CharField(max_length=20, choices=PROGRESS_CHOICES, default='pending')
    # 机场信息
    FLIGHT_STATUS_CHOICES = (
        ('scheduled', '已安排'),
        ('departed', '已起飞'),
        ('arrived', '已降落'),
        ('canceled', '已取消'),
    )
    # flight_id = models.BigIntegerField()
    flight_code = models.CharField(max_length=20)
    departure_airport = models.ForeignKey(
        Airport,
        on_delete=models.CASCADE,
        related_name="new_departures")
    departure_time = models.DateTimeField()
    arrival_airport = models.ForeignKey(
        Airport,
        on_delete=models.CASCADE,
        related_name="new_arrivals")
    arrival_time = models.DateTimeField()
    operating_aircraft = models.ForeignKey(
        Aircraft,
        on_delete=models.CASCADE,
        related_name="new_flights")
    status = models.CharField(max_length=20, choices=FLIGHT_STATUS_CHOICES, default='scheduled')
    def __str__(self):
        return f"AddFlight Review ID: {self.id}, Status: {self.progress}"

    class Meta:
        db_table = 'my_add_flight_validation'

class AddAircraftValidation(models.Model):
    PROGRESS_CHOICES = [
        ('pending', '审核中'),
        ('completed', '已完成'),
        ('rejected', '已拒绝'),
    ]

    id = models.AutoField(primary_key=True)
    initiator_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='aircraft_initiated_reviews')
    reviewing_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='aircraft_reviewed_reviews'
                                       , blank=True, null=True)
    progress = models.CharField(max_length=20, choices=PROGRESS_CHOICES, default='pending')
    # 飞机信息
    STATUS_CHOICES = (
        ('-1', '报废'),
        ('0', '维修'),
        ('1', '正常'),
    )
    # aircraft_id = models.BigAutoField(primary_key=True)
    # 多对一外键，级联删除，反向命名 airline.aircrafts.all()
    airline = models.ForeignKey(Airline, on_delete=models.CASCADE
                                , related_name="new_aircrafts")
    seats_num = models.IntegerField(default=0)
    age = models.IntegerField(default=0)
    aircraft_model = models.CharField(max_length=30)
    aircraft_mileage = models.IntegerField(default=0, null=True, blank=True)
    WIFI_availability = models.BooleanField(default=False, null=True, blank=True)
    status = models.CharField(max_length=3, choices=STATUS_CHOICES, default='1')

    def __str__(self):
        return f"AddAircraft Review ID: {self.id}, Status: {self.progress}"

    class Meta:
        db_table = 'my_add_aircraft_validation'

class LoginLog(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_email = models.CharField(max_length=50, blank=True, null=True)
    ip = models.CharField(max_length=100, blank=True, null=True)
    ua = models.CharField(max_length=200, blank=True, null=True)
    log_time = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        db_table = "my_login_log"