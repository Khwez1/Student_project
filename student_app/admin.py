from django.contrib import admin

from .models import Student, ClassGroup

class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'mark', 'class_group')
    search_fields = ('name',)
    list_filter = ('class_group',)

admin.site.register(Student, StudentAdmin)
admin.site.register(ClassGroup)