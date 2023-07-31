from django.contrib import admin
from .models import *

admin.site.register(ScrapType)
admin.site.register(ScrapItem)
admin.site.register(DailyScrapEntry)
admin.site.register(ScrapEntryDetail)
admin.site.register(Transaction)
admin.site.register(TransactionDetail)
admin.site.register(UserProfile)