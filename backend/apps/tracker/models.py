import datetime

from django.db import models


class Subscription(models.Model):
    class BillingCycle(models.TextChoices):
        MONTHLY = "monthly", "毎月"
        YEARLY = "yearly", "毎年"
        QUARTERLY = "quarterly", "毎四半期"

    name = models.CharField("サービス名", max_length=255)
    price = models.PositiveIntegerField("料金（円）")
    billing_cycle = models.CharField(
        "支払い周期",
        max_length=20,
        choices=BillingCycle.choices,
        default=BillingCycle.MONTHLY,
    )
    next_billing_date = models.DateField("次回支払日")
    is_active = models.BooleanField("有効", default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "サブスクリプション"
        verbose_name_plural = "サブスクリプション"
        ordering = ["next_billing_date"]

    def __str__(self) -> str:
        return f"{self.name} ({self.get_billing_cycle_display()})"


class RecurringTask(models.Model):
    class IntervalType(models.TextChoices):
        WEEKS = "weeks", "週間"
        MONTHS = "months", "ヶ月"

    class DayOfWeek(models.IntegerChoices):
        MONDAY = 0, "月曜日"
        TUESDAY = 1, "火曜日"
        WEDNESDAY = 2, "水曜日"
        THURSDAY = 3, "木曜日"
        FRIDAY = 4, "金曜日"
        SATURDAY = 5, "土曜日"
        SUNDAY = 6, "日曜日"

    name = models.CharField("タスク名", max_length=255)
    description = models.TextField("詳細メモ", blank=True)

    # --- スケジュール設定 ---
    interval_type = models.CharField(
        "間隔の単位",
        max_length=10,
        choices=IntervalType.choices,
        default=IntervalType.MONTHS,
    )
    interval_value = models.PositiveSmallIntegerField("間隔の数値", default=1)
    day_of_week = models.IntegerField(
        "指定曜日",
        choices=DayOfWeek.choices,
        null=True,
        blank=True,
    )
    start_date = models.DateField("開始日", default=datetime.date.today)
    end_date = models.DateField("終了日", null=True, blank=True)

    # --- 状態 ---
    next_due_date = models.DateField("次回実行予定日")
    is_active = models.BooleanField("有効", default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "定期タスク"
        verbose_name_plural = "定期タスク"
        ordering = ["next_due_date"]

    def __str__(self) -> str:
        return f"{self.name}（{self.schedule_label}）"

    @property
    def schedule_label(self) -> str:
        """人間が読みやすいスケジュール表記を返す。例: '2週間ごと (月曜日) - 2026/12/31まで'"""
        unit = "週間" if self.interval_type == self.IntervalType.WEEKS else "ヶ月"
        label = f"{self.interval_value}{unit}ごと"
        if self.day_of_week is not None:
            label += f" ({self.get_day_of_week_display()})"
        if self.end_date:
            label += f" - {self.end_date.strftime('%Y/%m/%d')}まで"
        return label
