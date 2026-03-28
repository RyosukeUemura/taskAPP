from django.contrib import admin

from .models import RecurringTask, Subscription


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "billing_cycle", "next_billing_date", "is_active")
    list_filter = ("billing_cycle", "is_active")
    search_fields = ("name",)
    list_editable = ("is_active",)
    date_hierarchy = "next_billing_date"


@admin.register(RecurringTask)
class RecurringTaskAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "interval_type",
        "interval_value",
        "day_of_week",
        "next_due_date",
        "end_date",
        "is_active",
    )
    list_filter = ("interval_type", "day_of_week", "is_active")
    search_fields = ("name",)
    list_editable = ("is_active",)
    date_hierarchy = "next_due_date"
    fieldsets = (
        (None, {
            "fields": ("name", "description", "is_active"),
        }),
        ("スケジュール設定", {
            "fields": (
                "interval_type",
                "interval_value",
                "day_of_week",
                "start_date",
                "end_date",
            ),
        }),
        ("実行日", {
            "fields": ("next_due_date",),
        }),
    )
