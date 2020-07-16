from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse, HttpResponseNotFound
from django.core import serializers
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.forms.models import modelformset_factory
from django.forms.formsets import formset_factory
from pathlib import Path
import subprocess
from django.conf import settings

from . import build_tex

import json

from .models import Customer, Bill, Part, CustomerForm, BillForm, PartForm, CronForm

###### BILL VIEWS ######

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
    template = loader.get_template('bill.html')
    output_dir = Path(settings.MEDIA_ROOT).absolute()
    print(Path(output_dir / "bla"))
    context = {
        'bill': bill,
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
    template = loader.get_template('new_bill.html')
    PartFormset = modelformset_factory(Part, PartForm, extra=1)
    bform = BillForm(request.POST or None, prefix="b")
    cform = CustomerForm(request.POST or None, prefix="c")
    pform = PartFormset(request.POST or None, prefix="p", queryset=Part.objects.none())

    some_form = CronForm(request.POST or None, prefix="some_")
    if some_form.is_valid() and request.POST:

        customer = some_form.cleaned_data
        print(customer)
        cform = CustomerForm(request.POST or None, instance=customer, prefix="c")
        print(customer)
    print(bform.errors)
    print(cform.errors)
    print(pform.errors)
    if bform.is_valid() and cform.is_valid() and pform.is_valid():
        print("OK THANKS!")
        bill = bform.save()
        c = cform.save()
        parts = pform.save()
        for part in parts:
            bill.parts.add(part)
        bill.customer = c
        bill.save()
        print("Redirecting ...")
        create_tex(bill=bill)
        return redirect('bill', bill_id=bill.id)
    context = {
        'title': f'Neue Rechnung erstellen',
        'bform': bform,
        'cform': cform,
        'pform': pform,
        'some_form': some_form
    }
    return HttpResponse(template.render(request=request, context=context))

def edit_bill(request, bill_id):
    bill = get_object_or_404(Bill, id=bill_id)
    if not bill:
        redirect('new_bill')

    PartFormset = modelformset_factory(Part, PartForm, extra=1)
    template = loader.get_template('new_bill.html')

    if bill.parts:
        pform = PartFormset(request.POST or None, prefix="p", queryset=bill.parts.all())
    else:
        pform = PartFormset(request.POST or None, prefix="p", queryset=Part.objects.none())

    bform = BillForm(request.POST or None, prefix="b", instance=bill)
    cform = CustomerForm(request.POST or None, prefix="c", instance=bill.customer)
    print(pform.is_valid())
    if bform.is_valid() and cform.is_valid() and pform.is_valid():
        print("OK THANKS!")
        bill = bform.save()
        cform.save()
        parts = pform.save()
        for part in parts:
            bill.parts.add(part)
        bill.save()

        create_tex(bill = bill)
        return redirect('bill', bill_id=bill_id)
    
    context = {
        'title': f'Rechnung bearbeiten',
        'bform': bform,
        'cform': cform,
        'pform': pform
    }
    return HttpResponse(template.render(request=request, context=context))

def del_bill(request, bill_id):
    Bill.objects.filter(id=bill_id).delete()
    return bills(request)

def create_tex(bill):
    output_dir = Path(settings.MEDIA_ROOT).absolute()
    output_dir.mkdir(parents=True, exist_ok=True)
    cust = bill.customer.surname
    if bill.customer.company:
        cust = bill.customer.company
    output_file = Path(output_dir / f'{cust}_{bill.number}.tex')

    texer = build_tex.DocumentTexer()
    print('created texer')

    texer.add_contact_info(
        name=bill.customer.name,
        surname=bill.customer.surname,
        street=bill.customer.street,
        city=bill.customer.city,
        gender=bill.customer.gender,
        company=bill.customer.company
    )

    json1 = json.loads(serializers.serialize('json', bill.parts.all()))
    parts = []
    for part in json1:
        parts.append(part['fields'])

    texer.add_components(
        parts=parts
    )
    texer.finish_adding(None, taxes=bill.taxes)


    texer.choose_heading(
        number=bill.number
    )

    texer.add_date_number(
        date=bill.date, 
        number=bill.number
    )
    #print(texer.template)

    with open(output_file, 'w') as fp2:
        print(output_file)
        fp2.write(texer.template)

        #print(os.system('env'))

def create_pdf(output_dir, output_file, output_pdf):
    cmd = ['xelatex', '-shell-escape', '-synctex=1', '-file-line-error', '-interaction=nonstopmode', f'-output-directory={output_dir}', output_file]
        #subprocess.run(cmd, shell=True, check=True)
        #print(cmd)
    try:
        print("Run script ...")
        subprocess.call(cmd)
    except Exception:
        pass
        # if subprocess.call(f'xetex {output_file}') != 0:
        #     print('Exit-code not 0, check result!')
        # else:
        #     os.system('open sometexfile.pdf')#

def dl_bill(request, bill_id):
    bill =  Bill.objects.get(id=bill_id)

    output_dir = Path(settings.MEDIA_ROOT).absolute()
    output_dir.mkdir(parents=True, exist_ok=True)
    print(output_dir)
    cust = bill.customer.surname
    if bill.customer.company:
        cust = bill.customer.company
    output_file = Path(output_dir / f'{cust}_{bill.number}.tex')
    output_pdf = Path(output_dir / f'{cust}_{bill.number}.pdf')

    create_pdf(output_dir=output_dir, output_file=output_file, output_pdf=output_pdf)

    with open(output_pdf, 'rb') as fh:
        response = HttpResponse(fh.read(), content_type="application/pdf")
        response['Content-Disposition'] = 'inline; filename=' + output_pdf.name
        return response

####### CUSTOMER VIEWS ##########



def customers(request):
    '''
    Get the customers overview view
    Lists customers and gives the links to see or edit them
    '''
    customers = Customer.objects.all()

    template = loader.get_template('customers.html')
    context = {
        'customers': customers,
        'title': 'Kunden'
    }
    return HttpResponse(template.render(request=request, context=context))


def customer(request, customer_id):
    '''
    Get the customer overview view
    Shows the customer and gives the links to see or edit him
    '''
    template = loader.get_template('customer.html')
    customer = Customer.objects.get(id=customer_id)

    context = {
        'title': f'Kunde {str(customer)}',
        'customer': customer,
        }
    return HttpResponse(template.render(request=request, context=context))

def edit_customer(request, customer_id):
    template = loader.get_template('new_customer.html')
    customer = Customer.objects.get(id=customer_id)
    cform = CustomerForm(request.POST or None, instance=customer, prefix="c")
    if cform.is_valid():
            context = {
        'title': f'Kunden bearbeiten',
        'cform': cform,
    }
    return HttpResponse(template.render(request=request, context=context))

def new_customer(request):
    template = loader.get_template('new_customer.html')
    cform = CustomerForm(request.POST or None, prefix="c")
    some_form = CronForm(request.POST or None, prefix="some_")

    if some_form.is_valid() and request.POST:
        customer = some_form.cleaned_data
        print(customer)
        cform = CustomerForm(request.POST or None, instance=customer, prefix="c")
        print(customer)
    print(cform.errors)

    if cform.is_valid():
        print("OK THANKS!")
        customer = cform.save()
        print("Redirecting ...")
        return redirect('customer', customer_id=customer.id)
    context = {
        'title': f'Neue Rechnung erstellen',
        'cform': cform,
        'some_form': some_form
    }
    return HttpResponse(template.render(request=request, context=context))

def del_customer(request, customer_id):
    Customer.objects.filter(id=customer_id).delete()
    return customers(request)



########### PARTS VIEWS