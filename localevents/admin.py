from django.contrib import admin

from .models import Event, EventCategory, EventSignup


class EventCategoryAdmin(admin.ModelAdmin):
    model = EventCategory


class EventAdmin(admin.ModelAdmin):
    model = Event


class EventSignupAdmin(admin.ModelAdmin):
    model = EventSignup


admin.site.register(EventCategory, EventCategoryAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(EventSignup, EventSignupAdmin)
