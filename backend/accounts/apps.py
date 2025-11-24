from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "accounts"

    def ready(self) -> None:
        from . import signals  # noqa: F401

        # def create_default_groups(sender, **kwargs):
        #     from django.contrib.auth.models import Group  
        #     for group_name in SystemRole.choices:
        #         Group.objects.get_or_create(name=group_name)

        # post_migrate.connect(create_default_groups, sender=self)
