from django.contrib.auth.models import Group
from django.db.models.signals import post_migrate
from django.dispatch import receiver

@receiver(post_migrate)
def create_default_roles(sender, **kwargs):
    roles = ['admin', 'Promotor', 'Analista']
    for role in roles:
        Group.objects.get_or_create(name=role)
