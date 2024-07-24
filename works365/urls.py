from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('registrar_usuario/', views.register_usuario, name='register_usuario'),
    path('visualizar_servico_usuario/', views.view_user_service, name='view_user_service'),
    path('solicitar_servico_usuario/', views.request_user_service, name='request_user_service'),

    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('quem_somos/', views.quem_somos, name='quem_somos'),
    
    path('processar_oferta/<int:servico_id>/', views.processar_oferta, name='processar_oferta'),
    
    path('visualizar_servico_profissional/', views.view_profissional_service, name='view_profissional_service'),
    path('registrar_profissional/', views.register_profissional, name='register_profissional'),
    # path('enviar-whatsapp/<int:profissional_id>/', views.enviar_whatsapp, name='enviar_whatsapp'),
]