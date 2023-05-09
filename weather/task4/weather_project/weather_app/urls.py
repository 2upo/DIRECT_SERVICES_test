from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/weather/random/', views.random_forecast, name='random_forecast'),
    path('api/weather/<str:city>/', views.forecast, name='forecast'),
    path('api/healthcheck/', views.healthcheck, name='healthcheck'),
]