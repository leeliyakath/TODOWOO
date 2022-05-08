from django.contrib import admin
from .models import Todo
# Register your models here.

# make the created date visible
class TodoAdminReadonly(admin.ModelAdmin):
    readonly_fields = ('created_date_time',)

admin.site.register(Todo, TodoAdminReadonly)
