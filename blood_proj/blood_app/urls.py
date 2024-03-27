from django.urls import path
from . import views 
from .views import view_donor,view_patient
urlpatterns = [

    path('', views.home, name='home'),
    ############ donor section #################
    path('index', views.index, name='index'),
    path('donor_register', views.donor_register, name='donor_register'),
    path('donor_login', views.donor_login, name='donor_login'),
    
    path('add_donor', views.add_donor, name='add_donor'),
    path('view_donor/<int:pk>/', views.view_donor, name='view_donor'),
    path('update_donor/<int:pk>/', views.update_donor, name='update_donor'),
    path('donate/<int:pk>/', views.donate, name='donate'),

    path('view_donate/<int:pk>/', views.view_donate, name='view_donate'),
    path('update_donate/<int:pk>/', views.update_donate, name='update_donate'),
    path('delete_donate/<int:pk>/', views.delete_donate, name='delete_donate'),
    path('SignOut', views.SignOut, name='SignOut'),

    path('patient_request', views.patient_request, name='patient_request'),

    path('approve_request/<int:request_id>/', views.approve_request, name='approve_request'),

   ######### patient section #############
    path('patient_home', views.patient_home, name='patient_home'),
    path('patient_register', views.patient_register, name='patient_register'),
    path('patient_login', views.patient_login, name='patient_login'),

    path('add_patient', views.add_patient, name='add_patient'),
    path('view_patient/<int:pk>/', views.view_patient, name='view_patient'),
    path('update_patient/<int:pk>/', views.update_patient, name='update_patient'),

    path('view_blood', views.view_blood, name='view_blood'),

    path('make_request/<int:pk>/', views.make_request, name='make_request'),

    path('request_history', views.request_history, name='request_history'),
    path('patient_SignOut', views.patient_SignOut, name='patient_SignOut'),

    path('search', views.search, name='search'),

    


]

