from dateutil.relativedelta import relativedelta
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

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


@require_POST
def complete_task(request, task_id: int):
    task = get_object_or_404(RecurringTask, pk=task_id)
    task.next_due_date += relativedelta(months=task.cycle_months)
    task.save(update_fields=["next_due_date", "updated_at"])
    return redirect("tracker:dashboard")
