from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from core.choices import SystemRole, ApplicationStatus, CheckType, CheckStatus, ShiftStatus

from volunteers.models import VolunteerProfile
from staff_programs.models import StaffProfile, ProgramRequest
from applications.models import Opportunity, Application
from placements.models import Placement, Shift
from compliance.models import ComplianceCheck


class Command(BaseCommand):
    help = "Seed demo data: users, profiles, program, opportunity, application, placement, checks."

    def handle(self, *args, **options):
        User = get_user_model()
        password = "Test1234!"

        self.stdout.write(self.style.WARNING(f"Using demo password: {password}"))

        # ---- Users ----
        sys_admin, _ = User.objects.get_or_create(
            username="sys_admin_demo",
            defaults={"email": "sys_admin_demo@example.com", "role": SystemRole.SYS_ADMIN},
        )
        sys_admin.role = SystemRole.SYS_ADMIN
        sys_admin.set_password(password)
        sys_admin.save()

        manager, _ = User.objects.get_or_create(
            username="manager_demo",
            defaults={"email": "manager_demo@example.com", "role": SystemRole.MANAGER},
        )
        manager.role = SystemRole.MANAGER
        manager.set_password(password)
        manager.save()

        staff, _ = User.objects.get_or_create(
            username="staff_demo",
            defaults={"email": "staff_demo@example.com", "role": SystemRole.STAFF},
        )
        staff.role = SystemRole.STAFF
        staff.set_password(password)
        staff.save()

        volunteer_user, _ = User.objects.get_or_create(
            username="volunteer_demo",
            defaults={"email": "volunteer_demo@example.com", "role": SystemRole.VOLUNTEER},
        )
        volunteer_user.role = SystemRole.VOLUNTEER
        volunteer_user.set_password(password)
        volunteer_user.save()

        self.stdout.write(self.style.SUCCESS("Users created/updated."))

        # ---- Profiles ----
        manager_profile, _ = StaffProfile.objects.get_or_create(
            user=manager,
            defaults={
                "department": "Ward A",
                "job_title": "Ward Manager",
                "phone": "07123 456789",
            },
        )

        staff_profile, _ = StaffProfile.objects.get_or_create(
            user=staff,
            defaults={
                "department": "Ward A",
                "job_title": "Staff Nurse",
                "phone": "07123 456788",
            },
        )

        volunteer_profile, _ = VolunteerProfile.objects.get_or_create(
            user=volunteer_user,
            defaults={
                "phone": "07123 456780",
                "role_preference": "Ward support, patient engagement",
            },
        )

        self.stdout.write(self.style.SUCCESS("Profiles created/updated."))

        # ---- ProgramRequest ----
        program, _ = ProgramRequest.objects.get_or_create(
            title="Ward Companion Volunteers",
            created_by=manager_profile,
            defaults={
                "primary_contact": manager_profile,
                "department": "Ward A",
                "description": "Volunteers to support patients with companionship and mealtime support.",
                "volunteers_needed": 5,
                "eligibility_status": "eligible",
                "status": "active",
            },
        )
        program.secondary_contacts.add(staff_profile)

        self.stdout.write(self.style.SUCCESS("ProgramRequest created/updated."))

        # ---- Opportunity ----
        opportunity, _ = Opportunity.objects.get_or_create(
            program=program,
            title="Ward A Companion",
            defaults={
                "description": "Support patients by chatting, helping with non-clinical tasks.",
                "is_active": True,
                "positions": 3,
            },
        )

        self.stdout.write(self.style.SUCCESS("Opportunity created/updated."))

        # ---- Application ----
        application, created_app = Application.objects.get_or_create(
            volunteer=volunteer_profile,
            opportunity=opportunity,
            defaults={
                "status": ApplicationStatus.NEW,
                "notes": "Initial demo application.",
            },
        )
        if not created_app:
            application.status = ApplicationStatus.UNDER_REVIEW
            application.save()

        self.stdout.write(self.style.SUCCESS("Application created/updated."))

        # ---- Placement ----
        placement, _ = Placement.objects.get_or_create(
            volunteer=volunteer_profile,
            opportunity=opportunity,
            defaults={
                "supervisor": manager_profile,
                "start_date": "2025-01-01",
                "hours_per_week": 4.0,
                "is_active": True,
            },
        )

        self.stdout.write(self.style.SUCCESS("Placement created/updated."))

        # ---- Shift ----
        Shift.objects.get_or_create(
            placement=placement,
            start="2025-01-02T09:00:00Z",
            end="2025-01-02T13:00:00Z",
            defaults={
                "location": "Ward A",
                "status": ShiftStatus.SCHEDULED,
            },
        )

        self.stdout.write(self.style.SUCCESS("Shift created (or already existed)."))

        # ---- Compliance Checks ----
        for check_type in [CheckType.DBS, CheckType.REFERENCES, CheckType.RIGHT_TO_WORK]:
            ComplianceCheck.objects.get_or_create(
                volunteer=volunteer_profile,
                check_type=check_type,
                defaults={
                    "status": CheckStatus.PENDING,
                    "details": f"{check_type} check (demo).",
                },
            )

        self.stdout.write(self.style.SUCCESS("Compliance checks created/updated."))

        self.stdout.write(self.style.SUCCESS("Demo data seeding complete."))
