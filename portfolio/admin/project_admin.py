from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from jalali_date.admin import ModelAdminJalaliMixin

from ..models import ProjectImage, Project
from ..forms import ProjectImageTabuFormSetAdmin


class ProjectImageTabu(admin.TabularInline):
    model = ProjectImage
    formset = ProjectImageTabuFormSetAdmin
    fields = ('image', 'is_main',)
    extra = 1
    min_num = 1


@admin.register(Project)
class ProjectAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    fieldsets = (
        (_('Project Information'), {
            'fields': (
                'title', 'description', 'client', 'link', 'location', 'start_date', 'video', 'keywords', 'is_active'
            )
        }),
        (_('Slug Settings'), {
            'classes': ('collapse',),
            'fields': ('slug_change', 'slug')
        }),
        (_('Date and Time'), {
            'classes': ('collapse',),
            'fields': ('datetime_created', 'datetime_updated'),
        }),
    )
    readonly_fields = ('datetime_created', 'datetime_updated')
    inlines = (ProjectImageTabu,)
    search_fields = ('title', 'client')
    list_filter = ('is_active', 'start_date')
    ordering = ('-datetime_updated',)
    list_display = ('title', 'client', 'start_date', 'is_active', 'datetime_updated')
