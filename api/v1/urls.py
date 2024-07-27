from django.urls import path
from .post import calcular_dados

urlpatterns = [
    path("calcular-dados/", calcular_dados, name="calcular_dados"),
]
