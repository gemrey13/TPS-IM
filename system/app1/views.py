from django.shortcuts import render, redirect
from .models import DailyScrapEntry, ScrapItem, ScrapEntryDetail

def daily_scrap_table(request):
    daily_scrap_entries = DailyScrapEntry.objects.all()
    return render(request, 'daily_scrap_table.html', {'daily_scrap_entries': daily_scrap_entries})

def add_daily_scrap_entry(request):
    if request.method == 'POST':
        date = request.POST.get('date')
        daily_scrap_entry = DailyScrapEntry.objects.create(date=date)

        scrap_items = ScrapItem.objects.all()
        for scrap_item in scrap_items:
            quantity = request.POST.get('quantity_{}'.format(scrap_item.id))
            if quantity and int(quantity) > 0:
                ScrapEntryDetail.objects.create(daily_scrap_entry=daily_scrap_entry, scrap_item=scrap_item, quantity=quantity)

        return redirect('daily_scrap_table')
    else:
        scrap_items = ScrapItem.objects.all()
        return render(request, 'add_daily_scrap_entry.html', {'scrap_items': scrap_items})

def remove_daily_scrap_entry(request, entry_id):
    entry = DailyScrapEntry.objects.get(pk=entry_id)
    entry.delete()
    return redirect('daily_scrap_table')
