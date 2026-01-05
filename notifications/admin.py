from django.contrib import admin
from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'task', 'notification_type', 'sent_at', 'created_at')
    list_filter = ('notification_type', 'sent_at', 'created_at')
    search_fields = ('user__username', 'task__title')
    readonly_fields = ('created_at',)
