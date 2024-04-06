from django.contrib import admin

from myapp.models import Airline, Aircraft, Airport, Flight, FlightDepartureInfo, RemainingTickets, User, Passenger, \
    Ticket, AddFlightValidation, AddAircraftValidation, LoginLog

# Register your models here.
admin.site.register([Airline, Aircraft, Airport, Flight, FlightDepartureInfo, RemainingTickets, User, Passenger, Ticket, AddFlightValidation, AddAircraftValidation, LoginLog])
