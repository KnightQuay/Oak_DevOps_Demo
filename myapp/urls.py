from django.contrib import admin
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

# 子路由
from myapp import views

urlpatterns = [
    path('user/login/', views.login),
    path('user/sign_up/', views.register),
    path('user/add_passenger/', views.add_passenger_to_current_user),
    path('user/get_user_by_email/', views.get_user_by_email),
    path('user/get_tickets/', views.get_tickets),
    path('user/get_passengers/', views.get_passengers),

    path('ticket/refund/', views.refund_ticket),
    path('ticket/book/', views.purchase_ticket),
    path('ticket/search/', views.search_tickets),
    path('ticket/change/', views.change_ticket),

    path('flight/get_available_flights_time/', views.get_available_flights_time),
    path('flight/get_available_flights_date/', views.get_available_flights_date),
    path('flight/get_airports_with_departures/', views.get_airports_with_departures),
    path('flight/get_airports_with_arrivals/', views.get_airports_with_arrivals),

    path('validation/get_items/', views.get_items),
    path('validation/get_validation_list/', views.get_validation_list),
    path('validation/add_flight/', views.add_flight),
    path('validation/add_aircraft/', views.add_aircraft),
    path('validation/accept/', views.accept),
    path('validation/reject/', views.reject),
    path('validation/remove/', views.remove),

    path('search/select/', views.get_related_data),

    path('excel/upload_airport_data/', views.upload_airport_data),
    path('excel/upload_aircraft_data/', views.upload_aircraft_data),
    path('excel/upload_passenger_data/', views.upload_passenger_data),
    path('excel/upload_flight_data/', views.upload_flight_data),
    path('excel/upload_ticket_data/', views.upload_ticket_data),

    path('statistics/generate_statistics/', views.generate_statistics)
]
