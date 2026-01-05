from django.contrib import admin
from .models import Category, Task, TaskNote, RecurringTask, SharedTaskList


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'created_at')
    list_filter = ('created_at', 'user')
    search_fields = ('name',)


class TaskNoteInline(admin.TabularInline):
    model = TaskNote
    extra = 1


class RecurringTaskInline(admin.StackedInline):
    model = RecurringTask
    extra = 0


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'priority', 'is_completed', 'due_date', 'category', 'created_at')
    list_filter = ('is_completed', 'priority', 'created_at', 'due_date')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [TaskNoteInline, RecurringTaskInline]
    fieldsets = (
        ('Task Info', {
            'fields': ('user', 'title', 'description', 'category')
        }),
        ('Status', {
            'fields': ('is_completed', 'priority')
        }),
        ('Dates', {
            'fields': ('due_date', 'created_at', 'updated_at')
        }),
    )


@admin.register(TaskNote)
class TaskNoteAdmin(admin.ModelAdmin):
    list_display = ('task', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('task__title', 'content')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(RecurringTask)
class RecurringTaskAdmin(admin.ModelAdmin):
    list_display = ('task', 'frequency', 'end_date')
    list_filter = ('frequency',)
    search_fields = ('task__title',)


@admin.register(SharedTaskList)
class SharedTaskListAdmin(admin.ModelAdmin):
    list_display = ('task', 'shared_with_user', 'permission_level', 'created_at')
    list_filter = ('permission_level', 'created_at')
    search_fields = ('task__title', 'shared_with_user__username')
