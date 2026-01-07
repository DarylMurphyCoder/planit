from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from tasks.models import Category


class Command(BaseCommand):
    help = 'Add default categories (Work, Personal, Home) to all users'

    def handle(self, *args, **options):
        default_categories = ['Work', 'Personal', 'Home']
        count = 0

        for user in User.objects.all():
            for cat_name in default_categories:
                category, created = Category.objects.get_or_create(
                    user=user,
                    name=cat_name
                )
                if created:
                    count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {count} default categories'
            )
        )
