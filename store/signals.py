from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import CustomUserModel
from .models import Customer
from django.contrib.auth import get_user_model


User = get_user_model()
@receiver(post_save, sender=User)
def create_customer(sender, instance, created, **kwargs):
    if created:  # فقط وقتی که یوزر جدید ساخته بشه
        Customer.objects.create(
            user = instance)
        # print(instance.phone_number)