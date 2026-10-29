from django.contrib import admin
from .models import Employee


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "position", "department", "email", "is_available", "date_hired")
    list_filter = ("is_available", "department")
    search_fields = ("name", "position", "email")
    actions = ["mark_unavailable", "mark_available"]

    @admin.action(description="Soft delete selected (is_available = False)")
    def mark_unavailable(self, request, queryset):
        queryset.update(is_available=False)

    @admin.action(description="Restore selected (is_available = True)")
    def mark_available(self, request, queryset):
        queryset.update(is_available=True)