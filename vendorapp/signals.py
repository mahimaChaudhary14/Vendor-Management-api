# signals.py

from datetime import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Avg
from .models import PurchaseOrder

@receiver(post_save, sender=PurchaseOrder)
def update_vendor_metrics(sender, instance, **kwargs):
    if instance.status == 'completed':
        completed_purchases = PurchaseOrder.objects.filter(vendor=instance.vendor, status='completed')
        on_time_deliveries = completed_purchases.filter(delivery_date__lte=timezone.now())
        instance.vendor.on_time_delivery_rate = (on_time_deliveries.count() / completed_purchases.count()) * 100 if completed_purchases.count() > 0 else 0

        completed_purchases_with_rating = completed_purchases.exclude(quality_rating=None)
        instance.vendor.quality_rating_avg = completed_purchases_with_rating.aggregate(Avg('quality_rating'))['quality_rating__avg'] if completed_purchases_with_rating.count() > 0 else 0

        instance.vendor.save()

    if instance.acknowledgment_date:
        completed_purchases = PurchaseOrder.objects.filter(vendor=instance.vendor, status='completed').exclude(acknowledgment_date=None)
        response_times = [(p.acknowledgment_date - p.issue_date).total_seconds() for p in completed_purchases]
        instance.vendor.average_response_time = sum(response_times) / len(response_times) if len(response_times) > 0 else 0

        instance.vendor.save()

    instance.vendor.fulfillment_rate = (completed_purchases.filter(issues=None).count() / completed_purchases.count()) * 100 if completed_purchases.count() > 0 else 0
    instance.vendor.save()
