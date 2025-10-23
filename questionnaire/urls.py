from django.urls import path
from . import views

urlpatterns = [
    path('', views.poser_question, name='poser_question'),
    path('historique/', views.historique, name='historique'),  # ✅ nouvelle page
    path('telecharger-pdf/', views.telecharger_pdf, name='telecharger_pdf'),  # ✅ nouvelle route
]
