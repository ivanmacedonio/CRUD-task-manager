from django.contrib import admin
from .models import Task

class TaskAdmin(admin.ModelAdmin):

    readonly_fields = ("created", )

#le agregamos la propiedad de solo lectura a un campo y
#se lo enviamos al panel 


admin.site.register(Task, TaskAdmin)


