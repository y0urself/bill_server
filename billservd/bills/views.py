from django.conf import settings
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.forms.models import modelformset_factory
from django.forms.formsets import formset_factory
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect, csrf_exempt

from pathlib import Path

from .build_tex import create_pdf, create_tex, get_path
from .models import Customer, Bill, Part, CustomerForm, BillForm, PartForm, CronForm, AuthForm, PartPaymentForm


###### OTHER VIEWS ######

def login_req(request):
    template = loader.get_template('login.html')
    login_form = AuthenticationForm(data = request.POST)
    print(request.POST)
    print(login_form.errors)
    if login_form.is_valid():
        username = login_form.cleaned_data.get('username')
        raw_password = login_form.cleaned_data.get('password')
        user = authenticate(username=username, password=raw_password)
        if user.is_authenticated:
            login(request, user)
            return redirect('bills')
        else:
            print("NOT AUTH")
    else:
        print("FORM NOT VALID ...")

    context = {
        'login_form': login_form,
    }
    return HttpResponse(template.render(request=request, context=context))

###### BILL VIEWS ######

@login_required
def bills(request):
    bills_list = Bill.objects.all()

    template = loader.get_template('bills.html')
    context = {
        'bills_list': bills_list,
        'title': 'Rechnungen'
    }
    return HttpResponse(template.render(request=request, context=context))

@login_required
def show_bill(request, bill_id):
    bill = Bill.objects.get(id=bill_id)
    payform = PartPaymentForm(initial={'part_opts': 0.66})
    template = loader.get_template('bill.html')
    output_dir = Path(settings.MEDIA_ROOT).absolute()
    print(Path(output_dir / "bla"))
    bill.update_sum()
    context = {
        'bill': bill,
        'payform': payform,
        'title': f'Rechnung Nr. {bill.number}'
    }
    return HttpResponse(template.render(request=request, context=context))


@login_required
def new_bill(request, customer_id=None):
    print(request.POST)
    template = loader.get_template('new_bill.html')

    PartFormset = modelformset_factory(Part, PartForm, extra=1)
    bform = BillForm(request.POST or None, prefix="b")
    cform = CustomerForm(request.POST or None, prefix="c")
    pform = PartFormset(request.POST or None, prefix="p", queryset=Part.objects.none())
    #some_form = CronForm(request.POST or None, prefix="some_")

    # if 'choose' in request.POST and some_form.is_valid():
    #     print('YAAAAAY')
    #     pform = PartFormset(None, prefix="p", queryset=Part.objects.none())
    #     print(request.POST['some_-customer'])
    #     customer_id = request.POST['some_-customer']

    if customer_id:
        c = Customer.objects.get(id=customer_id)
        cform = CustomerForm(request.POST or None, instance=c, prefix="c")
        #some_form = CronForm(request.POST or None, prefix="some_", initial={'customer': customer_id})

    if bform.is_valid():
        print("bVALID")
        if cform.is_valid():
            print("cVALID")
            if pform.is_valid():
                print("pVALID")
                bill = bform.save()
                c = cform.save()
                parts = pform.save()
                for part in parts:
                    bill.parts.add(part)
                bill.part_sum = bill.update_sum()
                bill.customer = c
                bill.save()
                print("Redirecting ...")
                for part in bill.parts.all():
                    part.nsum = part.calc_nsum()
                    part.save()
                create_tex(bill=bill)
                return redirect('bill', bill_id=bill.id)
        else:
            print("Not valid ...")
            print(bform.errors)
            print(cform.errors)
            print(pform.errors)
            print(cform.non_field_errors)

    context = {
        'title': f'Neue Rechnung erstellen',
        'bform': bform,
        'cform': cform,
        'pform': pform,
        #'some_form': some_form
    }
    return HttpResponse(template.render(request=request, context=context))

@login_required
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
        bill.part_sum = bill.update_sum()
        bill.save()
            
        for part in bill.parts.all():
            part.nsum = part.calc_nsum()
            part.save()

        create_tex(bill = bill)
        return redirect('bill', bill_id=bill_id)
    
    context = {
        'title': f'Rechnung bearbeiten',
        'bform': bform,
        'cform': cform,
        'pform': pform
    }
    return HttpResponse(template.render(request=request, context=context))

@login_required
def del_bill(request, bill_id):
    Bill.objects.filter(id=bill_id).delete()
    return bills(request)


@login_required
def dl_bill(request, bill_id):
    bill =  Bill.objects.get(id=bill_id)

    output_dir, output_file, output_pdf = get_path(company=bill.customer.company, surname=bill.customer.surname, number=bill.number, with01=False)

    if not output_file.exists():
        create_tex(bill)

    create_pdf(output_dir=output_dir, output_file=output_file, output_pdf=output_pdf)

    with open(output_pdf, 'rb') as fh:
        response = HttpResponse(fh.read(), content_type="application/pdf")
        response['Content-Disposition'] = 'inline; filename=' + output_pdf.name
        return response

@login_required
def dl_part_bill(request, bill_id):
    bill =  Bill.objects.get(id=bill_id)

    _, _, output_pdf = get_path(company=bill.customer.company, surname=bill.customer.surname, number=bill.number, with01=True)

    if not output_pdf.exists():
        return redirect('bill', customer_id=bill_id)

    with open(output_pdf, 'rb') as fh:
        response = HttpResponse(fh.read(), content_type="application/pdf")
        response['Content-Disposition'] = 'inline; filename=' + output_pdf.name
        return response

@login_required
def create_part_payment_bill(request, bill_id):
    bill =  Bill.objects.get(id=bill_id)
    print(request.POST['part_opts'])
    part = float(request.POST['part_opts'])
    payform = PartPaymentForm(request.POST or None)
    print(request)
    if request.POST:
        print(payform)
    if payform.is_valid():
        print(type(part) , part)
        output_dir = Path(settings.MEDIA_ROOT).absolute()
        output_dir.mkdir(parents=True, exist_ok=True)
        print(output_dir)
        cust = bill.customer.surname
        if bill.customer.company:
            cust = bill.customer.company
        # Some other FileName for Partitial Bills ...
        output_file = Path(output_dir / f'{cust}_{bill.number}_01.tex')
        output_pdf = Path(output_dir / f'{cust}_{bill.number}_01.pdf')

        create_tex(bill=bill, part=part)

        create_pdf(output_dir=output_dir, output_file=output_file, output_pdf=output_pdf)
    else:
        print("NOTVALID")
    return redirect('bill', bill_id=bill_id)

    with open(output_pdf, 'rb') as fh:
        response = HttpResponse(fh.read(), content_type="application/pdf")
        response['Content-Disposition'] = 'inline; filename=' + output_pdf.name
        return response

####### CUSTOMER VIEWS ##########

@login_required
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

@login_required
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

@login_required
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

@login_required
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

@login_required
def del_customer(request, customer_id):
    Customer.objects.filter(id=customer_id).delete()
    return customers(request)



########### PARTS VIEWS


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
