# views.py
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from .models import MenuItem, CateringBooking, Category
from .forms import ContactForm
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils.html import escape
from django.utils import timezone
from calendar import HTMLCalendar
from django.utils.timezone import now
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from decimal import Decimal

def index(request):
    return render(request, 'catering/index.html')

def calendar_view(request):
    bookings = CateringBooking.objects.all()
    calendar = HTMLCalendar().formatmonth(now().year, now().month)
    return render(request, 'admin/calendar.html', {'calendar': calendar, 'bookings': bookings})

def generate_bill(request, booking_id):
    booking = get_object_or_404(CateringBooking, id=booking_id)
    subtotal = calculate_total_amount(booking)
    subtotal, tax_amount, total_amount = calculate_tax_and_total(subtotal)
    
    context = {
        'booking': booking,
        'subtotal': subtotal,
        'tax_amount': tax_amount,
        'total_amount': total_amount,
    }
    html = render_to_string('catering/bill.html', context)
    
    # Return the HTML as a response (or use it to generate a PDF, etc.)
    return HttpResponse(html)

def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_superuser:
            login(request, user)
            return redirect('admin_dashboard')
        else:
            messages.error(request, "Invalid credentials or not an admin.")
    return render(request, 'catering/admin_login.html')

@login_required
def admin_dashboard(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect('admin_login')

    return render(request, 'catering/admin_dashboard.html')

def calculate_total_amount(booking):
    total_amount = Decimal('0.00')  # Initialize with Decimal
    
    for item in booking.menu_items.all():  # Get all menu items for the booking
        price = Decimal(item.price)  # Ensure price is treated as Decimal
        quantity = 1  # Assuming each menu item is counted once per booking
        total_amount += price * Decimal(quantity)  # Perform calculation with Decimal

    return total_amount

def menu(request):
    query = request.GET.get('search', '')
    category_id = request.GET.get('category')
    items = MenuItem.objects.all()

    if query:
        items = items.filter(name__icontains=query)
    if category_id:
        items = items.filter(category_id=category_id)

    categories = Category.objects.all()
    return render(request, 'catering/menu.html', {'items': items, 'categories': categories})

def book_catering(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        event_date = request.POST.get('event_date')
        special_requests = request.POST.get('special_requests')

        # Get quantities
        quantities = {key.split('_')[1]: int(value) for key, value in request.POST.items() if key.startswith('quantities_')}

        # Check availability
        bookings_on_date = CateringBooking.objects.filter(event_date=event_date)
        if bookings_on_date.count() >= 2:
            messages.error(request, "Booking for this date is not available.")
            return redirect('book_catering')

        # Create booking
        booking = CateringBooking(
            customer_name=name,
            customer_email=email,
            event_date=event_date,
            special_requests=special_requests
        )
        booking.save()

        # Add items with quantities
        for item_id, quantity in quantities.items():
            menu_item = MenuItem.objects.get(id=item_id)
            for _ in range(quantity):
                booking.menu_items.add(menu_item)

        return redirect('index')
    else:
        items = MenuItem.objects.all()
        return render(request, 'catering/book.html', {'items': items})

def add_menu_item(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        category_id = request.POST.get('category')
        category = Category.objects.get(id=category_id)

        MenuItem.objects.create(name=name, description=description, price=price, category=category)
        return redirect('menu')

    categories = Category.objects.all()
    return render(request, 'catering/add_menu_item.html', {'categories': categories})

def contact_us(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Process the form data (e.g., send email)
            messages.success(request, "Your message has been sent!")
            return redirect('contact_us')
    else:
        form = ContactForm()
    return render(request, 'catering/contact_us.html', {'form': form})

def order_history(request):
    # Fetch all catering bookings (or modify as needed)
    bookings = CateringBooking.objects.all()
    return render(request, 'catering/order_history.html', {'bookings': bookings})


def calendar_view(request):
    # Retrieve all bookings
    bookings = CateringBooking.objects.all()
    return render(request, 'catering/calendar.html', {'bookings': bookings})

def calculate_tax_and_total(subtotal, tax_rate=0.18):
    tax_amount = subtotal * Decimal(tax_rate)
    total_amount = subtotal + tax_amount
    return subtotal, tax_amount, total_amount
