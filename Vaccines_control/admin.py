from django.contrib import admin

# Register your models here.

from .models import *

# from . forms import StockCreateForm


class StockAdmin(admin.ModelAdmin):
     pass
admin.site.register(Stock, StockAdmin)


class VaccinatorAdmin(admin.ModelAdmin):
    pass
admin.site.register(Vaccinator, VaccinatorAdmin)


class DCCTAdmin(admin.ModelAdmin):
    pass
admin.site.register(DCCT, DCCTAdmin)


class StockHistoryAdmin(admin.ModelAdmin):
    pass
admin.site.register(StockHistory, StockHistoryAdmin)


