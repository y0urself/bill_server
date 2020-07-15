from django.contrib import admin

# Register your models here.

from .models import Bill, Part, Customer

admin.site.register(Bill)
admin.site.register(Part)
admin.site.register(Customer)