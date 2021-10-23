from django.contrib import admin
from .models import TaskToPerform


@admin.register(TaskToPerform)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'title', 'desc', 'complete', 'created']
