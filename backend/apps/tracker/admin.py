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
    list_display = ("name", "cycle_months", "next_due_date", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name",)
    list_editable = ("is_active",)
    date_hierarchy = "next_due_date"
