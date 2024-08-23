from django.shortcuts import render, HttpResponse, HttpResponseRedirect, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from .forms import *
from .models import *
from django.shortcuts import render, get_object_or_404
from .models import Flight, Airport
from django.db.models import Min, Q, F
import json
from django.contrib.auth.decorators import login_required, user_passes_test
from datetime import timedelta

# Create your views here.
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, _("You've been logged in successfully"))
                return HttpResponseRedirect(reverse("index"))
            else:
                messages.error(request, _("Invalid username and/or password"))
                return render(request, "login.html", {'form': form})
        else:
            messages.error(request, _("This username is not valid. Username should contain alphanumeric characters only."))
            return render(request, "login.html", {'form': form})
    else:
        form = LoginForm()
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "login.html", {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            try:
                account = form.save(commit=False)
                account.set_password(form.cleaned_data["password"])
                account.save()
            except:
                messages.error(request, _("Username already exists"))
                return render(request, "register.html", {'form': form})
            account = authenticate(request, username=form.cleaned_data["username"], password=form.cleaned_data["password"])
            login(request, account)
            return redirect('index')
        else:
            messages.error(request, _("Information is not valid. Please check information again."))
            return render(request, "register.html", {'form': form})
    else:
        form = SignUpForm()
        return render(request, "register.html", {'form': form})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def __get_airports():
    """Retrieve all airports from the database."""
    airports = Airport.objects.all().values("airport_code", "name", "city", "country")
    return list(airports)

def __get_ticket_types():
    """Retrieve all ticket types from the database."""
    ticket_types = TicketType.objects.all().values("ticket_type_id", "name")
    return list(ticket_types)

def __get_available_flights(departure_airport, arrival_airport, departure_date, num_passengers, chair_type_name):
    return Flight.objects.filter(
        departure_airport=departure_airport,
        arrival_airport=arrival_airport,
        departure_time__date=departure_date,
        flighttickettype__available_seats__gte=num_passengers,
        flighttickettype__ticket_type__name=chair_type_name
    ).annotate(
        min_price=Min(
            "flighttickettype__price",
            filter=Q(flighttickettype__available_seats__gte=num_passengers)
        ),
        ticket_type_price=F("flighttickettype__price")
    ).order_by("min_price")


def index(request):
    trip_type = request.GET.get("tripType")
    from_airport = request.GET.get("from")
    to_airport = request.GET.get("to")
    departure_date = request.GET.get("departureDate")
    return_date = request.GET.get("returnDate")
    num_passengers = int(request.GET.get("numPassengers", 1))  # Default to 1 if not provided
    chair_type_name = request.GET.get("chairType")

    context = {
        "trip_type": trip_type,
        "from_airport": from_airport,
        "to_airport": to_airport,
        "departure_date": departure_date,
        "return_date": return_date,
        "num_passengers": num_passengers,
        "chair_type": chair_type_name,
        "airports": json.dumps(__get_airports()),
        "ticket_types": __get_ticket_types(),
    }

    # If required fields are missing, return to the homepage
    if not from_airport:
        context["error_message"] = _("Please select a departure airport.")
    if not to_airport:
        context["error_message"] = _("Please select an arrival airport.")
    if not departure_date:
        context["error_message"] = _("Please select a departure date.")
    if trip_type == "round" and not return_date:
        context["error_message"] = _("Please select a return date.")
    if not chair_type_name:
        context["error_message"] = _("Please select a chair type.")
    if not num_passengers:
        context["error_message"] = _("Please select the number of passengers.")

    # If departure and destination are the same, return to the homepage
    if from_airport == to_airport:
        context["error_message"] = _("Departure and destination airports cannot be the same.")

    if context.get("error_message"):
        return render(request, "homepage.html", context)
    
    # Filter flights by chair type and available seats
    departure_flights = __get_available_flights(from_airport, to_airport, departure_date, num_passengers, chair_type_name)
    if not departure_flights:
        context["error_message"] = _("No flights available with the selected criteria. Please try again.")
        return render(request, "homepage.html", context)

    context["departure_flights"] = departure_flights

    # If round trip, get return flights with the same conditions
    if trip_type == "round":
        return_flights = __get_available_flights(to_airport, from_airport, return_date, num_passengers, chair_type_name)
        if not return_flights:
            context["error_message"] = _("No return flights available with the selected criteria. Please try again.")
            return render(request, "homepage.html", context)
        context["return_flights"] = return_flights

    return render(request, "homepage.html", context)

def flight_detail(request, flight_id):
    flight = get_object_or_404(Flight, flight_id=flight_id)
    departure_airport = flight.departure_airport
    arrival_airport = flight.arrival_airport
    
    context = {
        'flight': flight,
        'departure_airport': departure_airport,
        'arrival_airport': arrival_airport,
    }
    
    return render(request, 'flight_detail.html', context)

def flight_list(request):
    flights = Flight.objects.all()
    departure_date = request.GET.get('departure_date')
    if departure_date:
        flights = flights.filter(departure_time__date=departure_date)
    departure_location = request.GET.get('departure_location')
    if departure_location:
        flights = flights.filter(departure_airport__city=departure_location)
    airports = Airport.objects.values_list('city', flat=True).distinct()
    context = {
        'flights': flights,
        'airports': airports,
    }
    return render(request, 'flight_list.html', context)
@login_required
def user_bookings(request):
    bookings = Booking.objects.filter(account=request.user)
    return render(request, 'user_bookings.html', {'bookings': bookings})

@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, booking_id=booking_id)

    if booking.account != request.user:
        messages.error(request, "You do not have permission to cancel this booking.")
        return redirect('user_bookings')
    
    booking.set_status('PendingCancellation')
    booking.save()
    messages.success(request, "Your booking cancellation request has been submitted and is pending approval.")

    return redirect('user_bookings')
def is_admin(user):
    return user.is_superuser
@login_required
@user_passes_test(is_admin)
def pending_cancellations(request):
    bookings = Booking.objects.filter(status="PendingCancellation")
    return render(request, 'pending_cancellations.html', {'bookings': bookings})

@login_required
@user_passes_test(is_admin)
def approve_cancellation(request, booking_id):
    booking = get_object_or_404(Booking, booking_id=booking_id)
    booking.set_status("Canceled")  
    booking.save()
    messages.success(request, "Cancellation approved successfully.")
    return redirect('pending_cancellations')

@login_required
@user_passes_test(is_admin)
def reject_cancellation(request, booking_id):
    booking = get_object_or_404(Booking, booking_id=booking_id)
    booking.set_status("DeniedCancellation")  
    booking.save()
    messages.success(request, "Cancellation rejected.")
    return redirect('pending_cancellations')

