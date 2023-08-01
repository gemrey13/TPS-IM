from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import *

from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle



def generate_pdf_report(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="scrap_report.pdf"'

    # Create a SimpleDocTemplate for the PDF
    pdf = SimpleDocTemplate(response, pagesize=letter)

    # Retrieve data for daily dates and associated scrap items
    daily_scrap_entries = DailyScrapEntry.objects.all()

    # Create a list to store table data
    table_data = [
        ['Date', 'RFID', 'Type', 'Weight (kg)', 'Quantity'],  # Header row
    ]

    # Add the data to the table
    for entry in daily_scrap_entries:
        # Add the date to the table without background color
        table_data.append([str(entry.date), '', '', '', ''])

        # Fetch associated scrap items for the current daily entry
        scrap_entries = ScrapEntryDetail.objects.filter(daily_scrap_entry=entry)
        for scrap_entry in scrap_entries:
            # Add scrap item data to the table
            table_data.append(['', str(scrap_entry.scrap_item.RFID),
                               str(scrap_entry.scrap_item.scrap_type),
                               str(scrap_entry.scrap_item.weight),
                               str(scrap_entry.quantity)])

    # Define the style for the table
    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), 'gray'),  # Header row background color
        ('TEXTCOLOR', (0, 0), (-1, 0), 'white'),  # Header row text color
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Center-align all cells
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Header font
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Add padding to the header row
        ('BOX', (0, 0), (-1, -1), 1, 'black'),  # Add borders to all cells
        ('INNERGRID', (0, 0), (-1, -1), 0.25, 'black'),  # Add inner grid lines
    ])

    # Create the table with specified column widths
    col_widths = [80, 120, 120, 80, 80]  # Adjust the width of each column here
    table = Table(table_data, colWidths=col_widths)

    # Apply the table style
    table.setStyle(table_style)

    # Add the table to the PDF document
    elements = [table]
    pdf.build(elements)

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

        rfid_list = request.POST.getlist('scrap_item_rfid')
        weight_list = request.POST.getlist('scrap_item_weight')
        scrap_type_list = request.POST.getlist('scrap_item_type')
        quantity_list = request.POST.getlist('scrap_item_quantity')

        for rfid, weight, scrap_type_name, quantity in zip(rfid_list, weight_list, scrap_type_list, quantity_list):
            if rfid and weight and scrap_type_name and quantity:
                scrap_type, _ = ScrapType.objects.get_or_create(name=scrap_type_name)
                scrap_item, _ = ScrapItem.objects.get_or_create(
                    RFID=rfid,
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
        return redirect('daily_scrap_table')

    scrap_types = ScrapType.objects.all()
    return render(request, 'add_daily_scrap_entry.html', {'scrap_types': scrap_types})



@login_required(login_url='login')
def remove_scrap_entry_detail(request, detail_id):
    scrap_entry_detail = get_object_or_404(ScrapEntryDetail, id=detail_id)
    daily_scrap_entry = scrap_entry_detail.daily_scrap_entry
    scrap_entry_detail.delete()
    return redirect('daily_scrap_table')


from django.db.models import F

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



from django.contrib import messages

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


def add_transaction(request):
    if request.method == 'POST':
        date = request.POST.get('date')
        customer_id = request.POST.get('customer')
        staff_responsible_id = request.POST.get('staff_responsible')

        transaction = Transaction.objects.create(
            date=date,
            customer_id=customer_id,
            staff_responsible_id=staff_responsible_id
        )

        scrap_item_ids = request.POST.getlist('scrap_item')
        quantities = request.POST.getlist('quantity')

        for scrap_item_id, quantity in zip(scrap_item_ids, quantities):
            if scrap_item_id and quantity:
                scrap_item = ScrapItem.objects.get(id=scrap_item_id)
                quantity = int(quantity)

                TransactionDetail.objects.create(
                    transaction=transaction,
                    scrap_item=scrap_item,
                    quantity=quantity
                )

        return redirect('transaction_list')

    daily_scrap_entries = DailyScrapEntry.objects.all()
    scrap_items = ScrapItem.objects.all()
    customers = Customer.objects.all()
    staff = User.objects.filter(userprofile__user_type='staff')
    context = {
        'daily_scrap_entries': daily_scrap_entries,
        'scrap_items': scrap_items,
        'customers': customers,
        'staff': staff,
    }
    return render(request, 'add_transaction.html', context)


def transaction_list(request):
    transactions = Transaction.objects.all()
    return render(request, 'transaction_list.html', {'transactions': transactions})
