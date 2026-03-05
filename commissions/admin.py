from django.contrib import admin
from .models import *

<<<<<<< HEAD
from .models import Commission, CommissionType

=======
>>>>>>> ebf6af3 (feat: class-based views and admin)

class CommissionTypeAdmin(admin.ModelAdmin):
    model = CommissionType


<<<<<<< HEAD
class CommissionAdmin(admin.ModelAdmin):
    model = Commission


admin.site.register(CommissionType, CommissionTypeAdmin)
admin.site.register(Commission, CommissionAdmin)
=======
class CommissionTypeInline(admin.TabularInline):
    model = CommissionType


class CommissionAdmin(admin.ModelAdmin):
    model = Commission
    inlines = [CommissionTypeInline,]


admin.site.register(Commission, CommissionAdmin)
admin.site.register(CommissionType, CommissionTypeAdmin)
>>>>>>> ebf6af3 (feat: class-based views and admin)
