from datetime import date, timedelta

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from tasks.models import Category, Task


class Command(BaseCommand):
    help = "Add 10 sample tasks per user with varied priorities, due dates, and categories"

    def handle(self, *args, **options):
        sample_tasks = [
            {
                "title": "Finish project brief",
                "description": "Draft the project overview and share for review.",
                "priority": "high",
                "days_from_now": 1,
                "category": "Work",
                "is_completed": False,
            },
            {
                "title": "Prepare meeting agenda",
                "description": "List discussion points and timeboxes for tomorrow's sync.",
                "priority": "medium",
                "days_from_now": 2,
                "category": "Work",
                "is_completed": False,
            },
            {
                "title": "Book dentist appointment",
                "description": "Schedule a 6-month checkup and cleaning.",
                "priority": "medium",
                "days_from_now": 7,
                "category": "Personal",
                "is_completed": False,
            },
            {
                "title": "Weekly grocery run",
                "description": "Plan meals and pick up essentials for the week.",
                "priority": "low",
                "days_from_now": 3,
                "category": "Home",
                "is_completed": False,
            },
            {
                "title": "Refactor auth flow",
                "description": "Clean up login and signup views for readability.",
                "priority": "high",
                "days_from_now": 4,
                "category": "Work",
                "is_completed": False,
            },
            {
                "title": "Backup family photos",
                "description": "Upload recent photos to cloud storage.",
                "priority": "low",
                "days_from_now": 10,
                "category": "Personal",
                "is_completed": False,
            },
            {
                "title": "Pay utility bills",
                "description": "Settle electricity, water, and internet bills.",
                "priority": "medium",
                "days_from_now": 5,
                "category": "Home",
                "is_completed": False,
            },
            {
                "title": "Plan weekend hike",
                "description": "Choose a trail and invite friends.",
                "priority": "low",
                "days_from_now": 9,
                "category": "Personal",
                "is_completed": False,
            },
            {
                "title": "Create test coverage report",
                "description": "Run tests and summarize gaps for the team.",
                "priority": "high",
                "days_from_now": 2,
                "category": "Work",
                "is_completed": False,
            },
            {
                "title": "Deep clean kitchen",
                "description": "Wipe appliances, organize pantry, and mop floors.",
                "priority": "medium",
                "days_from_now": 6,
                "category": "Home",
                "is_completed": False,
            },
        ]

        total_created = 0

        for user in User.objects.all():
            category_cache = {}

            for task_data in sample_tasks:
                category_name = task_data["category"]
                if category_name not in category_cache:
                    category_obj, _ = Category.objects.get_or_create(
                        user=user,
                        name=category_name,
                    )
                    category_cache[category_name] = category_obj
                else:
                    category_obj = category_cache[category_name]

                due_date = date.today() + timedelta(days=task_data["days_from_now"])

                task, created = Task.objects.get_or_create(
                    user=user,
                    title=task_data["title"],
                    defaults={
                        "description": task_data["description"],
                        "priority": task_data["priority"],
                        "due_date": due_date,
                        "category": category_obj,
                        "is_completed": task_data["is_completed"],
                    },
                )

                if created:
                    total_created += 1

        self.stdout.write(
            self.style.SUCCESS(f"Created {total_created} sample tasks across all users")
        )
