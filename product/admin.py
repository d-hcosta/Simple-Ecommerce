from django.contrib import admin
from . import models
from .forms import MandatoryVariation

class VariationInline(admin.TabularInline):
    model = models.Variation
    formset = MandatoryVariation
    min_num = 1
    extra = 0
    can_delete = True

class AdminProduct(admin.ModelAdmin):
    list_display = ['name', 'short_description',
                    'get_formatted_price', 'get_formatted_promoprice']
    
    inlines = [
        VariationInline
    ]

admin.site.register(models.Product, AdminProduct)
admin.site.register(models.Variation)