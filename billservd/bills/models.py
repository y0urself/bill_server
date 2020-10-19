import datetime
import django.forms as forms
from django.utils import timezone
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput
from django.db.models import Model, CharField, IntegerField, FloatField, ForeignKey, ManyToManyField, CASCADE, DateField


class AuthForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={'class':'validate','placeholder': 'Benutzername'}))
    password = forms.CharField(widget=PasswordInput(attrs={'placeholder':'Passwort'}))


class Part(Model):
    vendor = CharField(max_length=100, blank=True)
    product_name = CharField(max_length=100, blank=True)
    product_type = CharField(max_length=100, blank=True)
    desc = CharField(max_length=100, blank=True)
    date = DateField(blank=True, null=True)
    amount = IntegerField(default=1)
    nprice = FloatField(default=0)
    nsum = FloatField(blank=True, default=0)

    def __str__(self):
        return f'{self.vendor}, {self.product_name}, {self.desc}'

    def calc_nsum(self):
        return self.nprice * self.amount


GENDERS = [
    ('male', 'männlich'),
    ('female', 'weiblich'),
    ('none', 'keins')
]

STATUSES = [
    ('open', 'Offen'),
    ('delivered', 'Verschickt'),
    ('partly paid', 'Teilweise bezahlt'),
    ('paid', 'Bezahlt')
]


class Customer(Model):
    class Meta:
        unique_together = [['name', 'surname', 'street', 'city'], ['company', 'street', 'city']]
    name = CharField(max_length=50, blank=True)
    surname = CharField(max_length=50, blank=True)
    company = CharField(max_length=70, blank=True)
    street = CharField(max_length=80)
    city = CharField(max_length=80)
    gender = CharField(max_length=10, choices=GENDERS, default='none')

    def __str__(self):
        cx = f'{self.name} {self.surname}, {self.street} {self.city}'
        if self.company:
            cx = f'{self.company}, {self.street} {self.city}'
        return f'{cx}'

class Bill(Model):
    date = DateField()
    taxes = FloatField(default=0.19)
    number = CharField(max_length=6, unique=True)
    parts = ManyToManyField(Part)
    customer = ForeignKey(Customer, on_delete=CASCADE, null=True)
    status = CharField(max_length=35, choices=STATUSES, default='open')
    part_sum = FloatField(default=0.0)
    open_sum = FloatField(default=0.0)
    paid_sum = FloatField(default=0.0)

    def bill_date(self):
        return f'Rechnungsdatum: {self.date}'

    def update_sum(self):
        sum_ = 0
        if self.parts:
            for part in self.parts.all():
                #print(part.nprice)
                sum_ += part.nprice
            sum_ = sum_ + sum_ * self.taxes
        return sum_

class PartForm(forms.ModelForm):
    class Meta:
        model = Part
        fields = [
            'vendor', 
            'product_name', 
            'product_type', 
            'desc', 
            'date', 
            'nprice', 
            'amount',
            'id'
        ]
        labels = {
            'vendor': 'Hersteller',
            'product_name': 'Produktbezeichnung',
            'product_type': 'Produkt-Typ',
            'desc': 'Produktbeschreibung',
            'date': 'Dienstleistungsdatum',
            'amount': 'Menge',
            'nprice': 'Netto-Preis'
        }
        widgets = {
            'vendor': forms.TextInput(attrs={'class': 'form-control part_input', 'placeholder': 'Hersteller'}),
            'product_name': forms.TextInput(attrs={'class': 'form-control part_input', 'placeholder': 'Produktbezeichnung'}),
            'product_type': forms.TextInput(attrs={'class': 'form-control part_input', 'placeholder': 'Produkt-Typ'}),
            'desc': forms.TextInput(attrs={'class': 'form-control part_input', 'placeholder': 'Produktbeschreibung'}),
            'date': forms.TextInput(attrs={'class': 'form-control part_input date_input', 'placeholder': 'Datum'}),
            'amount': forms.TextInput(attrs={'class': 'form-control part_input ', 'placeholder': 'Menge'}),
            'nprice': forms.TextInput(attrs={'class': 'form-control part_input', 'placeholder': 'Netto-Preis'}),
        }

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'surname', 'company', 'street', 'city', 'gender', 'id']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'surname': forms.TextInput(attrs={'class': 'form-control'}),
            'company': forms.TextInput(attrs={'class': 'form-control'}),
            'street': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            #'gender': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': 'Vorname',
            'surname': 'Nachname',
            'company': 'Firma',
            'street': 'Straße',
            'city': 'Wohnort',
            'gender': 'Geschlecht'
        }

class BillForm(forms.ModelForm):
    class Meta:
        model = Bill
        fields = ['date', 'taxes', 'number', 'id']
        widgets = {
            'date': forms.TextInput(attrs={'class': 'form-control'}),
            'taxes': forms.TextInput(attrs={'class': 'form-control'}),
            'number': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'date': 'Rechnungsdatum',
            'taxes': 'Steuersatz',
            'number': 'Rechnungsnummer'
        }

class CronForm(forms.Form):
    customer = forms.ModelChoiceField(queryset=Customer.objects.all())


PART_PAYMENTS = [
    (0.25, '1/4'),
    (0.33333, '1/3'),
    (0.5, '1/2'),
    (0.66666, '2/3'),
    (0.75, '3/4'),
]

class PartPaymentForm(forms.Form):
    part_opts = forms.CharField(widget=forms.Select(choices=PART_PAYMENTS))