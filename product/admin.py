from django.contrib import admin
from . import models

class VariationInline(admin.TabularInline):
    model = models.Variation
    extra = 1

class AdminProduct(admin.ModelAdmin):
    list_display = ['name', 'short_description',
                    'get_formatted_price', 'get_formatted_promoprice']
    
    inlines = [
        VariationInline
    ]

admin.site.register(models.Product, AdminProduct)
admin.site.register(models.Variation)