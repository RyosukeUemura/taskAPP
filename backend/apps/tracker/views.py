from dateutil.relativedelta import MO, TU, WE, TH, FR, SA, SU, relativedelta
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .models import RecurringTask, Subscription

# dateutil の weekday オブジェクトを DayOfWeek の整数値にマッピング
_WEEKDAY_DELTA = {
    0: MO,
    1: TU,
    2: WE,
    3: TH,
    4: FR,
    5: SA,
    6: SU,
}


def dashboard(request):
    subscriptions = Subscription.objects.filter(is_active=True).order_by(
        "next_billing_date"
    )
    monthly_total = subscriptions.filter(
        billing_cycle=Subscription.BillingCycle.MONTHLY
    ).aggregate(total=Sum("price"))["total"] or 0

    yearly_total = (
        subscriptions.filter(
            billing_cycle=Subscription.BillingCycle.YEARLY
        ).aggregate(total=Sum("price"))["total"]
        or 0
    )

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

    # 1. interval_type / interval_value に基づいて次回日付を計算
    if task.interval_type == RecurringTask.IntervalType.WEEKS:
        new_date = task.next_due_date + relativedelta(weeks=task.interval_value)
    else:
        new_date = task.next_due_date + relativedelta(months=task.interval_value)

    # 2. day_of_week が設定されていれば「直近の指定曜日」に調整
    if task.day_of_week is not None:
        new_date = new_date + relativedelta(weekday=_WEEKDAY_DELTA[task.day_of_week])

    # 3. end_date を超える場合はタスクを無効化して終了
    if task.end_date and new_date > task.end_date:
        task.is_active = False
        task.save(update_fields=["is_active", "updated_at"])
    else:
        task.next_due_date = new_date
        task.save(update_fields=["next_due_date", "updated_at"])

    return redirect("tracker:dashboard")
