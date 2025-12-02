from django.urls import path
from . import views

app_name = 'payments'
urlpatterns = [
    path('process/<int:order_id>/', views.payment_process, name='process'),
    path('webhook/', views.payment_webhook, name='webhook'),
]