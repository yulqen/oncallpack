from django.contrib import admin

from .models import Organisation, Person, Mode, Role, Type, KeyContact, RemoteAmendment


class PersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'organisation')


class OrganisationAdmin(admin.ModelAdmin):
    list_display = ('name', 'type')


admin.site.register(Organisation, OrganisationAdmin)
admin.site.register(Mode)
admin.site.register(KeyContact)
admin.site.register(Type)
admin.site.register(Person, PersonAdmin)
admin.site.register(Role)
admin.site.register(RemoteAmendment)
