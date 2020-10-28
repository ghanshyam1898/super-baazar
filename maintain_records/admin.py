from .models import *
from django.contrib import admin


class DealersAdmin(admin.ModelAdmin):
  list_display = ('dealer_number', 'dealer_name', 'dealer_phone_number', 'dealer_email', 'dealer_address', 'total_transaction', )

class PurchaseAdmin(admin.ModelAdmin):
  list_display = ('invoice_by', 'invoice_date_and_time', )  

admin.site.register(DealersDetails, DealersAdmin)
admin.site.register(PurchaseDetails, PurchaseAdmin)
admin.site.register(SalesDetails)
admin.site.register(ItemDetails)
