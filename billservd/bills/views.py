from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, HttpResponseNotFound
from django.core import serializers
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.forms.models import modelformset_factory

import json

from .models import Customer, Bill, Part, CustomerForm, BillForm, PartForm


def bills(request):
    bills_list = Bill.objects.all()

    template = loader.get_template('bills.html')
    context = {
        'bills_list': bills_list,
        'title': 'Rechnungen'
    }
    return HttpResponse(template.render(request=request, context=context))


def bill(request, bill_id):
    bill = Bill.objects.get(id=bill_id)
    print(bill)
    c = bill.customer
    p = bill.parts.all()
    print(c)
    template = loader.get_template('bill.html')
    context = {
        'bill': bill,
        'customer' : c,
        'parts' : p,
        'title': f'Rechnung Nr. {bill.id_field}'
    }
    return HttpResponse(template.render(request=request, context=context))


def parts(request):
    parts_list = Part.objects.all()
    template = loader.get_template('parts.html')
    context = {
        'parts_list': parts_list,
        'title': 'Produkte'
    }
    return HttpResponse(template.render(request=request, context=context))


def part(request, part_id):
    part = Part.objects.get(id=part_id)
    template = loader.get_template('part.html')
    context = {
        'part': part,
        'title': f'Produkt {part.product_name}'
    }
    return HttpResponse(template.render(request=request, context=context))


def new_bill(request):
    PartFormset = modelformset_factory(Part, PartForm)
    template = loader.get_template('new_bill.html')
    bform = BillForm(prefix="b_")
    cform = CustomerForm(prefix="c_")
    pform = PartFormset(prefix="p_")
    context = {
        'bill': 'null',
        'title': f'Neue Rechnung erstellen',
        'pk': 'null',
        'bform': bform,
        'cform': cform,
        'pform': pform
    }
    return HttpResponse(template.render(request=request, context=context))

@csrf_exempt
def save_bill(request):
    PartFormset = modelformset_factory(Part, PartForm)
    template = loader.get_template('bill.html')
    if request.method == "POST":
        b = BillForm(request.POST, prefix="b_")
        c = CustomerForm(request.POST, prefix="c_")
        p = PartFormset(request.POST, prefix="p_")
        if b.is_valid() and c.is_valid() and p.is_valid():
            print("VALID!")
            b.save()
            c.save()
            p.save()

    pass


def edit_bill(request, bill_id):
    #s erialize the Model to string and from string to json .... 
    # this is not so nice .... :(
    b = Bill.objects.get(id=bill_id)
    c = b.customer
    print(c)
    q = b.parts.all()
    p = []
    for pb in q:
        p.append(pb)
    print(p)
    PartFormset = modelformset_factory(Part, PartForm, extra=0)
    bform = BillForm(prefix="b", instance=b)
    cform = CustomerForm(prefix="c", instance=c)
    pform = PartFormset(prefix="p", queryset=q)
    if b:
        template = loader.get_template('new_bill.html')
        context = {
            'title': f'Rechnung bearbeiten',
            'pk' : bill_id,
            'bform': bform,
            'cform': cform,
            'pform': pform
        }
        return HttpResponse(template.render(request=request, context=context))
    else:
        return HttpResponseNotFound('<h1>Page not found</h1>')


def del_bill(request, bill_id):
    Bill.objects.filter(id=bill_id).delete()
    return bills(request)