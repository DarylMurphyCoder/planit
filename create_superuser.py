#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'planit.settings')
django.setup()

from django.contrib.auth.models import User  # noqa: E402

if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print("Superuser 'admin' created successfully!")
else:
    print("Superuser 'admin' already exists.")
