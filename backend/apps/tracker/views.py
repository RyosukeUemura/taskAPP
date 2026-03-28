from django.db.models import Sum
from django.shortcuts import render

from .models import RecurringTask, Subscription


def dashboard(request):
    subscriptions = Subscription.objects.filter(is_active=True).order_by(
        "next_billing_date"
    )
    monthly_total = subscriptions.filter(
        billing_cycle=Subscription.BillingCycle.MONTHLY
    ).aggregate(total=Sum("price"))["total"] or 0

    yearly_subscriptions = subscriptions.filter(
        billing_cycle=Subscription.BillingCycle.YEARLY
    )
    yearly_total = yearly_subscriptions.aggregate(total=Sum("price"))["total"] or 0

    tasks = RecurringTask.objects.filter(is_active=True).order_by("next_due_date")

    context = {
        "subscriptions": subscriptions,
        "monthly_total": monthly_total,
        "yearly_total": yearly_total,
        "tasks": tasks,
    }
    return render(request, "tracker/dashboard.html", context)
