from django.urls import path
from . import views

urlpatterns = [
    path('daily_scrap_table/', views.daily_scrap_table, name='daily_scrap_table'),
    path('add_daily_scrap_entry/', views.add_daily_scrap_entry, name='add_daily_scrap_entry'),
    path('remove_daily_scrap_entry/<int:entry_id>/', views.remove_daily_scrap_entry, name='remove_daily_scrap_entry'),
    path('remove_scrap_entry_detail/<int:detail_id>/', views.remove_scrap_entry_detail, name='remove_scrap_entry_detail'),
]
