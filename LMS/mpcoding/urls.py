from django.urls import path
from . import views

app_name = 'mpcoding'

urlpatterns = [
    path('editor/', views.code_editor, name='editor'),
    path('create-room/', views.create_room, name='create_room'),
    path('join-room/<uuid:room_id>/', views.join_room, name='join_room'),
    path('wait-room/<uuid:room_id>/', views.wait_room, name='wait_room'),
    path('battle-room/<uuid:room_id>/', views.battle_room, name='battle_room'),
    path('battle-result/<uuid:room_id>/', views.battle_result, name='battle_result'),
    path('submit-code/<uuid:room_id>/', views.submit_code, name='submit_code'),
    path('api/check-room/<uuid:room_id>/', views.check_room, name='check_room'),
    path('api/check-battle/<uuid:room_id>/', views.check_battle, name='check_battle'),
]
