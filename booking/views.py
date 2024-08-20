from django.shortcuts import render, HttpResponse, HttpResponseRedirect, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from .forms import *
from .models import *
from django.shortcuts import render, get_object_or_404
from .models import Flight, Airport

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


def index(request):
    return render(request, 'homepage.html')


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
    
    # Bộ lọc theo ngày khởi hành
    departure_date = request.GET.get('departure_date')
    if departure_date:
        flights = flights.filter(departure_time__date=departure_date)

    # Bộ lọc theo địa điểm khởi hành
    departure_location = request.GET.get('departure_location')
    if departure_location:
        flights = flights.filter(departure_airport__city=departure_location)

    # Lấy danh sách các thành phố từ model Airport
    airports = Airport.objects.values_list('city', flat=True).distinct()

    context = {
        'flights': flights,
        'airports': airports,
    }
    return render(request, 'flight_list.html', context)
