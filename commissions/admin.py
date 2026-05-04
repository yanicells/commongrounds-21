from .models import Commission, CommissionType
from django.contrib import admin
from .models import *


class CommissionTypeAdmin(admin.ModelAdmin):
    model = CommissionType


class CommissionAdmin(admin.ModelAdmin):
    model = Commission


admin.site.register(CommissionType, CommissionTypeAdmin)
admin.site.register(Commission, CommissionAdmin)
