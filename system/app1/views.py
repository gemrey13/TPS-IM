from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import F
from django.contrib import messages
from django.utils.timezone import localtime
from .models import *

from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

from django.http import HttpResponse
from django.template.loader import render_to_string
from reportlab.pdfgen import canvas



def transaction_report(request, transaction_id):
    transaction = Transaction.objects.get(id=transaction_id)
    transaction_date = localtime(transaction.date)
    formatted_date = transaction_date.strftime('%B %d, %Y - %I:%M %p')

    pdf_content = render_to_string('pdf-report/transaction-pdf.html', {'transaction': transaction})

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="transaction_report_{transaction_id}.pdf"'

    p = canvas.Canvas(response)
    p.drawString(100, 790, "Transaction Report")
    p.drawString(100, 750, f"Date: {formatted_date}")
    p.drawString(100, 730, f"Customer Name: {transaction.customer}")
    p.drawString(100, 710, f"Contact Number: {transaction.customer.contact_number}")
    p.drawString(100, 690, f"Customer Address: {transaction.customer.address}")
    p.drawString(100, 670, f"Staff: {transaction.staff_responsible}")
    p.drawString(100, 650, "Scraps:")
    
    y = 630
    for scrap_item in transaction.scraps.all():
        p.drawString(120, y, f"{scrap_item.RFID} - {scrap_item.scrap_type.name} ({scrap_item.weight} kg)")
        y -= 20

    p.showPage()
    p.save()

    return response


@login_required(login_url='login')
def daily_scrap_table(request):
    daily_scrap_entries = DailyScrapEntry.objects.all()
    return render(request, 'daily_scrap_table.html', {'daily_scrap_entries': daily_scrap_entries})

@login_required(login_url='login')
def add_daily_scrap_entry(request):
    if request.method == 'POST':
        date = request.POST.get('date')
        scraps_added = []

        try:
            daily_scrap_entry = DailyScrapEntry.objects.get(date=date)
        except DailyScrapEntry.DoesNotExist:
            daily_scrap_entry = DailyScrapEntry.objects.create(date=date)

        price_list = request.POST.getlist('price')
        weight_list = request.POST.getlist('scrap_item_weight')
        scrap_type_list = request.POST.getlist('scrap_item_type')
        quantity_list = request.POST.getlist('scrap_item_quantity')

        for price, weight, scrap_type_name, quantity in zip(price_list, weight_list, scrap_type_list, quantity_list):
            if price and weight and scrap_type_name and quantity:
                scrap_type, _ = ScrapType.objects.get_or_create(name=scrap_type_name)
                scrap_item, _ = ScrapItem.objects.get_or_create(
                    price=price,
                    defaults={
                        'weight': weight,
                        'scrap_type': scrap_type,
                    }
                )

                scrap_entry_detail = ScrapEntryDetail.objects.filter(
                    daily_scrap_entry=daily_scrap_entry,
                    scrap_item=scrap_item
                ).first()

                if scrap_entry_detail:
                    # If the ScrapEntryDetail already exists, update the quantity
                    scrap_entry_detail.quantity = F('quantity') + int(quantity)
                    scrap_entry_detail.save()
                else:
                    # If the ScrapEntryDetail does not exist, create a new one
                    ScrapEntryDetail.objects.create(
                        daily_scrap_entry=daily_scrap_entry,
                        scrap_item=scrap_item,
                        quantity=int(quantity)
                    )

                scraps_added.append(scrap_item)

        daily_scrap_entry.scraps.add(*scraps_added)

        previous_url = request.session.get('previous_url', reverse('daily_scrap_table'))
        print(previous_url)
        return redirect(previous_url)

    request.session['previous_url'] = request.META.get('HTTP_REFERER', reverse('daily_scrap_table'))
    scrap_types = ScrapType.objects.all()
    return render(request, 'add_daily_scrap_entry.html', {'scrap_types': scrap_types})



@login_required(login_url='login')
def remove_scrap_entry_detail(request, detail_id):
    scrap_entry_detail = get_object_or_404(ScrapEntryDetail, id=detail_id)
    daily_scrap_entry = scrap_entry_detail.daily_scrap_entry
    scrap_entry_detail.delete()
    return redirect('daily_scrap_table')



@login_required(login_url='login')
def add_scrap_item_to_daily_scrap_entry(request, entry_id):
    daily_scrap_entry = get_object_or_404(DailyScrapEntry, id=entry_id)

    associated_scrap_items = ScrapItem.objects.filter(
        scrapentrydetail__daily_scrap_entry=daily_scrap_entry
    )

    if request.method == 'POST':
        scrap_item_id = request.POST['scrap_item']
        quantity = int(request.POST['quantity'])

        try:
            scrap_item = ScrapItem.objects.get(id=scrap_item_id)

            if quantity > 0:
                # Check if ScrapEntryDetail already exists for the given daily_scrap_entry and scrap_item
                scrap_entry_detail = ScrapEntryDetail.objects.filter(
                    daily_scrap_entry=daily_scrap_entry,
                    scrap_item=scrap_item
                ).first()

                if scrap_entry_detail:
                    # If the ScrapEntryDetail already exists, update the quantity
                    scrap_entry_detail.quantity = F('quantity') + quantity
                    scrap_entry_detail.save()
                else:
                    # If the ScrapEntryDetail does not exist, create a new one
                    ScrapEntryDetail.objects.create(
                        daily_scrap_entry=daily_scrap_entry,
                        scrap_item=scrap_item,
                        quantity=quantity
                    )

                return redirect('daily_scrap_table')
            else:
                pass
        except (ScrapItem.DoesNotExist, ValueError):
            pass

    context = {
        'daily_scrap_entry': daily_scrap_entry,
        'associated_scrap_items': associated_scrap_items,
    }
    return render(request, 'add_scrap_item.html', context)




def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('pass')
        user = authenticate(request, username=username, password=password)
        if user:
            auth_login(request, user)
            return redirect('daily_scrap_table')
        else:
            messages.error(request, 'Invalid login credentials.')  
            return render(request, 'login.html', {'error': 'Invalid login credentials.'})
    else:
        messages.get_messages(request).used = True
        return render(request, 'login.html', {'error': 'Invalid credentials'})

def user_logout(request):
    logout(request)
    return redirect('login') 



def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'signup.html')

        try:
            user = User.objects.create_user(username=username, password=password)
            messages.success(request, 'Account created successfully. You can now login.')
            return redirect('login')
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
            return render(request, 'signup.html')

    messages.get_messages(request).used = True
    return render(request, 'signup.html')


@login_required(login_url='login')
def create_transaction(request):
    if request.method == 'POST':
        customer_name = request.POST.get('customer')
        contact_number = request.POST.get('contact_number')
        address = request.POST.get('address')

        customer, _ = Customer.objects.get_or_create(name=customer_name, defaults={'contact_number': contact_number, 'address': address})

        selected_scraps = request.POST.getlist('scraps')
        print(selected_scraps)

        transaction = Transaction.objects.create(date=timezone.now(), customer=customer, staff_responsible=request.user)

        for scrap_id in selected_scraps:
            print(scrap_id)
            scrap_item = ScrapItem.objects.get(pk=scrap_id)
            transaction.scraps.add(scrap_item)

        return redirect('transaction_list')
    else:
        scraps = ScrapItem.objects.all()
        return render(request, 'create_transaction.html', {'scraps': scraps})

@login_required(login_url='login')
def transaction_list(request):
    transactions = Transaction.objects.all().order_by('-date')
    return render(request, 'transaction_list.html', {'transactions': transactions})
