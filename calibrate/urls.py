from django.urls import path
from . import views

app_name = 'calibrate'

urlpatterns = [
  path('', views.CalibrationList.as_view(), name='calibration_list'),
  path('new', views.CalibrationCreate.as_view(), name='calibration_new'),
  path('edit/<int:pk>', views.CalibrationUpdate.as_view(), name='calibration_edit'),
  path('delete/<int:pk>', views.CalibrationDelete.as_view(), name='calibration_delete'),
  path('staffs/', views.staff_list, name='staff_list'),
  path('staffs/<int:id>/details/', views.staff_details, name='staff_details'),
  path('staffs/<int:id>/edit/', views.staff_edit, name='staff_edit'),
  path('staffs/add/', views.staff_add, name='staff_add'),
  path('staffs/addsuper', views.superStaff_add, name='superStaff_add'),
  path('staffs/addadmin', views.adminstaff_add, name= 'adminstaff_add'),
  path('staffs/<int:id>/delete/', views.staff_delete, name='staff_delete'),
]