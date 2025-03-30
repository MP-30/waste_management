from django.urls import path
from . import views

urlpatterns = [
    # Dashboard URLs
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('waste-generators/dashboard/', views.waste_generator_dashboard, name='waste_generator_dashboard'),

    # User Management URLs
    path('users/dashboard/', views.user_dashboard, name='user_dashboard'),
    path('users/add/', views.user_add, name='user_add'),
    path('users/<int:pk>/edit/', views.user_edit, name='user_edit'),
    path('users/<int:pk>/delete/', views.user_delete, name='user_delete'),
    path('users/roles/add/', views.role_add, name='role_add'),
    path('users/roles/', views.role_list, name='role_list'),
    path('users/roles/<int:pk>/edit/', views.role_edit, name='role_edit'),
    path('users/roles/<int:pk>/delete/', views.role_delete, name='role_delete'),
    path('users/permissions/', views.manage_permissions, name='manage_permissions'),

    # Waste Generator URLs
    path('waste-generators/', views.waste_generator_list, name='waste_generator_list'),
    path('waste-generators/add/', views.waste_generator_add, name='waste_generator_add'),
    path('waste-generators/<int:pk>/edit/', views.waste_generator_edit, name='waste_generator_edit'),
    path('waste-generators/<int:pk>/delete/', views.waste_generator_delete, name='waste_generator_delete'),
    path('waste-generators/groups/', views.waste_generator_groups, name='waste_generator_groups'),
    path('waste-generators/reports/', views.waste_generator_reports, name='waste_generator_reports'),
    path('waste-generators/import/', views.waste_generator_import, name='waste_generator_import'),
    path('waste-generators/export/', views.waste_generator_export, name='waste_generator_export'),

    # Waste Collector URLs
    path('waste-collectors/', views.waste_collector_list, name='waste_collector_list'),
    path('waste-collectors/add/', views.waste_collector_add, name='waste_collector_add'),
    path('waste-collectors/<int:pk>/edit/', views.waste_collector_edit, name='waste_collector_edit'),
    path('waste-collectors/<int:pk>/delete/', views.waste_collector_delete, name='waste_collector_delete'),

    # Waste Type URLs
    path('waste-types/', views.waste_type_list, name='waste_type_list'),
    path('waste-types/add/', views.waste_type_add, name='waste_type_add'),
    path('waste-types/<int:pk>/edit/', views.waste_type_edit, name='waste_type_edit'),
    path('waste-types/<int:pk>/delete/', views.waste_type_delete, name='waste_type_delete'),

    # Organization Configuration
    path('organization/settings/', views.organization_settings, name='organization_settings'),
]