from django.contrib import admin
from .models import Airport, Flight, Account, TicketType, FlightTicketType, Booking, Payment, Card, Voucher

admin.site.register(Airport)
@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = ('flight_number', 'departure_airport', 'arrival_airport', 'departure_time', 'arrival_time', 'base_price')
    list_filter = ('departure_airport', 'arrival_airport', 'departure_time', 'arrival_time')
    search_fields = ('flight_number', 'departure_airport__name', 'arrival_airport__name')
admin.site.register(Account)
admin.site.register(TicketType)
admin.site.register(FlightTicketType)
admin.site.register(Booking)
admin.site.register(Payment)
admin.site.register(Card)
admin.site.register(Voucher)
