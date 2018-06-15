from django.contrib import admin
from docportal.models import DocumentModel, ManufacturedUnitModel, DocumentPermission, UnitPermission


class DocumentAdmin(admin.ModelAdmin):
    list_display = ('name', 'doc_type', 'unit', 'file')


class UnitAdmin(admin.ModelAdmin):
    list_display = ('name',)


class DocPermissionAdmin(admin.ModelAdmin):
    list_display = ('viewer', 'document')


class UnitPermissionAdmin(admin.ModelAdmin):
    list_display = ('viewer', 'unit')


admin.site.register(DocumentModel, DocumentAdmin)
admin.site.register(ManufacturedUnitModel, UnitAdmin)
admin.site.register(DocumentPermission, DocPermissionAdmin)
admin.site.register(UnitPermission, UnitPermissionAdmin)
