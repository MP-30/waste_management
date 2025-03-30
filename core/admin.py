from django.contrib import admin
from .models import (
    Organization,
    WasteGenerator,
    WasteCollector,
    WasteType,
    WasteCollection,
    WasteGeneratorGroup
)

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'contact_person', 'contact_email', 'contact_phone')
    search_fields = ('name', 'contact_person', 'contact_email', 'owner__username')
    list_filter = ('owner',)

@admin.register(WasteGeneratorGroup)
class WasteGeneratorGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')
    ordering = ['name']

@admin.register(WasteGenerator)
class WasteGeneratorAdmin(admin.ModelAdmin):
    list_display = ('name', 'organization', 'address_line1', 'city', 'state', 'contact_person', 'is_active')
    list_filter = ('organization', 'group', 'is_active', 'state')
    search_fields = ('name', 'address_line1', 'address_line2', 'city', 'state', 'contact_person')

@admin.register(WasteCollector)
class WasteCollectorAdmin(admin.ModelAdmin):
    list_display = ('name', 'organization', 'license_number', 'contact_person')
    list_filter = ('organization',)
    search_fields = ('name', 'license_number', 'contact_person')

@admin.register(WasteType)
class WasteTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'hazardous')
    list_filter = ('hazardous',)
    search_fields = ('name',)

@admin.register(WasteCollection)
class WasteCollectionAdmin(admin.ModelAdmin):
    list_display = ('waste_generator', 'waste_collector', 'waste_type', 'quantity', 'collection_date', 'status')
    list_filter = ('status', 'waste_type', 'collection_date', 'waste_generator__organization')
    search_fields = ('waste_generator__name', 'waste_collector__name')
    date_hierarchy = 'collection_date'
