from django.contrib import admin

from .models import Mailing, MailingFilter


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    pass


@admin.register(MailingFilter)
class MailingFilterAdmin(admin.ModelAdmin):
    pass
