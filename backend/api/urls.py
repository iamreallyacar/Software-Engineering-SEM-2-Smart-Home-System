from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import auth_views, home_views, device_views, user_views, demo_views

router = DefaultRouter()
router.register(r'devices', device_views.DeviceViewSet)
router.register(r'rooms', home_views.RoomViewSet)
router.register(r'smarthomes', home_views.SmartHomeViewSet)
router.register(r'supported-devices', device_views.SupportedDeviceViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # Authentication endpoints
    path('auth/login/', auth_views.login_view, name='login'),
    path('auth/logout/', auth_views.logout_view, name='logout'),
    path('auth/register/', auth_views.register_view, name='register'),
    path('auth/user/', user_views.user_view, name='user'),
    
    # Smart home management
    path('create-smarthome/', home_views.create_smarthome, name='create_smarthome'),
    path('join-smarthome/', home_views.join_smart_home, name='join_smarthome'),
    path('leave-smarthome/', home_views.leave_smarthome, name='leave_smarthome'),
    path('smarthome-members/', home_views.get_smarthome_members, name='smarthome_members'),
    path('unlock-room/', home_views.unlock_room, name='unlock_room'),
    
    # Device management  
    path('device-control/', device_views.DeviceControlView.as_view(), name='device_control'),
    path('add-device/', device_views.add_device_to_room, name='add_device'),
    
    # User management
    path('dashboard-summary/', user_views.dashboard_summary, name='dashboard_summary'),
    path('current-user/', user_views.current_user_info, name='current_user'),
      # Recovery codes
    path('recovery-codes/generate/', auth_views.generate_recovery_codes, name='generate_recovery_codes'),
    path('recovery-codes/', auth_views.list_recovery_codes, name='list_recovery_codes'),
    path('reset-password/', auth_views.reset_password_with_code, name='reset_password'),
      # Demo and energy monitoring endpoints
    path('demo/energy-dashboard/', demo_views.real_time_energy_dashboard, name='energy_dashboard'),
    path('demo/run-scenario/', demo_views.run_demo_scenario, name='run_demo_scenario'),
    path('demo/scenarios/', demo_views.available_demo_scenarios, name='available_scenarios'),
    path('demo/device/<int:device_id>/energy/', demo_views.device_energy_details, name='device_energy_details'),
    path('demo/energy-trends/', demo_views.energy_trends_chart, name='energy_trends_chart'),
    path('demo/simulate-activity/', demo_views.simulate_activity, name='simulate_activity'),
]
