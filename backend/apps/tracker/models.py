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
    name = models.CharField("タスク名", max_length=255)
    description = models.TextField("詳細メモ", blank=True)
    cycle_months = models.PositiveSmallIntegerField("実行周期（ヶ月）")
    next_due_date = models.DateField("次回実行予定日")
    is_active = models.BooleanField("有効", default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "定期タスク"
        verbose_name_plural = "定期タスク"
        ordering = ["next_due_date"]

    def __str__(self) -> str:
        return f"{self.name}（{self.cycle_months}ヶ月ごと）"
