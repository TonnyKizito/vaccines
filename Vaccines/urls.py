
from django.contrib import admin
from django.urls import path, include
from Vaccines_control import views
from django.contrib.auth.views import LoginView,LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home_view,name=''),

    path('afterlogin', views.afterlogin_view,name='afterlogin'),
    path('logout/', LogoutView.as_view(template_name='vaccine/index.html'),name='logout'),

    path('adminclick', views.adminclick_view),
    path('districtadminclick', views.district_adminclick_view),

    path('storeclick', views.store_view),
    path('aboutus', views.aboutus_view),
    path('contactus', views.contactus_view),
    path('vaccinatorsignup', views.vaccinator_signup_view,name='vaccinatorsignup'),
     path('districtsignup', views.district_signup_view,name='districtsignup'),

    path('vaccinatorlogin', LoginView.as_view(template_name='vaccine/vaccinatorlogin.html')),
    path('districtlogin', LoginView.as_view(template_name='vaccine/districtlogin.html')),

    path('adminsignup', views.admin_signup_view),
    # path('district_adminsignup', views.district_admin_signup_view),


    path('adminlogin', LoginView.as_view(template_name='vaccine/adminlogin.html')),

    path('district_adminlogin', LoginView.as_view(template_name='vaccine/district_adminlogin.html')),


    path('admin-dashboard', views.admin_dashboard_view,name='admin-dashboard'),

    path('district-admin-dashboard', views.district_admin_dashboard_view,name='district-admin-dashboard'),


    path('admin-vaccinator', views.admin_vaccinator_view,name='admin-vaccinator'),
    path('district-admin-vaccinator', views.district_admin_vaccinator_view,name='district-admin-vaccinator'),

    path('admin-national-district', views.admin_national_district_view,name='admin-national-district'),




    path('admin-approve-vaccinator', views.admin_approve_doctor_view,name='admin-approve-vaccinator'),
     path('district-admin-approve-vaccinator', views.district_admin_approve_doctor_view,name='district-admin-approve-vaccinator'),




    path('admin-approve-district-admin', views.admin_approve_district_view,name='admin-approve-district-admin'),




    # path('admin-approve-district_admin', views.admin_approve_district_view,name='admin-approve-district_admin'),



    path('approve-doctor/<int:pk>', views.approve_doctor_view,name='approve-doctor'),

     path('approve-viccinator_by_district/<int:pk>', views.approve_vaccinator_by_district_view,name='approve-viccinator_by_district'),










    path('approve-district-admin/<int:pk>', views.approve_district_admin_view,name='approve-district-admin'),


     path('approve-district/<int:pk>', views.approve_district_view,name='approve-district'),




    path('reject-doctor/<int:pk>', views.reject_doctor_view,name='reject-doctor'),

    path('reject-vaccinator-by-district/<int:pk>', views.reject_vaccinator_by_district_view,name='reject-vaccinator-by-district'),



    path('reject-district-admin/<int:pk>', views.reject_district_admin_view,name='reject-district-admin'),



    path('reject-district/<int:pk>', views.reject_district_view,name='reject-district'),


    path('admin-view-vaccinator', views.admin_view_doctor_view,name='admin-view-vaccinator'),

    path('district-admin-view-vaccinator', views.district_admin_view_vaccinator_view,name='district-admin-view-vaccinator'),



    path('admin-view-district', views.admin_view_district_view,name='admin-view-district'),


    path('update-doctor/<int:pk>', views.update_doctor_view,name='update-doctor'),


     path('update-vaccinator-by-district/<int:pk>', views.update_vaccinator_by_district_view,name='update-vaccinator-by-district'),





    path('update-district/<int:pk>', views.update_district_view,name='update-district'),


    path('delete-doctor-from-hospital/<int:pk>', views.delete_doctor_from_hospital_view,name='delete-doctor-from-hospital'),
   
    path('delete-vaccinator-by-district/<int:pk>', views.delete_vaccinator_by_district_view,name='delete-vaccinator-by-district'),
   
   
   
    path('admin-add-vaccinator', views.admin_add_doctor_view,name='admin-add-vaccinator'),


    path('district-admin-add-vaccinator', views.district_admin_add_vaccinator_view,name='district-admin-add-vaccinator'),




    path('admin-add-district-admin', views.admin_add_district_admin_view,name='admin-add-district-admin'),




]


urlpatterns +=[
   path('pharmacylogin', LoginView.as_view(template_name='vaccine/vaccinatorlogin.html')),

   path('districtlogin', LoginView.as_view(template_name='vaccine/districtlogin.html')),


   path('vaccinator-dashboard', views.vaccinator_dashboard_view,name='vaccinator-dashboard'),
#    path('district-dashboard', views. district_dashboard_view,name='district-dashboard'),
   
   path('admin-pharmacy-appointment', views.admin_pharmacy_appointment_view,name='admin-pharmacy-appointment'),
]





#=======================PHARMACY================================================
urlpatterns += [
    path('home1', views.home, name='home1'),
    path('list_item/',views.list_item_view, name='list_item'),

    path('list_vaccine/',views.list_vaccine_view, name='list_vaccine'),
    
    path('add_items/', views.add_items, name='add_items'),

    
    
    
    path('add_vaccines/', views.add_vaccines, name='add_vaccines'),

     path('add_district_vaccines/', views.add_district_vaccines, name='add_district_vaccines'),





    path('facility_vaccine/',views.facility_vaccine_view, name='facility_vaccine'),

    path('district_vaccine/', views.district_vaccine_view, name='district_vaccine'),






    # path('add_items_debtor/', views.add_items_debtor, name='add_items_debtor'),

    
    path('update_items/<str:pk>/', views.update_items, name="update_items"),
    path('delete_items/<str:pk>/', views.delete_items, name="delete_items"),
    path('stock_detail/<str:pk>/', views.stock_detail, name="stock_detail"),
    path('issue_items/<str:pk>/', views.issue_items, name="issue_items"),
    path('reorder_level/<str:pk>/', views.reorder_level, name="reorder_level"),
    path('receive_items/<str:pk>/', views.receive_items, name="receive_items"),
    path('list_history/', views.list_history, name='list_history'),

    # path('list_history1/', views.list_history1, name='list_history1'),


    path('update_vaccine/<str:pk>/', views.update_vaccines, name="update_vaccine"),
    
    ]

