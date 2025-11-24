from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from accounts.models import SystemRole


class Command(BaseCommand):
    help = "Create one test user for each system role and print their groups."

    def handle(self, *args, **options):
        User = get_user_model()

        # Simple shared password for all test accounts
        password = "Test1234!"

        role_to_username = {
            SystemRole.SYS_ADMIN: "sys_admin_user",
            SystemRole.MANAGER: "manager_user",
            SystemRole.STAFF: "staff_user",
            SystemRole.VOLUNTEER: "volunteer_user",
        }

        self.stdout.write(self.style.WARNING(f"Using password: {password}"))

        for role, username in role_to_username.items():
            user, created = User.objects.get_or_create(username=username)
            user.email = f"{username}@example.com"
            user.role = role
            user.set_password(password)
            user.save()

            # ensure the group exists (in case post_migrate didn’t run yet)
            group, _ = Group.objects.get_or_create(name=role.value)

            # reload groups after signals
            user.refresh_from_db()
            group_names = list(user.groups.values_list("name", flat=True))

            if created:
                self.stdout.write(self.style.SUCCESS(f"Created user: {username} ({role})"))
            else:
                self.stdout.write(self.style.NOTICE(f"Updated user: {username} ({role})"))

            self.stdout.write(f"  -> groups: {group_names}")

        self.stdout.write(self.style.SUCCESS("Done."))
