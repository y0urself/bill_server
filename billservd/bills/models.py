from django.db.models import Model, CharField, FloatField, ForeignKey, ManyToManyField, CASCADE, DateField
import django.forms as forms
import datetime

from django.utils import timezone
# Create your models here.


class Part(Model):
    vendor = CharField(max_length=50, blank=True)
    product_name = CharField(max_length=50, blank=True)
    product_type = CharField(max_length=100, blank=True)
    desc = CharField(max_length=50, default='')
    date = DateField()
    nprice = FloatField()

    def __str__(self):
        return f'{self.vendor}, {self.product_name}, {self.desc}'

GENDERS = [
    ('männlich', 'male'),
    ('weiblich', 'female'),
    ('keins', 'none')
]

class Customer(Model):
    name = CharField(max_length=50, blank=True)
    surname = CharField(max_length=50, blank=True)
    company = CharField(max_length=70, blank=True)
    street = CharField(max_length=80)
    city = CharField(max_length=80)
    gender = CharField(max_length=10, choices=GENDERS, default='keins')

    def __str__(self):
        cx = self.name
        if self.company:
            cx = self.company
        return f'Kunde: {cx}'

class Bill(Model):
    date = DateField()
    taxes = FloatField(default=0.19)
    number = CharField(max_length=6, unique=True)
    parts = ManyToManyField(Part)
    customer = ForeignKey(Customer, on_delete=CASCADE, null=True)

    def bill_date(self):
        return f'Rechnungsdatum: {self.date}'



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
            'id'
        ]
        labels = {
            'vendor': 'Hersteller',
            'product_name': 'Produktbezeichnung',
            'product_type': 'Produkt-Typ',
            'desc': 'Produktbeschreibung',
            'date': 'Dienstleistungsdatum',
            'nprice': 'Netto-Preis'
        }
        widgets = {
            'vendor': forms.TextInput(attrs={'class': 'form-control part_input', 'placeholder': 'Hersteller'}),
            'product_name': forms.TextInput(attrs={'class': 'form-control part_input', 'placeholder': 'Produktbezeichnung'}),
            'product_type': forms.TextInput(attrs={'class': 'form-control part_input', 'placeholder': 'Produkt-Typ'}),
            'desc': forms.TextInput(attrs={'class': 'form-control part_input', 'placeholder': 'Produktbeschreibung'}),
            'date': forms.TextInput(attrs={'class': 'form-control part_input', 'placeholder': 'Datum'}),
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