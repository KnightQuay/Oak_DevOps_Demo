# Generated by Django 4.2.3 on 2023-12-22 16:46

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AddAircraftValidation',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('progress', models.CharField(choices=[('pending', '审核中'), ('completed', '已完成'), ('rejected', '已拒绝')], default='pending', max_length=20)),
                ('seats_num', models.IntegerField(default=0)),
                ('age', models.IntegerField(default=0)),
                ('aircraft_model', models.CharField(max_length=30)),
                ('aircraft_mileage', models.IntegerField(blank=True, default=0, null=True)),
                ('WIFI_availability', models.BooleanField(blank=True, default=False, null=True)),
                ('status', models.CharField(choices=[('-1', '报废'), ('0', '维修'), ('1', '正常')], default='1', max_length=3)),
            ],
            options={
                'db_table': 'my_add_aircraft_validation',
            },
        ),
        migrations.CreateModel(
            name='AddFlightValidation',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('progress', models.CharField(choices=[('pending', '审核中'), ('completed', '已完成'), ('rejected', '已拒绝')], default='pending', max_length=20)),
                ('flight_code', models.CharField(max_length=20)),
                ('departure_time', models.DateTimeField()),
                ('arrival_time', models.DateTimeField()),
                ('status', models.CharField(choices=[('scheduled', '已安排'), ('departed', '已起飞'), ('arrived', '已降落'), ('canceled', '已取消')], default='scheduled', max_length=20)),
            ],
            options={
                'db_table': 'my_add_flight_validation',
            },
        ),
        migrations.CreateModel(
            name='Aircraft',
            fields=[
                ('aircraft_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('seats_num', models.IntegerField(default=0)),
                ('age', models.IntegerField(default=0)),
                ('aircraft_model', models.CharField(max_length=30)),
                ('aircraft_mileage', models.IntegerField(blank=True, default=0, null=True)),
                ('WIFI_availability', models.BooleanField(blank=True, default=False, null=True)),
                ('status', models.CharField(choices=[('-1', '报废'), ('0', '维修'), ('1', '正常')], default='1', max_length=3)),
            ],
            options={
                'db_table': 'my_aircraft',
            },
        ),
        migrations.CreateModel(
            name='Airline',
            fields=[
                ('company_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('company_name_chinese', models.CharField(max_length=100)),
                ('company_code', models.CharField(blank=True, max_length=10, null=True)),
                ('company_loc', models.CharField(blank=True, max_length=100, null=True)),
                ('aircraft_num', models.IntegerField(default=0, verbose_name='present fleet of aircraft')),
                ('website_url', models.CharField(blank=True, max_length=100, null=True)),
                ('prefix', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'my_airline',
            },
        ),
        migrations.CreateModel(
            name='Airport',
            fields=[
                ('code', models.CharField(max_length=3, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=255)),
                ('phone', models.CharField(blank=True, max_length=20, null=True)),
                ('lounge_count', models.PositiveIntegerField(blank=True, null=True)),
                ('parking_spaces', models.PositiveIntegerField(blank=True, null=True)),
                ('terminal_num', models.PositiveIntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'my_airport',
            },
        ),
        migrations.CreateModel(
            name='Flight',
            fields=[
                ('flight_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('flight_code', models.CharField(max_length=20)),
                ('departure_time', models.DateTimeField()),
                ('arrival_time', models.DateTimeField()),
                ('status', models.CharField(choices=[('scheduled', '已安排'), ('departed', '已起飞'), ('arrived', '已降落'), ('canceled', '已取消')], default='scheduled', max_length=20)),
                ('arrival_airport', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='arrivals', to='myapp.airport')),
                ('departure_airport', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='departures', to='myapp.airport')),
                ('operating_aircraft', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='flights', to='myapp.aircraft')),
            ],
            options={
                'db_table': 'my_flight',
            },
        ),
        migrations.CreateModel(
            name='LoginLog',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('user_email', models.CharField(blank=True, max_length=50, null=True)),
                ('ip', models.CharField(blank=True, max_length=100, null=True)),
                ('ua', models.CharField(blank=True, max_length=200, null=True)),
                ('log_time', models.DateTimeField(auto_now_add=True, null=True)),
            ],
            options={
                'db_table': 'my_login_log',
            },
        ),
        migrations.CreateModel(
            name='Passenger',
            fields=[
                ('name', models.CharField(max_length=100)),
                ('id_number', models.CharField(max_length=18, primary_key=True, serialize=False, unique=True)),
                ('gender', models.CharField(choices=[('male', '男'), ('female', '女')], max_length=10)),
                ('age', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(200)])),
                ('phone_number', models.CharField(max_length=20)),
                ('email', models.CharField(blank=True, max_length=100, null=True)),
                ('id_type', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'db_table': 'my_passenger',
            },
        ),
        migrations.CreateModel(
            name='FlightDepartureInfo',
            fields=[
                ('flight', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='departureInfo', serialize=False, to='myapp.flight')),
                ('terminal', models.CharField(blank=True, max_length=10, null=True)),
                ('check_in_counter', models.CharField(blank=True, max_length=10, null=True)),
                ('boarding_gate', models.CharField(max_length=10)),
                ('boarding_time', models.DateTimeField()),
            ],
            options={
                'db_table': 'my_flight_departure_info',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_nickname', models.CharField(default='null', max_length=100)),
                ('user_email', models.CharField(max_length=50, primary_key=True, serialize=False, unique=True)),
                ('user_auth', models.CharField(choices=[('airline_member', '航空公司成员'), ('airport_member', '机场成员'), ('admin', '管理员'), ('normal_user', '普通用户')], default='normal_user', max_length=20)),
                ('user_tel', models.CharField(blank=True, max_length=100, null=True)),
                ('user_password', models.CharField(max_length=100)),
                ('user_address', models.CharField(blank=True, max_length=100, null=True)),
                ('user_icon_url', models.CharField(blank=True, max_length=1000, null=True)),
                ('token', models.CharField(blank=True, max_length=500, null=True)),
                ('airline_affiliation', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.airline')),
                ('airport_affiliation', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.airport')),
            ],
            options={
                'db_table': 'my_user',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('ticket_code', models.AutoField(primary_key=True, serialize=False)),
                ('seat_num', models.CharField(max_length=10)),
                ('cabin_class', models.CharField(max_length=20)),
                ('ticket_price', models.PositiveIntegerField()),
                ('status', models.CharField(choices=[('booked', '已购票'), ('used', '已使用'), ('refunded', '已退票')], default='booked', max_length=10)),
                ('flight', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tickets', to='myapp.flight')),
                ('passenger', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tickets', to='myapp.passenger')),
            ],
            options={
                'db_table': 'my_ticket',
            },
        ),
        migrations.CreateModel(
            name='RemainingTickets',
            fields=[
                ('ticket_type_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('ori_price', models.IntegerField()),
                ('total_num', models.IntegerField()),
                ('available_num', models.IntegerField()),
                ('discount_percentage', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('cabin_class', models.CharField(max_length=30)),
                ('purchased_seats', models.CharField(default='', max_length=3000)),
                ('flight', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='remainingTickets', to='myapp.flight')),
            ],
            options={
                'db_table': 'my_remaining_tickets',
            },
        ),
        migrations.AddField(
            model_name='passenger',
            name='affiliate_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='passengers', to='myapp.user'),
        ),
        migrations.CreateModel(
            name='FlightCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flight_code', models.CharField(max_length=20)),
                ('flight_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='my_flight_code', to='myapp.flight')),
            ],
        ),
        migrations.AddIndex(
            model_name='airport',
            index=models.Index(fields=['code'], name='airport_code_index'),
        ),
        migrations.AddField(
            model_name='aircraft',
            name='airline',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='aircrafts', to='myapp.airline'),
        ),
        migrations.AddField(
            model_name='addflightvalidation',
            name='arrival_airport',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='new_arrivals', to='myapp.airport'),
        ),
        migrations.AddField(
            model_name='addflightvalidation',
            name='departure_airport',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='new_departures', to='myapp.airport'),
        ),
        migrations.AddField(
            model_name='addflightvalidation',
            name='initiator_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='airport_initiated_reviews', to='myapp.user'),
        ),
        migrations.AddField(
            model_name='addflightvalidation',
            name='operating_aircraft',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='new_flights', to='myapp.aircraft'),
        ),
        migrations.AddField(
            model_name='addflightvalidation',
            name='reviewing_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='airport_reviewed_reviews', to='myapp.user'),
        ),
        migrations.AddField(
            model_name='addaircraftvalidation',
            name='airline',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='new_aircrafts', to='myapp.airline'),
        ),
        migrations.AddField(
            model_name='addaircraftvalidation',
            name='initiator_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='aircraft_initiated_reviews', to='myapp.user'),
        ),
        migrations.AddField(
            model_name='addaircraftvalidation',
            name='reviewing_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='aircraft_reviewed_reviews', to='myapp.user'),
        ),
        migrations.AddIndex(
            model_name='user',
            index=models.Index(fields=['user_email'], name='email_index'),
        ),
    ]
