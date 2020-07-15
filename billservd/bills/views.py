from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, HttpResponseNotFound
from django.core import serializers
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.forms.models import modelformset_factory
from django.forms.formsets import formset_factory

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


def show_bill(request, bill_id):
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
        'title': f'Rechnung Nr. {bill.number}'
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
    PartFormset = modelformset_factory(Part, PartForm, extra=1)
    template = loader.get_template('new_bill.html')
    bform = BillForm(prefix="b")
    cform = CustomerForm(prefix="c")
    pform = PartFormset(prefix="p", queryset=Part.objects.none())
    print(pform.as_p())
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
    print("START SUBMITTING ...")
    PartFormset = modelformset_factory(Part, PartForm, extra=0)
    template = loader.get_template('bill.html')
    print(request.POST.get('b-number'))
    #b_inst = Bill.objects.get(number=request.POST.get('b-number'))
    #print(b_inst)
    if request.method == "POST":
        print("WE HAVE A POST")
        b = BillForm(request.POST, prefix="b")#, instance=b_inst)
        print(b)
        c = CustomerForm(request.POST, prefix="c")
        p = PartFormset(request.POST, prefix="p")
        if b.is_valid():
            print("VALID!")
            if c.is_valid():
                print("VALID!")
                if p.is_valid():
                    print("VALID!")
                    customer = c.save(commit=False)
                    customer.save()
                    parts = p.save(commit=False)
                    bill = b.save(commit=False)
                    bill.save()
                    for part in parts:
                        part.save()
                        bill.parts.add(part)
                    bill.customer_id = customer.id
                    bill.save()
                    print(bill.id)
                    print(bill.parts)
        return show_bill(request, bill.id)
                    #bill = b.save()
    pass


def edit_bill(request, bill_id):
    PartFormset = modelformset_factory(Part, PartForm, extra=1)
    #s erialize the Model to string and from string to json .... 
    # this is not so nice .... :(
    b = Bill.objects.get(id=bill_id)
    c = b.customer
    if b.parts:
        q = b.parts.all()
        pform = PartFormset(prefix="p", queryset=q)
    else:
        pform = PartFormset(prefix="p", queryset=Part.objects.none())
        print(pform.as_p())

    bform = BillForm(prefix="b", instance=b, auto_id=b.id)
    cform = CustomerForm(prefix="c", instance=c, auto_id=c.id)
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