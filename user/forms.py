from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from event.models import Event


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    address = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'address',
            'email',
            'password1',
            'password2',
        ]


class TicketPurchaseForm(forms.ModelForm):
    event = forms.ModelChoiceField(queryset=Event.objects.all())
    quantity = forms.IntegerField(min_value=1, initial=1)
