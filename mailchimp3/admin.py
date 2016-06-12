from django.contrib import admin
from .models import *

class MailChimpAdmin(admin.ModelAdmin):
    pass

class ListAdmin(MailChimpAdmin):
    list_display = [ 'mailchimp_id', 'name']

class MemberAdmin(MailChimpAdmin):
    list_display = ['mailchimp_id', 'email_address', 'status', 'list']


admin.site.register(List, ListAdmin)
admin.site.register(Member, MemberAdmin)


