from django.urls import path
from . import views
from .views import flight_detail, flight_list, pending_cancellations, user_bookings, approve_cancellation, reject_cancellation
urlpatterns = [
    path('', views.index, name='index'),

    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('register', views.register_view, name='register'),

    path('flight', flight_list, name = 'flight'),
    path('flight/<int:flight_id>/', flight_detail, name='flight_detail'),

    path('book/', user_bookings, name='user_bookings'),
    path('cancelbooking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    
    path('pending-cancellations/', pending_cancellations, name='pending_cancellations'),
    path('approve-cancellation/<int:booking_id>/', approve_cancellation, name='approve_cancellation'),
    path('reject-cancellation/<int:booking_id>/', reject_cancellation, name='reject_cancellation'),
    
]
