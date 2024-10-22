from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from manager.models import Task, TaskType, Worker


# Register your models here.
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    ordering = ["deadline"]
    search_fields = ["priority"]


@admin.register(TaskType)
class TaskTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(Worker)
class WorkerAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("position",)
    fieldsets = UserAdmin.fieldsets + (("Position", {"fields": ("position",)}),)
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "Additional information",
            {
                "fields": (
                    "last_name",
                    "first_name",
                    "position",
                ),
            },
        ),
    )
