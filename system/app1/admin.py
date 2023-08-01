from django.contrib import admin
from .models import ScrapType, ScrapItem, Customer, DailyScrapEntry, ScrapEntryDetail, Transaction, TransactionDetail, UserProfile

# Register your models here
admin.site.register(ScrapType)

@admin.register(ScrapItem)
class ScrapItemAdmin(admin.ModelAdmin):
    list_display = ['RFID', 'scrap_type', 'weight']

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'contact_number', 'address']

@admin.register(DailyScrapEntry)
class DailyScrapEntryAdmin(admin.ModelAdmin):
    list_display = ['date', 'customer', 'staff_responsible']

@admin.register(ScrapEntryDetail)
class ScrapEntryDetailAdmin(admin.ModelAdmin):
    list_display = ['daily_scrap_entry', 'scrap_item', 'quantity']

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['date', 'customer', 'staff_responsible']

@admin.register(TransactionDetail)
class TransactionDetailAdmin(admin.ModelAdmin):
    list_display = ['transaction', 'scrap_item', 'quantity']

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'user_type']

