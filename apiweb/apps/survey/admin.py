from django.contrib import admin

from .models import JobAfterLeaving
from .models import Sector
@admin.register(Sector)
class SectorAdmin(admin.ModelAdmin):
    pass


class JobAfterLeavingAdminInline(admin.StackedInline):
    model = JobAfterLeaving
    readonly_fields = ("date_created", "date_updated", "last_updated_by")
    extra = 0

    def save_model(self, request, obj, form, change):
        obj.last_updated_by = request.user
        obj.save()


@admin.register(JobAfterLeaving)
class JobAfterLeavingAdmin(admin.ModelAdmin):
    readonly_fields = ("date_created", "date_updated", "last_updated_by")

    fieldsets = [
        ( "Job information", {
            "fields":
                [ "position_name", "current_job", "company_name", "start_date",
                "stop_date", "inside_academia", "location_job" ]
            }
        ), ( "Extra information", {
                "classes": ["collapse"],
                "fields": ["comments",  "date_created", "date_updated", "last_updated_by"]
            }
        ),
    ]

    def save_model(self, request, obj, form, change):
        obj.last_updated_by = request.user
        obj.save()




# Register your models here.
