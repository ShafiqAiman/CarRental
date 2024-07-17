from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .models import Car, Reservation
from .forms import ReservationForm, CarForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import JsonResponse
from django.db.models import Sum

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('homepage')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('homepage')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')
    
@login_required
def homepage(request):
    if not request.user.is_superuser:
        reservations = Reservation.objects.filter(user=request.user)
        return render(request, 'homepage.html', {'reservations': reservations})
    return render(request, 'homepage.html')    

def manage_cars(request):
    cars = Car.objects.all()
    return render(request, 'manage_cars.html', {'cars': cars})

def view_reservations(request):
    reservations = Reservation.objects.all()
    total_price_sum = Reservation.objects.aggregate(Sum('total_price'))['total_price__sum'] or 0.0
    
    context = {
        'reservations': reservations,
        'total_price_sum': total_price_sum,
    }
    
    return render(request, 'view_reservations.html', context)


def add_car(request):
    if request.method == 'POST':
        brand = request.POST['brand']
        model_name = request.POST['model_name']
        year = request.POST['year']
        mileage = request.POST['mileage']
        condition = request.POST['condition']
        price_per_hour = request.POST['price_per_hour']
        available = request.POST.get('available', False) == 'true'
        Car.objects.create(brand=brand, model=model_name, year=year, mileage=mileage,
                           condition=condition, price_per_hour=price_per_hour, available=available)
        return redirect('manage_cars')
    return render(request, 'add_car.html')

@login_required
def add_reservation(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user = request.user
            reservation.save()
            return redirect('homepage')  # Replace with appropriate redirect
    else:
        form = ReservationForm()
    
    return render(request, 'add_reservation.html', {'form': form})

def get_car_price(request):
    car_id = request.GET.get('car_id')
    
    try:
        car = Car.objects.get(id=car_id)
        price_per_hour = car.price_per_hour
        return JsonResponse({'price_per_hour': price_per_hour})
    except Car.DoesNotExist:
        return JsonResponse({'error': 'Car not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
def edit_car(request, car_id):
    car = get_object_or_404(Car, pk=car_id)
    if request.method == 'POST':
        form = CarForm(request.POST, instance=car)
        if form.is_valid():
            form.save()
            return redirect('manage_cars')  # Redirect to manage cars page after edit
    else:
        form = CarForm(instance=car)
    
    return render(request, 'edit_car.html', {'form': form, 'car': car})

def delete_car(request, car_id):
    car = get_object_or_404(Car, pk=car_id)
    if request.method == 'POST':
        car.delete()
        return redirect('manage_cars')  # Redirect to manage cars page after delete
    
    return render(request, 'delete_car.html', {'car': car})

# def view_feedbacks(request):
#     feedbacks = Feedback.objects.all()
#     return render(request, 'view_feedbacks.html', {'feedbacks': feedbacks})


