from django.contrib import admin

from jalali_date.admin import ModelAdminJalaliMixin

from ..models import ContactMe


@admin.register(ContactMe)
class ContactMeAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ('full_name', 'user', 'subject', 'email', 'datetime_created', 'answer',)
    ordering = ('answer', '-datetime_created',)
    fields = ('full_name', 'user', 'subject', 'email', 'message', 'answer', 'datetime_created', 'datetime_updated',)
    readonly_fields = ('datetime_created', 'datetime_updated', 'user',)
    list_filter = ('answer',)
    search_fields = ('full_name', 'subject', 'email', 'user__username', 'user__email')

    def has_add_permission(self, request):
        return False
