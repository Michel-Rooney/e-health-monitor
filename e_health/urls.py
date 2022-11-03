from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('pacientes/', views.pacientes, name='pacientes'),
    path('dados_paciente/<str:id>/', views.dados_paciente, name="dados_paciente"),
    path('grafico_peso/<str:id>/', views.grafico_peso, name="grafico_peso"),
    path('cadastro_info/', views.cadastro_info, name='cadastro_info'),
    path('torna_medico/', views.torna_medico, name='torna_medico'),
    path('cancelar_monitoriamento/<str:id>/', views.cancelar_monitoriamento, name='cancelar_monitoriamento'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
