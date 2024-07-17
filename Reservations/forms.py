# rental/forms.py

from django import forms
from .models import Reservation

class ReservationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter cars where available=True
        self.fields['car'].queryset = Car.objects.filter(available=True)
    class Meta:
        model = Reservation
        fields = ['car', 'start_date', 'end_date','period', 'total_price']
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

# forms.py

from django import forms
from .models import Car

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['brand', 'model', 'year', 'mileage', 'condition', 'price_per_hour', 'available']
