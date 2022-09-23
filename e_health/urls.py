from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('pacientes/', views.pacientes, name='pacientes'),
    path('dados_paciente/<str:id>/', views.dados_paciente, name="dados_paciente"),
    path('grafico_peso/<str:id>/', views.grafico_peso, name="grafico_peso"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)