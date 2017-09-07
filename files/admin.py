from django.contrib import admin
from .models import FileObject

class FileObjectAdmin(admin.ModelAdmin):
	list_display = ('user','data_type','description','uploaded_at','document')

admin.site.register(FileObject,FileObjectAdmin)
# Register your models here.
