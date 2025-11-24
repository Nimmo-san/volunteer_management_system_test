from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver

from core.choices import SystemRole
from .models import User


@receiver(post_save, sender=User)
def sync_user_role_group(sender, instance: User, **kwargs):
    """
    Ensure user is in the group matching their role, and
    removed from the other role groups.
    """
    role = instance.role
    # Construct a SystemRole member from the stored role value
    try:
        desired_group_name = SystemRole(role).value
    except ValueError:
        # Unknown role value; nothing to sync
        return
    if not desired_group_name:
        return

    # Get or create the desired group
    desired_group, _ = Group.objects.get_or_create(name=desired_group_name)

    # Remove from all role groups (use labels to match group names)
    role_group_names = {r.label for r in SystemRole}
    instance.groups.remove(*instance.groups.filter(name__in=role_group_names))

    # Add to the correct group
    instance.groups.add(desired_group)
