from django.urls import path,include
from . import views

urlpatterns = [
    path('register', views.register, name='register'),
    path('', views.login_user, name='login_user'),
    path('compute_billing', views.compute_billing, name='compute_billing'),
    # path('accounts/', include('django.contrib.auth.urls')),
    path('application', views.application, name='application'),
    path('generate_report', views.generate_report, name='generate_report'),
    
]