from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.auth.admin import UserAdmin
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.mail import send_mass_mail

from users.models import User
from .models import Subscriber

from polar_auth.settings import DEFAULT_FROM_EMAIL as from_address


@admin.action(description='Send email')
def admin_email(adminobject, request, queryset):
    print(request)
    print(request.POST)
    if 'apply' in request.POST:
        subject = request.POST['subject']
        message = request.POST['content']
        emails = [(subject, message, from_address, [object.email])
                  for object in queryset
                  ]
        send_mass_mail(emails, fail_silently=False)

        adminobject.message_user(request, f"Sent email to {queryset.count()} addresses.")
        return HttpResponseRedirect(request.get_full_path())

    context = {'queryset': queryset, 'count': queryset.count()}
    return render(request, 'admin/send_email.html', context=context)

    for object in queryset:
        print(object.email)


# Register your models here.
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('email', 'consent', 'privacy', 'first_survey_done', 'authorized')
    list_filter = ('email', 'consent', 'privacy', 'first_survey_done', 'authorized')
    fieldsets = (
        (None, {'fields': ('email', 'home_address', 'size', 'consent', 'privacy', 'first_survey_done', 'password', 'user_id', 'authorized')}),
        ('Permissions', {'fields': ('is_superuser',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'home_address', 'size', 'consent', 'privacy', 'first_survey_done', 'password',
                       'is_superuser')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    actions = [admin_email]


class SubscriberAdmin(ModelAdmin):
    model = Subscriber
    actions = [admin_email]


admin.site.register(User, CustomUserAdmin)
admin.site.register(Subscriber, SubscriberAdmin)
