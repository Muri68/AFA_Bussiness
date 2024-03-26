from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from vendor.models import Company
from .models import User


@receiver(post_save, sender=User)
def post_save_create_profile_receiver(sender, instance, created, **kwargs):
    print(created)
    if created:
        Company.objects.create(user=instance)
    else:
        try:
            vendor = Company.objects.get(user=instance)
            vendor.save()
            print("Vendor Created")
        except:
            # Create the userprofile if not exist
            # if not User.is_superuser:
            Company.objects.create(user=instance)
            print("Vendor Created")


@receiver(pre_save, sender=User)
def pre_save_profile_receiver(sender, instance, **kwargs):
    pass
# post_save.connect(post_save_create_profile_receiver, sender=User)