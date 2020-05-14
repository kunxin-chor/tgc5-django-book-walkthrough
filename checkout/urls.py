from django.urls import path
from .views import checkout, checkout_success, checkout_cancelled, handle_payment_completed


urlpatterns = [
    path('', checkout),
    path('success', checkout_success),
    path('cancelled', checkout_cancelled),
    path('payment_completed', handle_payment_completed)
]