from django.urls import path
from . import views

urlpatterns = [
    path('', views.set_pengguna, name='set_pengguna'),
    path('data_entry/', views.set_data_entry, name='set_data_entry'),
    path('content/', views.set_content, name='set_content'),

    #pengguna
    path('api/pengguna/<int:user_id>/', views.get_pengguna_detail_api, name='get_pengguna_detail_api'),
    path('pengguna/<id>/view', views.view_pengguna, name ='viewdata'),
    path('pengguna/<id>/update',views.update_pengguna, name = 'updatedata'),
    path('pengguna/<id>/delete',views.delete_pengguna, name = 'deletedata')
]
