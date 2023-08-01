from django.urls import path
from . import views

urlpatterns = [
    path('daily_scrap_table/', views.daily_scrap_table, name='daily_scrap_table'),
    path('add_daily_scrap_entry/', views.add_daily_scrap_entry, name='add_daily_scrap_entry'),
    path('remove_scrap_entry_detail/<int:detail_id>/', views.remove_scrap_entry_detail, name='remove_scrap_entry_detail'),
    path('add_scrap_item_to_daily_scrap_entry/<int:entry_id>/', views.add_scrap_item_to_daily_scrap_entry, name='add_scrap_item_to_daily_scrap_entry'),

    path('generate-pdf-report/', views.generate_pdf_report, name='generate_pdf_report'),



    path('login/', views.login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('signup/', views.signup, name='signup'),
]
