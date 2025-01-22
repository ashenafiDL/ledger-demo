from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import Department, JobTitle


@admin.register(Department)
class DepartmentAdmin(ModelAdmin):
    list_display = (
        "department_name_en",
        "department_name_am",
        "abbreviation_en",
        "abbreviation_am",
        "created_at",
        "updated_at",
    )
    ordering = ["department_name_en"]


@admin.register(JobTitle)
class JobTitleAdmin(ModelAdmin):
    list_display = ("title_en", "title_am", "created_at", "updated_at")
    ordering = ["title_en"]
